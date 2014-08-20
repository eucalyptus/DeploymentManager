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


class Enterprise(BaseConfig):
    def __init__(self, name=None):
        super(Enterprise, self).__init__(name=name,
                                         description=None,
                                         write_file_path=None,
                                         read_file_path=None,
                                         version=None)
        self.clientcert = self.create_property('clientcert')
        self.clientkey = self.create_property('clientkey')

    def set_credentials(self, clientcert=None, clientkey=None):
        self.clientcert.value = clientcert
        self.clientkey.value = clientkey
