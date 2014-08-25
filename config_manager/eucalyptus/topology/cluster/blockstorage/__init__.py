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
from config_manager.eucalyptus.topology.cluster.blockstorage.storage_controller import \
    Storage_Controller
import config_manager.eucalyptus.topology.cluster.blockstorage.storage_backends
from storage_backends.ceph import Ceph
from storage_backends.das import Das
from storage_backends.emc import Emc
from storage_backends.equalogic import Equalogic
from storage_backends.netapp import Netapp
from storage_backends.overlay import Overlay

_STORAGE_BACKENDS = {str(Ceph.__name__).lower(): Ceph,
                     str(Das.__name__).lower(): Das,
                     str(Emc.__name__).lower(): Emc,
                     str(Equalogic.__name__).lower(): Equalogic,
                     str(Netapp.__name__).lower(): Netapp,
                     str(Overlay.__name__).lower(): Overlay}


class BlockStorage(BaseConfig):
    def __init__(self,
                 name,
                 cluster_name,
                 backend_type,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 storage_controllers=None,
                 storage_backend=None):

        # Create the Eucalyptus software specific properties
        self.eucalyptus_properties.create_property(
            name='blockstoragemanager',
            property_string=str(cluster_name) + '.storage.blockstoragemanager',
            value=None)
        self.eucalyptus_properties.create_property(
            name='chapuser',
            property_string=str(cluster_name) + '.storage.chapuser',
            value=None)
        self.eucalyptus_properties.create_property(
            name='dasdevice',
            property_string=str(cluster_name) + '.storage.dasdevice',
            value=None)
        self.eucalyptus_properties.create_property(
            name='deletedvolexpiration',
            property_string=str(cluster_name) + '.storage.deletedvolexpiration',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxconcurrentsnapshotuploads',
            property_string=str(cluster_name) + '.storage.maxconcurrentsnapshotuploads',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxsnapshotpartsqueuesize',
            property_string=str(cluster_name) + '.storage.maxsnapshotpartsqueuesize',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxsnaptransferretries',
            property_string=str(cluster_name) + '.storage.maxsnaptransferretries',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxtotalvolumesizeingb',
            property_string=str(cluster_name) + '.storage.maxtotalvolumesizeingb',
            value=None)
        self.eucalyptus_properties.create_property(
            name='maxvolumesizeingb',
            property_string=str(cluster_name) + '.storage.maxvolumesizeingb',
            value=None)
        self.eucalyptus_properties.create_property(
            name='multihostaccess',
            property_string=str(cluster_name) + '.storage.multihostaccess',
            value=None)
        self.eucalyptus_properties.create_property(
            name='ncpaths',
            property_string=str(cluster_name) + '.storage.ncpaths',
            value=None)
        self.eucalyptus_properties.create_property(
            name='poolname',
            property_string=str(cluster_name) + '.storage.poolname',
            value=None)
        self.eucalyptus_properties.create_property(
            name='resourceprefix',
            property_string=str(cluster_name) + '.storage.resourceprefix',
            value=None)
        self.eucalyptus_properties.create_property(
            name='resourcesuffix',
            property_string=str(cluster_name) + '.storage.resourcesuffix',
            value=None)
        self.eucalyptus_properties.create_property(
            name='sanhost',
            property_string=str(cluster_name) + '.storage.sanhost',
            value=None)
        self.eucalyptus_properties.create_property(
            name='sanpassword',
            property_string=str(cluster_name) + '.storage.sanpassword',
            value=None)
        self.eucalyptus_properties.create_property(
            name='sanuser',
            property_string=str(cluster_name) + '.storage.sanuser',
            value=None)
        self.eucalyptus_properties.create_property(
            name='scpaths',
            property_string=str(cluster_name) + '.storage.scpaths',
            value=None)
        self.eucalyptus_properties.create_property(
            name='shouldtransfersnapshots',
            property_string=str(cluster_name) + '.storage.shouldtransfersnapshots',
            value=None)
        self.eucalyptus_properties.create_property(
            name='snapshotpartsizeinmb',
            property_string=str(cluster_name) + '.storage.snapshotpartsizeinmb',
            value=None)
        self.eucalyptus_properties.create_property(
            name='snapshotuploadtimeoutinhours',
            property_string=str(cluster_name) + '.storage.snapshotuploadtimeoutinhours',
            value=None)
        self.eucalyptus_properties.create_property(
            name='storeprefix',
            property_string=str(cluster_name) + '.storage.storeprefix',
            value=None)
        self.eucalyptus_properties.create_property(
            name='tasktimeout',
            property_string=str(cluster_name) + '.storage.tasktimeout',
            value=None)
        self.eucalyptus_properties.create_property(
            name='tid',
            property_string=str(cluster_name) + '.storage.tid',
            value=None)
        self.eucalyptus_properties.create_property(
            name='timeoutinmillis',
            property_string=str(cluster_name) + '.storage.timeoutinmillis',
            value=None)
        self.eucalyptus_properties.create_property(
            name='volumesdir',
            property_string=str(cluster_name) + '.storage.volumesdir',
            value=None)
        self.eucalyptus_properties.create_property(
            name='zerofillvolumes',
            property_string=str(cluster_name) + '.storage.zerofillvolumes',
            value=None)
        # Create json configuration (blocks) properties
        self.storage_controllers = self.create_property('storage_controllers', value=[])
        self.backend_type = self.create_property(json_name='backend_type',
                                                 value=backend_type,
                                                 validate_callback=self.validate_backend_type)

        # Baseconfig init() will read in default values from read_file_path if it is populated.
        super(BlockStorage, self).__init__(name=name,
                                           description=None,
                                           read_file_path=None,
                                           write_file_path=None,
                                           property_type=property_type,
                                           version=None)

    def validate_backend_type(self, backend_type):
        try:
            if backend_type is not None:
                _STORAGE_BACKENDS[str(backend_type).lower()]
        except KeyError:
            hlist = ""
            for key in _STORAGE_BACKENDS:
                hlist += "{0}, ".format(key)
            raise ValueError('Unknown hypervisor type:"{0}". Possible types:"{1}"'
                             .format(backend_type, hlist.rstrip(', ')))
        if not hasattr(self, 'backend_type') or not self.backend_type.value:
            return backend_type
        if (backend_type != self.backend_type.value) and self.storage_controllers.value:
                raise ValueError('Must remove storage controllrs to change backend_type')
        return backend_type

    # todo add check for correct attributes such as matching backend type etc..
    def add_storage_controllers(self, storage_controllers):
        if not storage_controllers:
            raise ValueError('add_storage_controllers provided empty value: "{0}"'
                             .format(storage_controllers))
        if not isinstance(storage_controllers, list):
            storage_controllers = [storage_controllers]
        for sc in storage_controllers:
            assert isinstance(sc, Storage_Controller), \
                'add storage_controller passed non BlockStorageController type, ' \
                'sc:"{0}"'.format(sc)
            if self.get_storage_controller(sc.name.value):
                raise ValueError('Storage Controller with name:"{0}" already exists'
                                 .format(sc.name.value))
            self.storage_controllers.value.append(sc)

    def get_storage_controller(self, name):
        for sc in self.storage_controllers.value:
            if sc.name == name:
                return sc

    def delete_storage_controller(self, name):
        sc = self.get_storage_controller(name)
        if sc:
            self.storage_controllers.value.pop(sc)

    def create_storage_controller(self, name):
        raise NotImplementedError('Make this work')
