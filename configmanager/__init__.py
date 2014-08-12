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


class DeploymentManager(object):
    def __init__(self):
        print "none"


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
                'topology': self.topology}


class Topology:
    def __init__(self):
        self.clc = "10.111.1.101"
        self.walrus = "10.111.1.101"
        self.user_facing = ["10.111.1.101", "10.111.1.102"]
        self.clusters = Clusters()

    def to_dict(self):
        return {'clc-1': self.clc,
                'walrus': self.walrus,
                'user-facing': self.user_facing,
                'clusters': self.clusters}

class Clusters:
    def __init__(self):
        self.clusters = {}

    def add_cluster(self, cluster):
        self.clusters.update()

    def to_dict(self):
        return {}


class Cluster(object):
    def __init__(self, name):
        self.name = name
    


class EnterpriseCert:
    def __init__(self):
        self.clientcert = "much cert"
        self.clientkey = "such key"

    def to_dict(self):
        return {'clientcert': self.clientcert,
                'clientkey': self.clientkey}

class Atrributes:
    def __init__(self):
        self.eucalyptus = Eucalyptus()

    def to_dict(self):
        return dict(eucalyptus=self.eucalyptus)


class NodeControllers:
    def __init__(self):
        self.max_cores = 8
        self.cache_size = 40000

    def to_dict(self):
        return {'max-cores': self.max_cores,
                'cache-size': self.cache_size}


class Config:
    def __init__(self):
        self.name = "my-config"
        self.description = "my such config"
        self.default_attributes = Atrributes()

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

