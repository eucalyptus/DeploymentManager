# Software License Agreement (BSD License)
#
# Copyright (c) 2009-2014, Eucalyptus Systems, Inc.
# All rights reserved.
#
# Redistribution and use of this software in source and binary forms, with or
# without modification, are permitted provided that the following conditions
# are met:
#
# Redistributions of source code must retain the above
#   copyright notice, this list of conditions and the
#   following disclaimer.
#
#   Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the
#   following disclaimer in the documentation and/or other
#   materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# Author: Tony Beckham tony@eucalyptus.com
#
import json
import operator
import random
import socket
import xmlrpclib

from time import sleep
from paramiko import BadHostKeyException, AuthenticationException, SSHException, SSHClient, AutoAddPolicy


class UnableToFullfillRequestException(Exception):
    pass


class PxeManager(object):
    def __init__(self, cobbler_url, cobbler_user, cobbler_password, host_manager_client, public_ip_manager_client,
                 private_ip_manager_client, ssh_user="root", ssh_password="foobar"):
        """

        :param cobbler_url: (string) URL of cobbler server
        :param cobbler_user: (string) cobbler user
        :param cobbler_password: (string) cobbler user's password
        :param host_manager_client: (object) ResourceManger object for machines
        :param public_ip_manager_client: (object) ResourceManger object for public IPs
        :param private_ip_manager_client: (object) ResourceManger object for private IPs
        :param ssh_user: (string) user to attempt ssh login to reserved host
        :param ssh_password: (string) password for user of reserved host
        """
        self.cobbler = xmlrpclib.Server(cobbler_url)
        self.token = self.cobbler.login(cobbler_user, cobbler_password)
        self.host_manager = host_manager_client
        self.public_ip_manager = public_ip_manager_client
        self.private_ip_manager = private_ip_manager_client
        self.ssh_user = ssh_user
        self.ssh_password = ssh_password
        self.distro = {'centos': 'centos7-x86_64-raid0',
                       'rhel': 'rhel7-x86_64-raid0',
                       'centos6u7': 'centos6u7-x86_64-raid0',
                       'centos7u3': 'centos7u3-x86_64-raid0',
                       'rhel6u7': 'rhel6u7-x86_64-raid0',
                       'centos70': 'centos7u0-x86_64-raid0'}
        self.host_reservation = []
        self.file_name = 'kickstart.check'
        self.public_ip_reservation = []
        self.private_ip_reservation = []

    def make_host_reservation(self, owner, count, job_id, distro, tags=None):
        """
        Get machines from machine pool
        :param tags: Dict of tags that you want to use to filter resources
        :param owner: who the reservation is for
        :param count: how many machines to reserve
        :param job_id: unique identifier for the reservation
        :param distro: what OS to install (see the global dict "distro" for valid options)
        :return:
        """
        print "INFO: fetching list of idle hosts"
        available_machines = self.host_manager.find_resources(field="state", value="idle")
        print "INFO: Found {} total machines available".format(
            len(available_machines))
        if any(tags):
            print "INFO: applying tag filter to available host list"
            filtered_machines = self.filter_hosts_by_tags(available_machines, tags)
        else:
            filtered_machines = available_machines
        print "INFO: Found {} machines that meet the requested attribute " \
              "requirements".format(len(filtered_machines))
        if len(filtered_machines) < count and \
                len(filtered_machines) < len(available_machines):
            print "Oops...There are not enough free resources with the "\
                    "attributes you requested. You might need to "\
                    "reduce your attribute requirements."
            raise UnableToFullfillRequestException()
        elif len(filtered_machines) < count:
            print "Oops...There are not enough free resources to fill your request."
            raise UnableToFullfillRequestException()

        print "INFO: Randomizing filtered machines list"
        random.shuffle(filtered_machines)

        for i in range(count):
            hostname = filtered_machines[i]['hostname']
            print "INFO: using host", hostname
            data = json.dumps({'hostname': hostname, 'owner': owner, 'state': 'pxe', 'job_id': job_id})
            print "INFO: updating", hostname, "status to pxe"
            self.host_manager.update_resource(data)
            print "INFO: finding", hostname, "in Cobbler"
            simplehost = self.cobbler.find_system({"hostname": hostname})[0]
            try:
                print "INFO: placing file on", hostname, "before kickstarting"
                self.put_file_on_target(ip=self.cobbler.get_system(simplehost)['interfaces']['em1']['ip_address'],
                                        file_name=self.file_name)
                print "INFO: adding host", hostname, "to the reservation"
                if hostname not in self.host_reservation:
                    self.host_reservation.append(hostname)
                print "INFO: kickstarting host:", hostname
                self.kickstart_machine(system_name=hostname, distro=distro)
            except (BadHostKeyException, AuthenticationException, SSHException, socket.error):
                print "ERROR: could not reach", hostname, "for preflight checks"
                self.reservation_failed(system_name=hostname, state="needs_repair")
                print "INFO: reserving the next available host"
                self.make_host_reservation(owner=owner, count=1, job_id=job_id, distro=distro, tags=tags)

        '''
        Check that the resources in the reservation are ready
        '''
        print "The reservation is for hosts ", self.host_reservation
        print "Waiting 2 minutes for systems to boot"
        sleep(120)
        for resource in self.host_reservation:
            print "Checking status of " + resource
            if not self.is_system_ready(system_name=resource):
                print "INFO:", resource, "was not ready within allotted time. Removing host from reservation."
                self.host_reservation.remove(resource)
                print "INFO: attempting to allocate another machine."
                self.make_host_reservation(owner=owner, count=1, job_id=job_id, distro=distro, tags=tags)

        print "Request fulfilled."
        return

    def kickstart_machine(self, system_name, distro):
        """
        Kickstart machine with specified OS

        :param system_name:
        :param distro:
        :return:
        """
        print "INFO: fetching", system_name, "from Cobbler and setting profile"
        simplehost = self.cobbler.find_system({"hostname": system_name})[0]
        system_handle = self.cobbler.get_system_handle(simplehost, self.token)
        self.cobbler.modify_system(system_handle, "profile", self.distro[distro], self.token)
        self.cobbler.modify_system(system_handle, "netboot-enabled", 1, self.token)
        self.cobbler.save_system(system_handle, self.token)

        reboot_args = {"power": "reboot", "systems": [simplehost]}
        print "INFO: Cobbler is rebooting", system_name
        self.cobbler.background_power_system(reboot_args, self.token)
        return

    def is_system_ready(self, system_name):
        """
        Check that a given system can be reached via ssh after it is kickstarted. If it cannot be reached we will
        try another host. Mark the failed attempt in the DB as a "pxe_failed" for later cleanup. On success update the
        DB with the state of the machine. Another check is that we check for the presence of a file that was placed on
        the host prior to kickstart. If this file is present it indicated that kickstart did not happen.

        :param system_name: name of the system to check
        :return:
        """
        simplehost = self.cobbler.find_system({"hostname": system_name})[0]
        sys_ip = self.cobbler.get_system(simplehost)['interfaces']['em1']['ip_address']
        if self.check_ssh(ip=sys_ip):
            if self.check_for_file_on_target(ip=sys_ip, file_name=self.file_name):
                self.reservation_failed(system_name=system_name, state="pxe_failed")
                return False
            print "File that was created on", system_name, "before kickstart was not detected.\nKICKSTART SUCCEEDED!"
            data = json.dumps({'hostname': system_name, 'state': 'in_use'})
            print "INFO: updating", system_name, "status to in_use"
            self.host_manager.update_resource(data)
            return True
        else:
            print "INFO: updating", system_name, "status to pxe_failed"
            self.reservation_failed(system_name=system_name, state="pxe_failed")
        return False

    def reservation_failed(self, system_name, state):
        data = json.dumps({'hostname': system_name, 'owner': '', 'state': state, 'job_id': ''})
        self.host_manager.update_resource(data)

    def free_machines(self, field, value):
        """
        free machines that match given criteria by clearing owner and job_id fields

        :param field:
        :param value:
        :return:
        """
        resources = self.host_manager.find_resources(field=field, value=value)
        for resource in resources:
            system_name = resource['hostname']
            print "Freeing " + system_name
            data = json.dumps({'hostname': system_name, 'owner': '', 'state': 'idle', 'job_id': ''})
            self.host_manager.update_resource(data)
        return

    def put_file_on_target(self, ip, file_name):
        """
        SSH to a host and touch a file there. We can later check for this files existence to determine whether a
        kickstart completed successfully.

        :param ip: (string) IP address of host
        :param file_name: name of file to create
        :return:
        """
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())  # wont require saying 'yes' to new fingerprint
        ssh.connect(ip, username=self.ssh_user, password=self.ssh_password)
        ssh.exec_command('touch ' + file_name)
        ssh.close()
        return

    def check_for_file_on_target(self, ip, file_name):
        """
        SSH to a host and check for the presence of a file.

        :param ip: (string) IP of a host
        :param file_name: Name of file to check if it exists
        :return: True if the file was found
        """
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())  # wont require saying 'yes' to new fingerprint
        ssh.connect(ip, username=self.ssh_user, password=self.ssh_password)
        command = "[ -f /root/" + file_name + " ] && echo OK"
        _, stdout, _ = ssh.exec_command(command)
        if stdout.read():
            ssh.close()
            print "Found a file that should not have been on the host"
            return True
        ssh.close()
        return False

    def check_ssh(self, ip, interval=20, retries=45):
        """
        Attempt to ssh to a given host. Default is to try for 15 minutes

        :param ip: ip of host to try
        :param user: user to log in as
        :param password: user login password
        :param interval: seconds between retries
        :param retries: number of retries
        :return:
        """
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())

        for i in range(retries):
            try:
                print "Attempting ssh to " + ip + "....." + str(i+1) + "/" + str(retries)
                ssh.connect(ip, username=self.ssh_user, password=self.ssh_password)
                print "Obtained ssh connection to " + ip + "!"
                return True
            except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
                print e
                sleep(interval)
        return False

    def get_host_reservation_as_ip(self, reservation):
        """
        Will lookup IP of a given hostname in cobbler server.

        :param reservation: An array of hostnames to get IPs of
        :return: An array of IPs
        """
        reservation_ips = []
        for item in reservation:
            simplehost = self.cobbler.find_system({"hostname": item})[0]
            reservation_ips.append(self.cobbler.get_system(simplehost)['interfaces']['em1']['ip_address'])
        return reservation_ips

    def get_individual_reservation_as_ip(self, reservation):
        """
        Look up single reservation hostname and return IP from cobbler server
        :param reservation:
        :return: single IP as string
        """
        reservation_ip = None
        simplehost = self.cobbler.find_system({"hostname": reservation})[0]
        reservation_ip = self.cobbler.get_system(simplehost)['interfaces']['em1']['ip_address']
        return reservation_ip

    def make_ip_reservation(self, ip_type, job_id, number_of_ips, tags=None):
        """
        Used to make a reservation of public or private IPs.  Typically the job_id would be the jenkins job or some
        other string that would be unique to the entire reservation. This makes it easier to free the IPs associated
        with the reservation. However, an user's name can also be used*.

        *Use caution when using a user's name when freeing as that would free all for that person. If a user name is
        used for the reservation it is best practice to free those by IP address

        :param tags: Dict of tags that you want to use to filter resources
        :param ip_type: Type of IP reservation to make (public/private)
        :param job_id: job_id or owner to make the reservation for
        :param number_of_ips: how many IPs to reserve
        :return: an array of the IPs that were reserved
        """
        type_dict = {'public': self.public_ip_manager,
                     'private': self.private_ip_manager}
        reservation_dict = {'public': self.public_ip_reservation,
                            'private': self.private_ip_reservation}
        ip_manager = type_dict[ip_type]
        free_addresses = ip_manager.find_resources(field="owner", value="")
        filtered_addresses = self.filter_resources_by_tags(free_addresses, tags)
        if len(filtered_addresses) < number_of_ips:
            print "Oops...There are not enough free IPs to fill your request."
            raise UnableToFullfillRequestException()

        for i in range(number_of_ips):
            address = filtered_addresses[i]['address']
            data = json.dumps({'address': address, 'owner': job_id})
            ip_manager.update_resource(data)
            reservation_dict[ip_type].append(address)
        return reservation_dict[ip_type]

    def free_ip_reservation(self, ip_type, field="owner", value=""):
        """
        Free ip reservation. Usually you would free by owner:job_id to free all for a particular reservation. However,
        it is possible to filter on any field:value. This is useful to free individual IPs

        ex1: to free an entire reservation - field="owner", value="vic-CI-edge-23"

        ex2: to free individual ip - field="address", value="10.111.51.50"

        :param ip_type: Type of IP reservation to free (public/private)
        :param field: Field to filter on (default is owner but can also be address)
        :param value: Criteria to filter on, typically a job_id name
        :return:
        """
        type_dict = {'public': self.public_ip_manager,
                     'private': self.private_ip_manager}
        ip_type = type_dict[ip_type]
        resources = ip_type.find_resources(field=field, value=value)
        for resource in resources:
            address = resource['address']
            print "Freeing " + address
            data = json.dumps({'address': address, 'owner': ''})
            ip_type.update_resource(data)
        return

    def filter_resources_by_tags(self, resources, tags):
        """
        Filter a list of resources down to the ones that have the tags passed in

        :param resources: List of resources
        :param tags: Dict of tags to match
        :return: Filtered list of resources
        """
        if not tags:
            return resources
        matching_resources = []
        # For each resource
        for resource in resources:
            # Check that each tag is available, if so add it to the returned array
            all_tags_valid = True
            for tag in tags.keys():
                if tag not in resource['tags'] or resource['tags'][tag] != tags[tag]:
                    all_tags_valid = False
            if all_tags_valid:
                matching_resources.append(resource)
        return matching_resources

    def compare_tag(self, name, value, oper, tags):
        """
        Utility function to simplify the testing of key/value pairs in filtering
        function.
        :param name: Name of the key/value pair to compare
        :param value: Value to compare
        :param oper: what is our operation?
        :param tags: tags from the host entry in the mongodb
        :return:
        """
        # we will use a 10% fudge factor because memory is not exact
        if 'memory' in name:
            value *= .9
        if name in tags and oper(tags[name], value):
            return True
        return False

    def filter_hosts_by_tags(self, resources, tags):
        """
        Filter out the resources that meet the tag requirements. When
        comparing integers such as memory or cpucores, we will compare
        greater than or equal to (Memory is not exact when it comes to byte
        count so we test that it is greater than or equal to a close
        proximity of GB, i.e. 67258503167 is just under 64GB, and if you ask
        for 4 cpucores we will give you machines with 4 or 8.)
        :param resources: available resources from mongodb
        :param tags: tags that we are filtering against
        :return: list of dicts
        """
        matching_resources = []
        oper = operator.eq
        for r in resources:
            found = True
            for name, filters in tags.iteritems():
                if isinstance(filters, int):
                    oper = operator.ge
                if not self.compare_tag(name, value=filters,
                                        oper=oper, tags=r['tags']):
                    found = False
                    break
            if found:
                matching_resources.append(r)
        return matching_resources
