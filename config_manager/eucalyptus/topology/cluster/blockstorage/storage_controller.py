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


class Storage_Controller(BaseConfig):

    def __init__(self,
                 name,
                 hostname,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None
                 ):
        description = description or "Eucalyptus Storage Controller Host Configuration Block"
        if not hostname:
            raise ValueError('Storage Controller Hostname must be populated')
        name = name or hostname
        self.hostname = self.create_property(json_name='hostname', value=hostname)
        # Baseconfig init() will read in default values from read_file_path if it is populated.
        super(Storage_Controller, self).__init__(name=name,
                                                 description=description,
                                                 read_file_path=read_file_path,
                                                 write_file_path=write_file_path,
                                                 property_type=property_type,
                                                 version=version)
