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
import config_manager.eucalyptus.topology.cluster.blockstorage
from config_manager.eucalyptus.topology.cluster.clustercontroller import ClusterController
from config_manager.eucalyptus.topology.cluster.nodecontroller import NodeController
from config_manager.eucalyptus.topology.cluster.nodecontroller.hyperv import Hyperv
from config_manager.eucalyptus.topology.cluster.nodecontroller.kvm import Kvm
from config_manager.eucalyptus.topology.cluster.nodecontroller.xen import Xen
from config_manager.eucalyptus.topology.cluster.nodecontroller.esxi import Esxi
from config_manager.eucalyptus.topology.cluster.nodecontroller.vsphere import Vsphere

_HYPERVISORS = {
    str(Esxi.__name__).lower(): Esxi,
    str(Hyperv.__name__).lower(): Hyperv,
    str(Kvm.__name__).lower(): Kvm,
    str(Vsphere.__name__).lower(): Vsphere,
    str(Xen.__name__).lower(): Xen}


class Cluster(BaseConfig):
    def __init__(self,
                 name,
                 hypervisor=None,
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
        self.hypervisor_type = self.create_property(
            'hypervisor_type', value=hypervisor, validate_callback=self.validate_hypervisor_type)

        # Baseconfig init() will read in default values from read_file_path if it is populated.
        super(Cluster, self).__init__(name=name,
                                      description=description,
                                      read_file_path=read_file_path,
                                      write_file_path=write_file_path,
                                      property_type=property_type,
                                      version=version)

    def add_block_storage(self, block_storage):
        assert isinstance(block_storage, BlockStorage), 'Cant add non block_storage type:{0}'\
            .format(type(block_storage))
        if self.block_storage.value:
            raise ValueError('Delete existing block storage before adding another')
        self.block_storage.value = block_storage

    def create_block_storage(self, backend_type, name=None, read_file_path=None):
        name = name or self.name.value + "_block_storage"
        block_storage = BlockStorage(name=name, cluster_name=self.name,
                                     backend_type=backend_type, read_file_path=read_file_path)
        self.add_block_storage(block_storage)
        return block_storage

    def delete_block_storage(self):
        self.block_storage.value = None

    def validate_hypervisor_type(self, hypervisor):
        try:
            if hypervisor is not None:
                _HYPERVISORS[str(hypervisor).lower()]
        except KeyError:
            hlist = ""
            for key in _HYPERVISORS:
                hlist += "{0}, ".format(key)
            raise ValueError('Unknown hypervisor type:"{0}". Possible types:"{1}"'
                             .format(hypervisor, hlist.rstrip(', ')))
        if not self.nodes.value:
            return hypervisor
        if hypervisor == self.hypervisor_type.value:
            return hypervisor
        for node in self.nodes.value:
            if node.hypervisor != hypervisor:
                raise ValueError('Must delete all nodes if changing hypervisor type')
        return hypervisor

    def add_nodes(self, nodes):
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            if not isinstance(node, NodeController):
                raise ValueError('Could not add obj of non-NodeController type:{0}, obj:{1}'
                                 .format(type(node), node))
            if node.hypervisor.value != self.hypervisor_type.value:
                raise ValueError('Node hypervisor type:"{0}" does not match clusters:"{1}"'
                                 .format(node.hypervisor.value, self.hypervisor_type))
            if self.get_node(node.name):
                raise ValueError('Node with name:"{0}" already exists in cluster'.format(node.name))
            self.nodes.value.append(node)

    def get_node(self, name):
        for node in self.nodes.value:
            if node.name.value == name:
                return node
        return None

    def create_node(self, ip, read_file_path=None, write_file_path=None,
                    description=None, version=None):
        if not self.hypervisor_type.value:
            raise ValueError('Must set "hypervisor_type" in cluster before adding nodes')
        node_class = _HYPERVISORS[self.hypervisor_type.value]
        new_node = node_class(name=ip,
                              read_file_path=read_file_path,
                              write_file_path=write_file_path,
                              description=description,
                              version=version)
        self.add_nodes(new_node)
        return new_node
