#!/usr/bin/env python
# coding=utf-8

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

class Euca_Conf_File(BaseConfig):
    def __init__(self,
                 name='eucalyptus_conf',
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None):

        self.EUCALYPTUS = self.create_property(
            json_name = 'EUCALYPTUS',
            value = None,
            description = """Where Eucalyptus is installed"""
        )

        self.EUCA_USER = self.create_property(
            json_name = 'EUCA_USER',
            value = None,
            description = """This is the username that you would like eucalyptus to run as"""
        )

        self.CLOUD_OPTS = self.create_property(
            json_name = 'CLOUD_OPTS',
            value = None,
            description = """Extra options to pass to the eucalyptus-cloud process, such as
                             loglevels, heap size, or other JVM flags. """
        )

        self.CREATE_SC_LOOP_DEVICES = self.create_property(
            json_name = 'CREATE_SC_LOOP_DEVICES',
            value = None,
            description = """The number of loop devices to make available at SC startup time.
                             The default is 256.  If you supply "max_loop" to the loop driver
                             then this setting must be equal to that number. """
        )

        self.LOGLEVEL = self.create_property(
            json_name = 'LOGLEVEL',
            value = None,
            description = """The level of logging output.  Valid settings are, in descending
                             order ofverbosity: EXTREME, TRACE, DEBUG, INFO, WARN, ERROR, and
                             FATAL. The default is INFO. """
        )

        self.LOGROLLNUMBER = self.create_property(
            json_name = 'LOGROLLNUMBER',
            value = None,
            description = """The number of old log files to keep when rotating logs, in
                             range [0-999]. The default is 10. When set to 0, no rotation is
                             performed and log sizelimit is (LOGMAXSIZE, below) is
                             not enforced. """
        )

        self.LOGMAXSIZE = self.create_property(
            json_name = 'LOGMAXSIZE',
            value = None,
            description = """The maximum size of the log file, in bytes. 100MB by default.
                             For thissize to be enforced, LOGROLLNUMBER, above, must be 1 or
                             higher. If logrotation is performed by an outside tool, either set
                             LOGROLLNUMBER to 0 or set this limit to a large value. """
        )

        self.NC_PORT = self.create_property(
            json_name = 'NC_PORT',
            value = None,
            description = """On a NC, this defines the TCP port on which the NC will
                             listen. On a CC, this defines the TCP port on which the CC
                             will contact NCs. """
        )

        self.CC_PORT = self.create_property(
            json_name = 'CC_PORT',
            value = None,
            description = """The TCP port on which the CC will listen. """
        )

        self.SCHEDPOLICY = self.create_property(
            json_name = 'SCHEDPOLICY',
            value = None,
            description = """The scheduling policy that the CC uses to choose the NC on
                             which torun each new instance.  Valid settings include
                             GREEDY and ROUNDROBIN.
                             The default scheduling policy is ROUNDROBIN. """
        )

        self.NODES = self.create_property(
            json_name = 'NODES',
            value = None,
            description = """A space-separated list of IP addresses for all the NCs that
                             this CC should communicate with.  The ``euca_conf --register-nodes''
                             commandmanipulates this setting. """
        )

        self.DISABLE_TUNNELING = self.create_property(
            json_name = 'DISABLE_TUNNELING',
            value = None,
            description = """The default is valid when multiple CCs reside in the same layer 2
                             broadcast domain or running single cluster.  Change this setting
                             to "N" to enable tunneling when you have separate layer 2 broadcast
                             domains in separate clusters. This setting has no effect in
                             Edge mode. """
        )

        self.NC_SERVICE = self.create_property(
            json_name = 'NC_SERVICE',
            value = None,
            description = """The location of the NC service.
                             The default is axis2/services/EucalyptusNC"""
        )

        self.HYPERVISOR = self.create_property(
            json_name = 'HYPERVISOR',
            value = None,
            description = """The hypervisor that the NC will interact with in order to manage
                             virtual machines.  Supported values include "kvm" and "xen". """
        )

        self.USE_VIRTIO_ROOT = self.create_property(
            json_name = 'USE_VIRTIO_ROOT',
            value = None,
            description = """If "1", use Virtio for the root file system"""
        )

        self.USE_VIRTIO_DISK = self.create_property(
            json_name = 'USE_VIRTIO_DISK',
            value = None,
            description = """If "1", use Virtio for dynamic block volumes"""
        )

        self.USE_VIRTIO_NET = self.create_property(
            json_name = 'USE_VIRTIO_NET',
            value = None,
            description = """If "1", use Virtio for the network card"""
        )

        self.MAX_CORES = self.create_property(
            json_name = 'MAX_CORES',
            value = None,
            description = """The number of virtual CPU cores that Eucalyptus is allowed to allocate
                             to instances.  The default value of 0 allows Eucalyptus to use all
                             CPU cores on the system. """
        )

        self.NC_WORK_SIZE = self.create_property(
            json_name = 'NC_WORK_SIZE',
            value = None,
            description = """The amount of disk space, in megabytes, that the NC is allowed to use
                             in its work directory ($INSTANCE_PATH/eucalyptus/work). By default
                             the NC chooses automatically.  Values below 10 are ignored. """
        )

        self.NC_CACHE_SIZE = self.create_property(
            json_name = 'NC_CACHE_SIZE',
            value = None,
            description = """The amount of disk space, in megabytes, that the NC is allowed to
                             use inits image cache directory ($INSTANCE_PATH/eucalyptus/cache).
                             By default the NC chooses automatically.
                             A value below 10 will disable caching. """
        )

        self.CONCURRENT_DISK_OPS = self.create_property(
            json_name = 'CONCURRENT_DISK_OPS',
            value = None,
            description = """The number of disk-intensive operations that the NC is allowed
                             to perform at once. A value of 1 serializes all disk-intensive
                             operations. The default value is 4. """
        )

        self.CREATE_NC_LOOP_DEVICES = self.create_property(
            json_name = 'CREATE_NC_LOOP_DEVICES',
            value = None,
            description = """The number of loop devices to make available at NC startup time.
                             The default is 256.  If you supply "max_loop" to the loop driver then
                             this setting must be equal to that number. """
        )

        self.INSTANCE_PATH = self.create_property(
            json_name = 'INSTANCE_PATH',
            value = None,
            description = """The directory where the NC will store instances' root filesystems,
                             ephemeral storage, and cached copies of images. """
        )

        self.NC_BUNDLE_UPLOAD_PATH = self.create_property(
            json_name = 'NC_BUNDLE_UPLOAD_PATH',
            value = None,
            description = """If euca-bundle-upload, euca-check-bucket, or euca-delete-bundle do
                             not appear in the NC's search PATH then specify their
                             locations here. """
        )

        self.NC_CHECK_BUCKET_PATH = self.create_property(
            json_name = 'NC_CHECK_BUCKET_PATH',
            value = None,
            description = """If euca-bundle-upload, euca-check-bucket, or euca-delete-bundle do
                             not appear in the NC's search PATH then specify their
                             locations here. """
        )

        self.NC_DELETE_BUNDLE_PATH = self.create_property(
            json_name = 'NC_DELETE_BUNDLE_PATH',
            value = None,
            description = """If euca-bundle-upload, euca-check-bucket, or euca-delete-bundle do
                             not appear in the NC's search PATH then specify their
                             locations here. """
        )

        self.NC_MIGRATION_READY_THRESHOLD = self.create_property(
            json_name = 'NC_MIGRATION_READY_THRESHOLD',
            value = None,
            description = """The maximum amount of time, in seconds, that an instance will remain
                             in a migration-ready state on a source NC while awaiting the
                             preparation of a destination NC for a migration. After this time
                             period, the migration request will be terminated and the any
                             preparation on the source NC will be rolled back.
                             Default is 15 minutes. """
        )

        self.WALRUS_DOWNLOAD_MAX_ATTEMPTS = self.create_property(
            json_name = 'WALRUS_DOWNLOAD_MAX_ATTEMPTS',
            value = None,
            description = """The number of connection attempts that NC will try to downlaod an
                             image or image manifest from Walrus. Failure to download may be due
                             to a registered image not being available for download while
                             Walrus is decrypting and caching it. Smallest allowed value is 1,
                             while the biggest is 98. The default, as of 3.3.1, is 9, which
                             gives over 13 minutes of wait time. (Download attempts are
                             backedoff at exponentially increasing intervals up to a max of 300
                             sec between retries.)"""
        )

        self.VNET_MODE = self.create_property(
            json_name = 'VNET_MODE',
            value = None,
            description = """The networking mode in which to run.  The same mode must be
                             specified on all CCs and NCs in the entire cloud. Valid values
                             include EDGE, MANAGED, and MANAGED-NOVLAN."""
        )

        self.VNET_PRIVINTERFACE = self.create_property(
            json_name = 'VNET_PRIVINTERFACE',
            value = None,
            description = """The name of the network interface that is on the same network as
                             the NCs. The default is "eth0".
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_PUBINTERFACE = self.create_property(
            json_name = 'VNET_PUBINTERFACE',
            value = None,
            description = """On a CC, this is the name of the network interface that is
                             connected to the "public" network.  When tunnelling is enabled, this
                             must be a bridge.  The default is "eth0".
                             Networking modes: Managed, Managed (No VLAN)
                             On an NC, this is the name of the network interface that is connected
                             to the same network as the CC.  The default is "eth0".
                             Networking modes: Edge, Managed"""
        )

        self.VNET_BRIDGE = self.create_property(
            json_name = 'VNET_BRIDGE',
            value = None,
            description = """On an NC, this is the name of the bridge interface to which
                             instances' network interfaces should attach.
                             A physical interface that can reach the CC must be attached to
                             this bridge.
                             Networking modes: Edge, Managed (No VLAN)"""
        )

        self.VNET_PUBLICIPS = self.create_property(
            json_name = 'VNET_PUBLICIPS',
            value = None,
            description = """A space-separated list of individual and/or hyphenated ranges of
                             public IP addresses to assign to instances.
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_SUBNET = self.create_property(
            json_name = 'VNET_SUBNET',
            value = None,
            description = """The address and network mask of the network the cloud should use for
                             instances' private IP addresses.
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_NETMASK = self.create_property(
            json_name = 'VNET_NETMASK',
            value = None,
            description = """The address and network mask of the network the cloud should use for
                             instances' private IP addresses.
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_ADDRSPERNET = self.create_property(
            json_name = 'VNET_ADDRSPERNET',
            value = None,
            description = """The number of IP addresses to allocate to each security group.
                             Specify a power of 2 between 16 and 2048.
                             IMPORTANT: the system will reserve 11 IPs from each security group
                             for internal systemuse, leaving VNET_ADDRSPERNET-11 IPs free for VMs
                             to use for eachsecurity group.
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_DNS = self.create_property(
            json_name = 'VNET_DNS',
            value = None,
            description = """The address of the DNS server to supply to instances in DHCP responses.
                             Networking modes: Managed, Managed (No VLAN). Moving forward,
                             this option will be deprecated in favor of the CLC property. """
        )

        self.VNET_DOMAINNAME = self.create_property(
            json_name = 'VNET_DOMAINNAME',
            value = None,
            description = """The search domain to supply to instance in DHCP responses.
                             NOTE:
                             This should always be cloud.vmstate.instance_subdomain + ".internal",
                             and will be overridden by the CLC property.
                             Moving forward, this option will be deprecated in favor of the CLC
                             property.
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_LOCALIP = self.create_property(
            json_name = 'VNET_LOCALIP',
            value = None,
            description = """Set this to the IP address that other CCs can use to reach this CC
                             if layer 2 tunneling between CCs does not work.
                             It is not normally necessary to change this setting.
                             Networking modes: Managed, Managed (No VLAN)"""
        )

        self.VNET_DHCPDAEMON = self.create_property(
            json_name = 'VNET_DHCPDAEMON',
            value = None,
            description = """The ISC DHCP server executable to use.
                             Networking modes: Edge, Managed, Managed (No VLAN)"""
        )

        self.VNET_DHCPUSER = self.create_property(
            json_name = 'VNET_DHCPUSER',
            value = None,
            description = """The user as which the DHCP daemon runs on your distribution.
                             The default is "dhcpd".
                             Networking modes: Edge, Managed, Managed (No VLAN)"""
        )

        super(Euca_Conf_File, self).__init__(name=name,
                                             description=description,
                                             read_file_path=read_file_path,
                                             write_file_path=write_file_path,
                                             property_type=property_type,
                                             version=version)
