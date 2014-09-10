#!/usr/bin/env python
# coding=utf-8

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
from config_manager.eucalyptus.topology.network.managed_network_config \
    import Managed_Network_Config


class Managed_Novlan_Network_Config(Managed_Network_Config):
    _network_mode_string = 'MANAGED_NOVLAN'
    def __init__(self,
                 subnet=None,
                 public_ips=None,
                 name=None,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 network_type=None):

        super(Managed_Novlan_Network_Config, self).__init__(subnet=subnet,
                                                            public_ips=public_ips,
                                                            name=name,
                                                            description=description,
                                                            read_file_path=read_file_path,
                                                            write_file_path=write_file_path,
                                                            property_type=property_type,
                                                            version=version,
                                                            network_type=network_type)
