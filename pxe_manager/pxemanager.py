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

    def get_machines(self, owner, count, job_id, distro):
        os = self.distro[distro]
        for i in range(count):
            '''
            TODO: query DB update DB, kickstart
            '''
            # system_name = self.resource_manager.get_resource(state="idle")
            # self.resource_manager.update_resource(owner=owner, job_id= job_id, state="PXE")
            # print "kickstarting host: " + self.cobbler.find_system({"name": system_name})
            # self.kickstart_machine(system_name=system_name, distro=os)
        return

    def kickstart_machine(self, system_name, distro):
        """
        Kickstart machine with specified OS

        :param system_name:
        :param distro:
        :return:
        """
        system_handle = self.cobbler.get_system_handle(system_name, self.token)
        self.cobbler.modify_system(system_handle, "profile", distro, self.token)
        self.cobbler.modify_system(system_handle, "netboot-enabled", 1, self.token)
        self.cobbler.save_system(system_handle, self.token)

        reboot_args = {"power": "reboot", "systems": [system_name]}
        self.cobbler.background_power_system(reboot_args, self.token)

        '''
        TODO: ssh polling here
        '''
        return

    def free_machines(self, job_id):
        '''

        :param job_id:
        :return:
        '''
        '''
        TODO: free machines associated with job id by clearing owner and job_id fields
        '''
        print "Not yet implemented"
        return