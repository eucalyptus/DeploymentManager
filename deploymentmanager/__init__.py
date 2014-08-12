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

    def to_dict(self):
        return {'log-level': self.log_level,
                'set-bind-addr': self.set_bind_addr,
                'install-load-balancer': self.install_load_balancer,
                'install-imaging-worker': self.install_imaging_worker,
                'eucalyptus-repo': self.eucalyptus_repo,
                'euca2ools-repo': self.euca2ools_repo,
                'enterprise-repo': self.enterprise_repo}


class Atrributes:
    def __init__(self):
        self.eucalyptus = Eucalyptus()

    def to_dict(self):
        return dict(eucalyptus=self.eucalyptus)


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

