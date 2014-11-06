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


class ClusterController(BaseConfig):

    def __init__(self,
                 hostname,
                 name=None,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 network_type=None):
        name = name or hostname
        self.hostname = self.create_property('hostname', value=hostname)
        self.network_type = self.create_property(json_name='network_type',
                                                 value=network_type)
        self.bridge_interface = self.create_property(json_name='bridge_interface',
                                                     value=None)
        self.log_level = self.create_property(json_name='log_level',
                                              value=None)
        super(ClusterController, self).__init__(name=name,
                                                description=None,
                                                read_file_path=None,
                                                write_file_path=None,
                                                property_type=property_type,
                                                version=None)
