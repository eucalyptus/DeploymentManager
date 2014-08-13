#!/usr/bin/env python

# Copyright 2009-2014 Eucalyptus Systems, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json


class Eucalyptus:
    def __init__(self):
        self.log_level = "INFO"
        self.set_bind_addr = True
        self.install_load_balancer = True
        self.install_imaging_worker = True
        self.eucalyptus_repo = "in brightest day in blackest night no evil " \
                               "shall escape my sight"
        self.euca2ools_repo = "captain planet"
        self.enterprise_repo = "energon cubes"
        self.enterprise = EnterpriseCert()
        self.node_controllers = NodeControllers()
        self.topology = Topology()
        self.network = Network()
        self.system_properties = SystemProperties()

    def add_topology(self, topology):
        self.topology = topology

    def add_network(self, network):
        self.network = network

    def add_system_properties(self, system_properties):
        self.system_properties = system_properties

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


class SystemProperties:
    def __init__(self, properties=None):
        self.system_properties = {}
        if properties:
            self.system_properties = properties

    def add_property(self, key, value):
        self.system_properties.update({key: value})

    def to_dict(self):
        return self.system_properties


class Network:
    def __init__(self, network_json_file=None, network_json=None):
        self.network = {}

    def to_dict(self):
        return self.network


class Topology:
    def __init__(self):
        self.clc = None
        self.walrus = "10.111.1.101"
        self.user_facing = ["10.111.1.101", "10.111.1.102"]
        self.clusters = {}

    def add_cluster(self, clusters):
        for cluster in clusters:
            mycluster = cluster.to_dict()
            self.clusters.update(mycluster)

    def add_cloud_controller(self, clc):
        self.clc = clc

    def to_dict(self):
        return {'clc-1': self.clc.hostname,
                'walrus': self.walrus,
                'user-facing': self.user_facing,
                'clusters': self.clusters}


class Walrus:
    def __init__(self, hostname):
        self.hostname = hostname


class CloudController:
    def __init__(self, hostname):
        self.hostname = hostname


class Cluster(object):
    def __init__(self, name, cc_hostname=None, sc_hostname=None):
        self.name = name
        self.cc_hostname = cc_hostname
        self.sc_hostname = sc_hostname

    def to_dict(self):
        return {
            self.name: {
                'cc-1': self.cc_hostname,
                'sc-1': self.sc_hostname
            }
        }


class EnterpriseCert:
    def __init__(self):
        self.clientcert = "much cert"
        self.clientkey = "such key"

    def to_dict(self):
        return {'clientcert': self.clientcert,
                'clientkey': self.clientkey}


class DefaultAtrributes:
    def __init__(self):
        self.eucalyptus = Eucalyptus()

    def add_eucalyptus(self, eucalyptus):
        self.eucalyptus = eucalyptus

    def to_dict(self):
        return dict(eucalyptus=self.eucalyptus)


class NodeControllers:
    def __init__(self):
        self.max_cores = 8
        self.cache_size = 40000

    def to_dict(self):
        return {'max-cores': self.max_cores,
                'cache-size': self.cache_size}


class MidoNet:
    def __init__(self):
        self.name = "MidoNet"

    def to_dict(self):
        return {}


class Config:
    def __init__(self):
        self.name = "my-config"
        self.description = "my such config"
        self.default_attributes = {}

    def add_midonet(self, midonet):
        self.default_attributes.update({'midonet': midonet})

    def add_eucalyptus(self, eucalyptus):
        self.default_attributes.update({'eucalyptus': eucalyptus})

    def to_dict(self):
        return dict(name=self.name,
                    description=self.description,
                    default_attributes=self.default_attributes)


class DMJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)

