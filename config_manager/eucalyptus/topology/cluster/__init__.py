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
from config_manager.eucalyptus.topology.cluster.blockstorage import BlockStorage
from config_manager.eucalyptus.topology.cluster.clustercontroller import ClusterController
from config_manager.eucalyptus.topology.cluster.nodecontroller import NodeController


import copy


class Cluster(BaseConfig):
    def __init__(self,
                 name,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None
                 ):
        # Create the Eucalyptus software specific properties
        self.addressespernetwork = self._set_eucalyptus_property(
            str(name) + '.cluster.addressespernetwork', value='')
        self.maxnetworkindex = self._set_eucalyptus_property(
            str(name) + '.cluster.maxnetworkindex', value='')
        self.maxnetworktag = self._set_eucalyptus_property(
            str(name) + '.cluster.maxnetworktag', value='')
        self.minnetworkindex = self._set_eucalyptus_property(
            str(name) + '.cluster.minnetworkindex', value='')
        self.minnetworktag = self._set_eucalyptus_property(
            str(name) + '.cluster.minnetworktag', value='')
        self.networkmode = self._set_eucalyptus_property(
            str(name) + '.cluster.networkmode', value='')
        self.sourcehostname = self._set_eucalyptus_property(
            str(name) + '.cluster.sourcehostname', value='')
        self.usenetworktags = self._set_eucalyptus_property(
            str(name) + '.cluster.usenetworktags', value='')
        self.vnetnetmask = self._set_eucalyptus_property(
            str(name) + '.cluster.vnetnetmask', value='')
        self.vnetsubnet = self._set_eucalyptus_property(
            str(name) + '.cluster.vnetsubnet', value='')
        self.vnettype = self._set_eucalyptus_property(
            str(name) + '.cluster.vnettype', value='')

        # Create storage and cluster controller configuration (blocks) properties
        self.block_storage = self.create_property('block_storage', value=None)
        self.network = self.create_property('network', value=None)
        self.cluster_controllers = self.create_property('cluster_controllers', value=None)
        self.vmware_brokers = self.create_property('vmware_brokers', value=None)
        self.nodes = self.create_property('nodes', value=[])

        # Baseconfig init() will read in default values from read_file_path if it is populated.
        super(Cluster, self).__init__(name=name,
                                      description=description,
                                      read_file_path=read_file_path,
                                      write_file_path=write_file_path,
                                      property_type=property_type,
                                      version=version)
