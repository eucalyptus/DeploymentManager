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
import socket
import xmlrpclib
import json

from time import sleep
from paramiko import BadHostKeyException, AuthenticationException, SSHException, SSHClient, AutoAddPolicy


class PxeManager(object):
    def __init__(self, cobbler_url, cobbler_user, cobbler_password, resource_manager_client):
        self.cobbler = xmlrpclib.Server(cobbler_url)
        self.token = self.cobbler.login(cobbler_user, cobbler_password)
        self.resource_manager = resource_manager_client
        self.distro = {'esxi51': 'qa-vmwareesxi51u0-x86_64',
                       'esxi50': 'qa-vmwareesxi50u1-x86_64',
                       'centos': 'qa-centos6-x86_64-striped-drives',
                       'rhel': 'qa-rhel6u5-x86_64-striped-drives'}
        self.reservation = []

    def get_resource(self, owner, count, job_id, distro):
        """
        Get machines from machine pool
        :param owner: who the reservation is for
        :param count: how many machines to reserve
        :param job_id: unique identifier for the reservation
        :param distro: what OS to install (see the global dict "distro" for valid options)
        :return:
        """
        resources = self.resource_manager.find_resources(field="state", value="idle")['_items']
        if len(resources) < count:
            print "Oops...There are not enough free resources to fill your request."
            return

        for i in range(count):
            hostname = resources[i]['hostname']
            data = json.dumps({'hostname': hostname, 'owner': owner, 'state': 'pxe', 'job_id': job_id})
            self.resource_manager.update_resource(data)
            print "kickstarting host: " + hostname
            self.reservation.append(hostname)
            self.kickstart_machine(system_name=hostname, distro=distro)

        '''
        Check that the resources in the reservation are ready
        '''
        print "Waiting 2 minutes for systems to boot"
        sleep(120)
        for resource in self.reservation:
            print "Checking status of " + resource
            if not self.is_system_ready(system_name=resource):
                print "Host was not ready within allotted time. Attempting to allocate another machine."
                self.reservation.remove(resource)
                self.get_resource(owner=owner, count=1, job_id=job_id, distro=distro)

        print "Request fulfilled."
        return

    def kickstart_machine(self, system_name, distro):
        """
        Kickstart machine with specified OS

        :param system_name:
        :param distro:
        :return:
        """
        system_handle = self.cobbler.get_system_handle(system_name, self.token)
        self.cobbler.modify_system(system_handle, "profile", self.distro[distro], self.token)
        self.cobbler.modify_system(system_handle, "netboot-enabled", 1, self.token)
        self.cobbler.save_system(system_handle, self.token)

        reboot_args = {"power": "reboot", "systems": [system_name]}
        self.cobbler.background_power_system(reboot_args, self.token)
        return

    def is_system_ready(self, system_name):
        sys_ip = self.cobbler.get_system(system_name)['interfaces']['eth0']['ip_address']
        if self.check_ssh(ip=sys_ip):
            data = json.dumps({'hostname': system_name, 'state': 'in_use'})
            self.resource_manager.update_resource(data)
            return True
        else:
            data = json.dumps({'hostname': system_name, 'owner': '', 'state': 'pxe_failed', 'job_id': ''})
            self.resource_manager.update_resource(data)
        return False

    def free_machines(self, field, value):
        """
        free machines that match given criteria by clearing owner and job_id fields

        :param field:
        :param value:
        :return:
        """
        resources = self.resource_manager.find_resources(field=field, value=value)['_items']
        for resource in resources:
            system_name = resource['hostname']
            print "Freeing " + system_name
            data = json.dumps({'hostname': system_name, 'owner': '', 'state': 'idle', 'job_id': ''})
            self.resource_manager.update_resource(data)
        return

    def check_ssh(self, ip, user="root", password="foobar", interval=20, retries=45):
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
                ssh.connect(ip, username=user, password=password)
                print "Obtained ssh connection to " + ip + "!"
                return True
            except (BadHostKeyException, AuthenticationException, SSHException, socket.error) as e:
                print e
                sleep(interval)
        return False

    def get_reservation_as_ip(self, reservation):
        reservation_ips = []
        for item in reservation:
            reservation_ips.append(self.cobbler.get_system(item)['interfaces']['eth0']['ip_address'])
        return reservation_ips


