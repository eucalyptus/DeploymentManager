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

from config_manager.machine_config import Machine_Config
from config_manager.eucalyptus.euca_conf_file import Euca_Conf_File

class Euca_Machine(Machine_Config):
    def __init__(self,
                 hostname,
                 name=None,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None):

        self._eucalyptus_conf = self.create_property(json_name='eucalyptus_conf',
                                                     value=Euca_Conf_File())

        super(Euca_Machine, self).__init__(hostname=hostname,
                                             name=name,
                                             description=description,
                                             read_file_path=read_file_path,
                                             write_file_path=write_file_path,
                                             property_type=property_type,
                                             version=version)


    @property
    def eucalyptus_conf(self):
        return self._eucalyptus_conf.value
