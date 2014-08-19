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

from config_manager.baseconfig import BaseConfig, EucalyptusProperty
import copy


class Eucalyptus(BaseConfig):
    def __init__(self):
        super(Eucalyptus, self).__init__(name=None,
                                         description=None,
                                         write_file_path=None,
                                         read_file_path=None,
                                         version=None)
        self.log_level = self.create_property(json_name='log-level')
        self.set_bind_addr = self.create_property('set_bind_addr', value=True)
        self.eucalyptus_repo = self.create_property('eucalyptus-repo')
        self.euca2ools_repo = self.create_property('euca2ools-repo')
        self.enterprise_repo = self.create_property('enterprise-repo')
        self.enterprise = self.create_property('enterprise')
        self.nc = self.create_property('nc')
        self.topology = self.create_property('topology')
        self.network = self.create_property('network')
        self.system_properties = self.create_property('system_properties')
        self.install_load_balancer = self.create_property(
            'install-load-balancer', value=True)
        self.install_imaging_worker = self.create_property('install-imaging-worker', value=True)
        self.use_dns_delegation = self._set_eucalyptus_property(
            name='bootstrap.webservices.use_dns_delegation', value=True)

    def _process_json_output(self, json_dict, show_all=False, **kwargs):
        tempdict = copy.copy(json_dict)
        eucaprops = {}
        aggdict = self._aggregate_eucalyptus_properties()
        for key in aggdict:
            value = aggdict[key]
            # todo handle value of 'False' as valid
            if not value and show_all:
                eucaprops["!" + str(key)] = aggdict[key]
            elif value:
                eucaprops[key] = aggdict[key]
        if eucaprops:
            if not 'eucalyptus_properties' in tempdict:
                tempdict['eucalyptus_properties'] = aggdict
            else:
                tempdict['eucalyptus_properties'].update(aggdict)
        return super(Eucalyptus, self)._process_json_output(json_dict=tempdict,
                                                            show_all=show_all,
                                                            **kwargs)

    def add_topology(self, topology):
        self.topology.value = topology

    def set_log_level(self, log_level):
        self.log_level.value = log_level
