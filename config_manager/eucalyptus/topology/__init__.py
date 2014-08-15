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


class Topology(BaseConfig):
    def __init__(self, name=None):
        super(Topology, self).__init__(name=name,
                                       description=None,
                                       config_file_path=None,
                                       version=None)

        self.cloud_controller = None
        self.walrus = None
        self.user_facing = None
        self.clusters = self.create_prop('clusters', value=[])

    def add_cluster(self, clusters):
        for cluster in clusters:
            mycluster = cluster.to_dict()
            self.clusters.update(mycluster)

    def add_cloud_controller(self, clc):
        self.cloud_controller = clc

    def add_walrus(self, walrus):
        self.walrus = walrus

    def add_user_facing_services(self, ufs):
        self.user_facing = ufs

    def to_dict(self):
        return {'clc-1': self.cloud_controller.hostname,
                'walrus': self.walrus.hostname,
                'user-facing': self.user_facing.hostnames,
                'clusters': self.clusters}
