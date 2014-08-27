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
import socket
import copy


class Network(BaseConfig):
    def __init__(self,
                 public_ips,
                 private_ips,
                 name=None,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 network_type=None):

        self.public_ips = self.create_property('public_ips',
                                               value=public_ips,
                                               validate_callback=self.validate_publicips)
        self.private_ips = self.create_property('private_ips',
                                                value=private_ips,
                                                validate_callback=self.validate_privateips)

        super(Network, self).__init__(name=name,
                                      description=None,
                                      read_file_path=None,
                                      write_file_path=None,
                                      property_type=property_type,
                                      version=None)

    def validate_privateips(self, privateips):
        return self.validate_ip_strings(privateips)

    def validate_publicips(self, publicips):
        return self.validate_ip_strings(publicips)

    def validate_ip_strings(self, iplist):
        if iplist is None or iplist == []:
            return iplist
        if not isinstance(iplist, list):
            iplist = [iplist]
        for item in iplist:
            ips = str(item).split('-')
            # Validate any ips passed
            for ip in ips:
                try:
                    socket.inet_aton(ip)
                except socket.error as se:
                    se.args = ('{0}: "{1}"'.format(se.args[0], ip),) + se.args[1:]
                    raise se

        return iplist

    def add_public_ip_entry(self, public_ip_entry):
        public_ip_list = copy.copy(self.public_ips.value)
        if not public_ip_entry:
            raise ValueError('Bad public ip:"{0}" pass to add_public_ip_entry'
                             .format(public_ip_entry))
        for ip_entry in str(public_ip_entry).split(','):
            newips = str(ip_entry).split('-')
            self.validate_ip_strings(newips)
            for entry in self.public_ips.value:
                entry_ips = entry.split('-')
                if len(entry_ips) == 1:
                    if len(newips) == 1:
                        newips.append(newips[0])
                    if self.is_ip_in_range(entry_ips[0], newips[0], newips[1]):
                        raise ValueError('New Public IP entry:"{0}" conflicts with existing '
                                         'entry:"{1}"'
                                         .format(ip_entry, entry))
                else:
                    for ip in newips:
                        if self.is_ip_in_range(ip, entry_ips[0], entry_ips[1]):
                            raise ValueError('New Public IP entry:"{0}" conflicts with existing '
                                             'entry range:"{1}"'
                                             .format(ip_entry, entry))
            public_ip_list.append(ip_entry)
        self.public_ips.value = public_ip_list

    def add_private_ip_entry(self, private_ip_entry):
        private_ip_list = copy.copy(self.private_ips.value)
        if not private_ip_entry:
            raise ValueError('Bad private ip:"{0}" pass to add_private_ip_entry'
                             .format(private_ip_entry))
        for ip_entry in str(private_ip_entry).split(','):
            newips = str(ip_entry).split('-')
            self.validate_ip_strings(newips)
            for entry in self.private_ips.value:
                entry_ips = entry.split('-')
                if len(entry_ips) == 1:
                    entry_ips.append(entry_ips[0])
                for ip in newips:
                    if self.is_ip_in_range(ip, entry_ips[0], entry_ips[1]):
                        raise ValueError('New Private IP entry:"{0}" conflicts with existing '
                                         'entry:"{1}"'
                                         .format(ip_entry, entry))
            private_ip_list.append(ip_entry)
        self.public_ips.value = private_ip_list

    def is_ip_in_range(self, ip, range_start, range_end):
        self.validate_ip_strings([ip, range_start, range_end])
        if ip == range_start or ip == range_end:
            return True
        ip_octs = ip.split('.')
        rangestart_octs = range_start.split('.')
        rangeend_octs = range_end.split('.')
        for x in xrange(0, len(rangestart_octs)):
            if rangestart_octs[x] > ip_octs[x]:
                return False
            elif rangestart_octs[x] < ip_octs[x]:
                for y in xrange(0, len(rangeend_octs)):
                    if rangeend_octs[y] < ip_octs[y]:
                        return False
                return True
        return False
