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
from config_manager.eucalyptus.topology.cluster.blockstorage.storage_controller import \
    Storage_Controller
import config_manager.eucalyptus.topology.cluster.blockstorage.storage_backends
from storage_backends.ceph import Ceph
from storage_backends.das import Das
from storage_backends.emc import Emc
from storage_backends.equalogic import Equalogic
from storage_backends.netapp import Netapp
from storage_backends.overlay import Overlay

storage_backends = {'ceph': Ceph,
                    'das': Das,
                    'emc': Emc,
                    'equalogic': Equalogic,
                    'netapp': Netapp,
                    'overlay': Overlay}


class BlockStorage(BaseConfig):
    def __init__(self,
                 name,
                 cluster_name,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 backend_type=None,
                 storage_controllers=None,
                 storage_backend=None):

        # Create the Eucalyptus software specific properties
        self.blockstoragemanager = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.blockstoragemanager', value='')
        self.chapuser = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.chapuser', value='')
        self.dasdevice = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.dasdevice', value='')
        self.deletedvolexpiration = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.deletedvolexpiration', value='')
        self.maxconcurrentsnapshotuploads = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.maxconcurrentsnapshotuploads', value='')
        self.maxsnapshotpartsqueuesize = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.maxsnapshotpartsqueuesize', value='')
        self.maxsnaptransferretries = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.maxsnaptransferretries', value='')
        self.maxtotalvolumesizeingb = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.maxtotalvolumesizeingb', value='')
        self.maxvolumesizeingb = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.maxvolumesizeingb', value='')
        self.multihostaccess = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.multihostaccess', value='')
        self.ncpaths = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.ncpaths', value='')
        self.poolname = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.poolname', value='')
        self.resourceprefix = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.resourceprefix', value='')
        self.resourcesuffix = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.resourcesuffix', value='')
        self.sanhost = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.sanhost', value='')
        self.sanpassword = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.sanpassword', value='')
        self.sanuser = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.sanuser', value='')
        self.scpaths = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.scpaths', value='')
        self.shouldtransfersnapshots = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.shouldtransfersnapshots', value='')
        self.snapshotpartsizeinmb = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.snapshotpartsizeinmb', value='')
        self.snapshotuploadtimeoutinhours = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.snapshotuploadtimeoutinhours', value='')
        self.storeprefix = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.storeprefix', value='')
        self.tasktimeout = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.tasktimeout', value='')
        self.tid = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.tid', value='')
        self.timeoutinmillis = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.timeoutinmillis', value='')
        self.volumesdir = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.volumesdir', value='')
        self.zerofillvolumes = self._set_eucalyptus_property(
            str(self.cluster_name) + '.storage.zerofillvolumes', value='')

        # Create json configuration (blocks) properties
        self.storage_controllers = self.create_property('storage_controllers', value=[])
        self.backend_type = self.create_property(json_name='backend_type',
                                                 value=backend_type)

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

    def create_storage_controller(self, name):
        raise NotImplementedError('Make this work')
