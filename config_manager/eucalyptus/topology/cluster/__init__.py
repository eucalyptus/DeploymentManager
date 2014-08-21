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
from config_manager.namespace import Namespace
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
        self.eucalyptus_properties.create_property(
            name='addressespernetwork',
            property_string=str(name) + '.cluster.addressespernetwork',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxnetworkindex',
            property_string=str(name) + '.cluster.maxnetworkindex',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxnetworktag',
            property_string=str(name) + '.cluster.maxnetworktag',
            value=None)
        self.eucalyptus_properties.create_property(
            name='minnetworkindex',
            property_string=str(name) + '.cluster.minnetworkindex',
            value=None)
        self.eucalyptus_properties.create_property(
            name='minnetworktag',
            property_string=str(name) + '.cluster.minnetworktag',
            value=None)
        self.eucalyptus_properties.create_property(
            name='networkmode',
            property_string=str(name) + '.cluster.networkmode',
            value=None)
        self.eucalyptus_properties.create_property(
            name='sourcehostname',
            property_string=str(name) + '.cluster.sourcehostname',
            value=None)
        self.eucalyptus_properties.create_property(
            name='usenetworktags',
            property_string=str(name) + '.cluster.usenetworktags',
            value=None)
        self.eucalyptus_properties.create_property(
            name='vnetnetmask',
            property_string=str(name) + '.cluster.vnetnetmask',
            value=None)
        self.eucalyptus_properties.create_property(
            name='vnetsubnet',
            property_string=str(name) + '.cluster.vnetsubnet',
            value=None)
        self.eucalyptus_properties.create_property(
            name='vnettype',
            property_string=str(name) + '.cluster.vnettype',
            value=None)

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
