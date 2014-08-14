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

import xmlrpclib
import json
from resource_manager.client import ResourceManagerClient

class PxeManager(object):
    def __init__(self):
        self.cobbler = xmlrpclib.Server("http://cobbler.com/cobbler_api")
        self.token = self.cobbler.login("***", "***")

        self.resource_manager = ResourceManagerClient()

        self.distro = {'esxi51': 'qa-vmwareesxi51u0-x86_64',
                'esxi50': 'qa-vmwareesxi50u1-x86_64',
                'centos': 'qa-centos6-x86_64-striped-drives',
                'rhel': 'qa-rhel6u5-x86_64-striped-drives'}

    def get_resource(self, owner, count, job_id, distro):
        """
        Get machines from machine pool
        :param owner: who the reservation is for
        :param count: how many machines to reserve
        :param job_id: unique identifier for the reservation
        :param distro: what OS to install (see the global dict "distro" for valid options)
        :return:
        """
        resources = self.resource_manager.find_resource(field="state", value="idle")
        for i in range(count):
            data = json.dumps({'hostname': resources[i]['hostname'], 'owner': owner, 'state': 'pxe', 'job_id': job_id})
            self.resource_manager.update_resource(data)
            print "kickstarting host: " + resources[i]['hostname']
            self.kickstart_machine(system_name=resources[i]['hostname'], distro=distro)
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

        '''
        TODO: ssh polling here

        If ssh success then update DB otherwise retry
            data = json.dumps({'hostname': system_name, 'state': 'in_use'})
            self.resource_manager.update_resource(data)
        '''
        return

    def free_machines(self, field, value):
        """
        free machines that match given criteria by clearing owner and job_id fields

        :param field:
        :param value:
        :return:
        """
        resources = self.resource_manager.find_resource(field=field, value=value)
        for resource in resources:
            system_name = resource['hostname']
            print "Freeing " + system_name
            data = json.dumps({'hostname': system_name, 'owner': '', 'state': 'idle', 'job_id': ''})
            self.resource_manager.update_resource(data)
        return