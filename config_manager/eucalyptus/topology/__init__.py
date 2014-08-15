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
from config_manager.eucalyptus.topology.cluster import Cluster
from config_manager.eucalyptus.topology.cloud_controller import CloudController
from config_manager.eucalyptus.topology.walrus import Walrus
from config_manager.eucalyptus.topology.ufs import UserFacingServices


class Topology(BaseConfig):
    def __init__(self, name=None):
        super(Topology, self).__init__(name=name,
                                       description=None,
                                       write_file_path=None,
                                       read_file_path=None,
                                       version=None)

        self.cloud_controllers_property = \
            self.create_property('cloud_controller')
        self.walrus_property = self.create_property('walrus')
        self.user_facing_services_property = \
            self.create_property('user_facing')
        self.clusters_property = self.create_property('clusters', value=[])

    def add_clusters(self, clusters):
        if not clusters:
            raise ValueError('add_clusters provided empty value: "{0}"'
                             .format(clusters))
        if not isinstance(clusters, list):
            clusters = [clusters]
        for cluster in clusters:
            assert isinstance(cluster, Cluster), 'add clusters passed non ' \
                                                 'cluster type, cluster:"{0}"'\
                                                 .format(cluster)
            self.clusters_property.value.append(cluster)

    def create_cluster(self, name, cc_hostname=None, sc_hostname=None):
        cluster = Cluster(name,
                          cc_hostname=cc_hostname,
                          sc_hostname=sc_hostname)
        self.add_clusters(cluster)

    def get_cluster(self, clustername):
        clusters = self.clusters_property.get()
        for cluster in clusters:
            if cluster.name == clustername:
                return cluster
        return None


    def delete_cluster(self, clustername):
        cluster = self.get_cluster(clustername)
        if cluster:
            clusters = self.clusters_property.get()
            clusters.remove(cluster)
            self.clusters_property.update()


    def add_cloud_controllers(self, clcs):
        if clcs is None:
            raise ValueError('add_cloud_controllers provided empty '
                             'value: "{0}"'.format(clcs))
        if not isinstance(clcs, list):
            clcs = [clcs]
        if self.cloud_controllers_property is None:
            self.cloud_controllers_property = []
        for clc in clcs:
            self.cloud_controllers_property.get().append(clc)

    def add_walrus(self, walrus):
        self.walrus = walrus

    def add_user_facing_services(self, ufs):
        self.user_facing = ufs

    def to_dict(self):
        return {'clc-1': self.cloud_controller.hostname,
                'walrus': self.walrus.hostname,
                'user-facing': self.user_facing.hostnames,
                'clusters': self.clusters}
