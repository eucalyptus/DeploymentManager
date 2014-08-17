#!/usr/bin/env python

# Copyright 2009-2014 Eucalyptus Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from config_manager.baseconfig import BaseConfig

# from config_manager.eucalyptus.network import Network
# from config_manager.eucalyptus.system_properties import SystemProperties


class Eucalyptus(BaseConfig):
    def __init__(self):
        super(Eucalyptus, self).__init__(name=None,
                                         description=None,
                                         write_file_path=None,
                                         read_file_path=None,
                                         version=None)
        self.create_property(json_name='log-level')
        self.create_property('set_bind_addr', value=True)
        self.create_property('install_load_balancer', value=True)
        self.create_property('install_imaging_worker', value=True)
        self.create_property('eucalyptus_repo')
        self.create_property('euca2ools_repo')
        self.create_property('enterprise_repo')
        self.create_property('enterprise')
        self.create_property('node_controllers')
        self.create_property('topology')
        self.create_property('network')
        self.create_property('system_properties')

    def set_log_level(self, log_level):
        self.log_level = log_level

    def add_topology(self, topology):
        self.topology = topology

    def add_network(self, network_config):
        self.network = network_config

    def add_system_properties(self, sys_property):
        self.system_properties = sys_property

    def add_enterprise_credentials(self, enterprise_creds):
        self.enterprise = enterprise_creds

    def add_packages(self, packages):
        self.eucalyptus_repo = packages.eucalyptus_repo
        self.euca2ools_repo = packages.euca2ools_repo

    def to_dict(self):
        return {'log-level': self.log_level,
                'set-bind-addr': self.set_bind_addr,
                'install-load-balancer': self.install_load_balancer,
                'install-imaging-worker': self.install_imaging_worker,
                'eucalyptus-repo': self.eucalyptus_repo,
                'euca2ools-repo': self.euca2ools_repo,
                'enterprise-repo': self.enterprise_repo,
                'enterprise': self.enterprise,
                'nc': self.node_controllers,
                'topology': self.topology,
                'network': self.network,
                'system_properties': self.system_properties}
