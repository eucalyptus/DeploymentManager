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


class BlockStorage(BaseConfig):
    storage_manager_name = None

    def __init__(self,
                 name,
                 cluster_name,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 storage_controllers=None,
                 storage_backend=None):

        description = description or 'Eucalyptus Block Storage Configuration Block for ' \
                                     'backend:"{0}"'.format(self.storage_manager_name)
        # Create the Eucalyptus software specific properties
        self.eucalyptus_properties.blockstoragemanager = EucalyptusProperty(
            name=str(cluster_name) + '.storage.blockstoragemanager',
            properties_manager=self.eucalyptus_properties,
            value=self.storage_manager_name,
            validate_callback=self.validate_storage_manager_property)

        self.eucalyptus_properties.chapuser = EucalyptusProperty(
            name=str(cluster_name) + '.storage.chapuser',
            properties_manager=self.eucalyptus_properties,
            value=None)
        # self.eucalyptus_properties.dasdevice = EucalyptusProperty(
        #       name=str(cluster_name) + '.storage.dasdevice',
        #       properties_manager=self.eucalyptus_properties,
        #       value=None)
        self.eucalyptus_properties.deletedvolexpiration = EucalyptusProperty(
            name=str(cluster_name) + '.storage.deletedvolexpiration',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.maxconcurrentsnapshotuploads = EucalyptusProperty(
            name=str(cluster_name) + '.storage.maxconcurrentsnapshotuploads',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.maxsnapshotpartsqueuesize = EucalyptusProperty(
            name=str(cluster_name) + '.storage.maxsnapshotpartsqueuesize',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.maxsnaptransferretries = EucalyptusProperty(
            name=str(cluster_name) + '.storage.maxsnaptransferretries',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.maxtotalvolumesizeingb = EucalyptusProperty(
            name=str(cluster_name) + '.storage.maxtotalvolumesizeingb',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.maxvolumesizeingb = EucalyptusProperty(
            name=str(cluster_name) + '.storage.maxvolumesizeingb',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.multihostaccess = EucalyptusProperty(
            name=str(cluster_name) + '.storage.multihostaccess',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.ncpaths = EucalyptusProperty(
            name=str(cluster_name) + '.storage.ncpaths',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.poolname = EucalyptusProperty(
            name=str(cluster_name) + '.storage.poolname',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.resourceprefix = EucalyptusProperty(
            name=str(cluster_name) + '.storage.resourceprefix',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.resourcesuffix = EucalyptusProperty(
            name=str(cluster_name) + '.storage.resourcesuffix',
            properties_manager=self.eucalyptus_properties,
            value=None)
        # self.eucalyptus_properties.sanhost = EucalyptusProperty(
        #       name=str(cluster_name) + '.storage.sanhost',
        #       properties_manager=self.eucalyptus_properties,
        #       value=None)
        # self.eucalyptus_properties.sanpassword = EucalyptusProperty(
        #       name=str(cluster_name) + '.storage.sanpassword',
        #       properties_manager=self.eucalyptus_properties,
        #       value=None)
        # self.eucalyptus_properties.sanuser = EucalyptusProperty(
        #       name=str(cluster_name) + '.storage.sanuser',
        #       properties_manager=self.eucalyptus_properties,
        #       value=None)
        self.eucalyptus_properties.scpaths = EucalyptusProperty(
            name=str(cluster_name) + '.storage.scpaths',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.shouldtransfersnapshots = EucalyptusProperty(
            name=str(cluster_name) + '.storage.shouldtransfersnapshots',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.snapshotpartsizeinmb = EucalyptusProperty(
            name=str(cluster_name) + '.storage.snapshotpartsizeinmb',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.snapshotuploadtimeoutinhours = EucalyptusProperty(
            name=str(cluster_name) + '.storage.snapshotuploadtimeoutinhours',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.storeprefix = EucalyptusProperty(
            name=str(cluster_name) + '.storage.storeprefix',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.tasktimeout = EucalyptusProperty(
            name=str(cluster_name) + '.storage.tasktimeout',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.tid = EucalyptusProperty(
            name=str(cluster_name) + '.storage.tid',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.timeoutinmillis = EucalyptusProperty(
            name=str(cluster_name) + '.storage.timeoutinmillis',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.volumesdir = EucalyptusProperty(
            name=str(cluster_name) + '.storage.volumesdir',
            properties_manager=self.eucalyptus_properties,
            value=None)
        self.eucalyptus_properties.zerofillvolumes = EucalyptusProperty(
            name=str(cluster_name) + '.storage.zerofillvolumes',
            properties_manager=self.eucalyptus_properties,
            value=None)

        # Create json configuration (blocks) properties
        self.storage_controllers = self.create_property(json_name='storage_controllers',
                                                        value=[])

        # Baseconfig init() will read in default values from read_file_path if it is populated.
        super(BlockStorage, self).__init__(name=name,
                                           description=None,
                                           read_file_path=None,
                                           write_file_path=None,
                                           property_type=property_type,
                                           version=None)

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

    def create_storage_controller(self, hostname, name=None):
        new_sc = Storage_Controller(name=name, hostname=hostname)
        self.add_storage_controllers(new_sc)
        return new_sc

    def validate_storage_manager_property(self, storagemanager):
        raise ValueError('Cannot change storage manager value for class:"{0}"'
                         .format(self.__class__.__name__))
