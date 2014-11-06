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


class NodeController(BaseConfig):
    def __init__(self,
                 name,
                 hypervisor,
                 read_file_path=None,
                 write_file_path=None,
                 description=None,
                 version=None):
        description = description or "Eucalyptus Node Controller Configuration Block"
        self.hypervisor = self.create_property('hypervisor', value=hypervisor)
        # Use validator to make the hypervisor name read-only
        self.hypervisor.validate = lambda x: self.hypervisor.value
        super(NodeController, self).__init__(name=name,
                                             description=description,
                                             write_file_path=write_file_path,
                                             read_file_path=read_file_path,
                                             version=version)
        self.max_cores = self.create_property('max-cores')
        self.cache_size = self.create_property('cache-size')
        self.operating_system = self.create_property('operating-system')
