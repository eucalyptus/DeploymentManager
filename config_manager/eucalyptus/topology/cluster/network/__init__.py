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
from config_manager.eucalyptus.topology.cluster.network.edge_network_config \
    import Edge_Network_Config
from config_manager.eucalyptus.topology.cluster.network.managed_network_config \
    import Managed_Network_Config
from config_manager.eucalyptus.topology.cluster.network.managed_novlan_network_config \
    import Managed_Novlan_Network_Config

import copy
import ipaddr
import socket
import math


class Network(BaseConfig):
    modes = {
        'EDGE': Edge_Network_Config,
        'MANAGED': Managed_Network_Config,
        'MANAGED_NOVLAN': Managed_Novlan_Network_Config
    }

    def __init__(self,
                 mode=None,
                 name=None,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 network_type=None):

        description = description or "Eucalyptus Network Configuration Block"

        # Network Configuration properties...
        self.network_mode_configuration_property = self.create_property(
            'mode_configuration',
            value=mode,
            validate_callback=self._validate_network_mode_property,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE\n"
                        "The networking mode in which to run. \n"
                        "The same mode must be specified on all CCs and NCs in your cloud"
        )
        self.instance_dns_server_property = self.create_property(
            'instance_dns_server',
            value=[],
            validate_callback=self._validate_ip_entry_strings,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE\n"
                        "The addresses of the DNS servers to supply to instances in \n"
                        "DHCP responses."
        )
        self.vm_mac_prefix_property = self.create_property(
            json_name='vnet_macprefix',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN\n"
                        "This option is used to specify a prefix for MAC addresses generated \n"
                        "by Eucalyptus for VM instances. The prefix has to be in the form HH:HH \n"
                        "where H is a hexadecimal digit. Example: VNET_MACPREFIX='D0:D0'"
        )
        self.intercluster_tunneling_enabled_property= self.create_property(
            json_name=' DISABLE_TUNNELING',
            value=None,
            validate_callback=self._validate_reverse_boolean,
            description="Tunneling is used to enable to enable intercluster VM network \n"
                        "communication when clusters are located in different layer 2 broadcast \n"
                        "domains. Enabling this property can cause network loops if clusters \n"
                        "reside in the same l2 broadcast domain"
        )

        self.default_dhcp_daemon_property = self.create_property(
            'dhcp_daemon',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE(on NC)\n"
                        "The ISC DHCP executable to use.\n"
                        "This is set to a distro-dependent value by packaging."
        )
        self.default_dhcp_user_property = self.create_property(
            json_name='vnet_dhcpuser',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN\n"
                        "The user the DHCP daemon runs as on your distribution."
        )
        self.default_cc_public_interface_property = self.create_property(
            'default_cc_public_interface',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE(on NC)\n"
                        "On a CC, this is the name of the network interface that is connected\n"
                        "to the “public” network. \n"
        )
        self.default_nc_public_interface_property = self.create_property(
            'default_nc_public_interface',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE(on NC)\n"
                        "On an NC, this is the name of the network\n"
                        "interface that is connected to the same network as the CC. Depending\n"
                        "on the hypervisors configuration this may be a bridge or a physical\n"
                        "interface that is attached to the bridge."
        )
        self.default_private_interface_property = self.create_property(
            'vnet_private_interface',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE(on NC)\n"
                        "The name of the network interface that is on the same network as \n"
                        "the NCs. In Managed and Managed (No VLAN) modes this must be a bridge \n"
                        "for instances in different clusters but in the same security group to \n"
                        "be able to reach one another with their private addresses."
        )
        self.default_node_bridge_interface_property = self.create_property(
            'vnet_bridge_interface',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN, EDGE(on NC)\n"
                        "On an NC, this is the name of the bridge interface to which instances' \n"
                        "network interfaces should attach. A physical interface that can reach \n"
                        "the CC must be attached to this bridge. Common setting for KVM is br0."
        )
        self.default_l2tp_localip_property = self.create_property(
            'vnet_localip',
            value=None,
            description="Modes: MANAGED, MANAGED-NOVLAN\n"
                        "By default the CC automatically determines which IP address to use \n"
                        "when setting up tunnels to other CCs. Set this to the IP address that \n"
                        "other CCs can use to reach this CC if tunneling does not work."
        )

        super(Network, self).__init__(name=name,
                                      description=description,
                                      read_file_path=read_file_path,
                                      write_file_path=write_file_path,
                                      property_type=property_type,
                                      version=version)



    def _validate_network_mode_property(self, value):
        if value:
            if isinstance(value, str):
                value = str(value).upper()
                if self.modes.has_key(value):
                    mode_class = self.modes[value]
                    return mode_class()
                raise ValueError('Invalid network mode:"{0}", valid options:'
                                 .format(value, self.modes.keys()))
            else:
                for net_class in self.modes:
                    if isinstance(value, net_class):
                        return value
                raise ValueError('Invalid network mode object:' + str(value))
        return None

    def get_network_mode_config(self):
        return self.network_mode_configuration_property.value

    def set_network_mode(self, mode):
        self.network_mode_configuration_property.value = mode

    def create_vm_network_subnet(self, subnet, gateway=None, public_ips=None, private_ips=None):
        mode_config = self.get_network_mode_config()
        subnet = mode_config.create_subnet(subnet=subnet,
                                           gateway=gateway,
                                           public_ips=public_ips,
                                           private_ips=private_ips)
        return subnet

    def get_subnet_by_ip(self, ip):
        mode_config = self.get_network_mode_config()
        for subnet in mode_config.vm_subnets:
            if subnet._is_ip_entry_in_subnet(ip):
                return subnet
        return None

    def get_subnet_by_name(self, name):
        mode_config = self.get_network_mode_config()
        for subnet in mode_config.vm_subnets:
            if subnet.name == name:
                return subnet
        return None

    def _validate_addrs_per_security_group_property(self, value):
        if value and not math.log(int(value),2)%1:
            return value
        else:
            return None

    def _check_mode_allows(self, modes, err_string=None):
        if err_string:
            err_string = 'Check for: "{0}"'.format(err_string)
        else:
            err_string = ""
        for mode in modes:
            if self._network_mode_string.upper() == str(mode).upper():
                return
        raise ValueError('Current network mode:"{0}", is not part of allowed modes:"{1}". {2}'
                         .format(self._network_mode_string, modes, err_string))


    def _validate_privateips(self, privateips):
        return self._validate_ip_entry_strings(privateips)

    def _validate_publicips(self, publicips):
        return self._validate_ip_entry_strings(publicips)

    def _validate_ip_entry_strings(self, iplist):
        if iplist is None or iplist == []:
            return iplist
        if not isinstance(iplist, list):
            checklist = [iplist]
        else:
            checklist = iplist
        for item in checklist:
            ips = str(item).split('-')
            # Validate any ips passed
            for ip in ips:
                self._validate_ip_string(ip)
        return iplist

    def _validate_ip_string(self, ip):
        try:
            socket.inet_aton(ip)
        except TypeError, socket.error:
            raise ValueError('Invalid IP address: "{0}"'.format(ip))

    def _sort_ip_list(self, iplist):
        items = sorted(iplist.items(), key=lambda item: socket.inet_aton(item[0]))
        return items

    def is_address_in_network(cls, ip_addr, network):
        """
        :param ip_addr: Ip address ie: 192.168.1.5
        :param network: Ip network in cidr notation ie: 192.168.1.0/24
        :return: boolean true if ip is found to be in network/mask, else false
        """
        ip = ipaddr.IPv4Address(ipaddr)
        ip_net = ipaddr.IPv4Network(network)
        return ip_net.Contains(ip)

    def add_public_ip_entry(self, public_ip_entry):
        new_list = []
        if not public_ip_entry:
            raise ValueError('Bad public ip:"{0}" pass to add_public_ip_entry'
                             .format(public_ip_entry))
        ip_entry_list = str(public_ip_entry).split(',')
        for ip_entry in ip_entry_list:
            # Check if the entry conflicts with the network, broadcast or gateway addrs
            self._check_ip_entry_for_subnet_conflicts(ip_entry)
            # Check for conflicts in both the existing ip entries as well as the current...
            templist = copy.copy(ip_entry_list)
            templist.remove(ip_entry)
            templist.extend(self.public_ips_property.value)
            self._check_ip_for_list_conflicts(ip_entry=ip_entry, existing_list=templist)
            new_list.append(ip_entry)
        self.public_ips_property.value.extend(new_list)
        self.public_ips_property.value.sort()

    def delete_public_ip_entry(self, ip_entry):
        for entry in self.public_ips_property.value:
            if entry == ip_entry:
                delentry= self.public_ips_property.value.pop(entry)
                self.public_ips_property.value.sort()
                return delentry

    def add_private_ip_entry(self, private_ip_entry):
        new_list = []
        if not self.subnet:
            raise ValueError('Must set network subnet before adding private ip entries')
        if not private_ip_entry:
            raise ValueError('Bad private ip:"{0}" passed to add_private_ip_entry'
                             .format(private_ip_entry))
        ip_entry_list = str(private_ip_entry).split(',')
        for ip_entry in ip_entry_list:
            if not self._is_ip_entry_in_subnet(ip_entry):
                # Check if the entry is within the current subnet
                raise ValueError('IP Entry:"{0}" is not in configured subnet:"{1}"'
                                 .format(ip_entry, self.subnet))
            # Check if the entry conflicts with the network, broadcast or gateway addrs
            self._check_ip_entry_for_subnet_conflicts(ip_entry)
            # Check for conflicts in both the existing ip entries as well as the current...
            templist = copy.copy(ip_entry_list)
            templist.remove(ip_entry)
            templist.extend(self.private_ips_property.value)
            self._check_ip_for_list_conflicts(ip_entry=ip_entry,
                                     existing_list=templist)
            new_list.append(ip_entry)
        self.private_ips_property.value.extend(new_list)
        self.private_ips_property.value.sort()

    def _is_ip_entry_in_subnet(self, ip_entry, subnet=None):
        subnet = subnet or self.subnet
        if not isinstance(subnet, ipaddr.IPv4Network):
            raise TypeError('subnet must be of type ipaddr.IPv4Network. type:"{0}", subnet:"{1}"'
                            .format(type(subnet), subnet))
        for ip in str(ip_entry).split('-'):
            self._validate_ip_string(ip)
            if not subnet.Contains(ipaddr.IPv4Address(ip)):
                return False
        return True

    def delete_private_ip_entry(self, ip_entry):
        for entry in self.private_ips_property.value:
            if entry == ip_entry:
                delentry = self.private_ips_property.value.pop(entry)
                self.private_ips_property.value.sort()
                return delentry

    def clear_all_private_ip_entries(self):
        self.private_ips_property.value = []

    def clear_all_public_ip_entries(self):
        self.public_ips_property.value = []

    def _check_ip_for_list_conflicts(self,
                            ip_entry,
                            existing_list,
                            err_on_conflict=True):
        '''
        Checks an ip entry which is a string representing a single ip "x.x.x.x" or a
        range of ips "x.x.x.x-y.y.y.y" against a list of existing ip entries. If there is any
        overlap or conflicts between 'ip_entry' and the 'existing_list' of entries a value error is
        raised or an error is printed depending on the 'err_on_conflict' flag.
        :param ip_entry: string ip entry either: 'x.x.x.x', or range 'x.x.x.x-y.y.y.y'
        :param existing_list: list of ip entries to check against
        :param err_on_conflict: boolean, if True will raise ValueError for conflicts
                                with 'existing_list'
        :raises: ValueError
        '''
        newips = str(ip_entry).split('-')
        self._validate_ip_entry_strings(newips)

        # Check individual ips for conflicts with existing ips/ranges...
        if existing_list:
            for existing_entry in existing_list:
                conflict = False
                existing_ips = existing_entry.split('-')
                if len(existing_ips) == 1:
                    if len(newips) == 1:
                        if newips[0] == existing_ips[0]:
                            conflict = True
                    else:
                        # See if the existing ip is within the new (range) entry given...
                        if self._is_ip_in_range(existing_ips[0], newips[0], newips[1]):
                            conflict = True
                else:
                    for ip in newips:
                        if self._is_ip_in_range(ip, existing_ips[0], existing_ips[1]):
                            conflict = True
                            break
                if conflict:
                    if err_on_conflict:
                        raise ValueError('New IP entry:"{0}" conflicts with existing '
                                         'entry:"{1}"'
                                         .format(ip_entry, existing_entry))
                    else:
                        return existing_entry
        return None

    def _check_ip_entry_for_subnet_conflicts(self, ip_entry, subnet=None, gateway=None):
        """
        Checks an ip entry which is a string representing a single ip "x.x.x.x" or a
        range of ips "x.x.x.x-y.y.y.y" against the subnet's network, broadcast and gateway
        addresses for conflicts.
        :param ip_entry: string ip entry either: 'x.x.x.x', or range 'x.x.x.x-y.y.y.y'
        :param subnet: ipaddr network object used to check for network, and bcast addr conflicts
        :param gateway: ipaddr address object used to check for conflicts
        """
        subnet = subnet or self.subnet
        gateway = gateway or self.gateway
         # Check individual ips for conflicts with the subnet addrs...
        newips = str(ip_entry).split('-')
        self._validate_ip_entry_strings(newips)
        if subnet or gateway:
            for ip in newips:
                if subnet:
                    if (str(ip) == str(subnet.broadcast) or
                                str(ip) == str(subnet.network)):
                        raise ValueError('Error. IP entry:"{0}" conflicts with subnet.'
                                         '(Nework addr:"{1}", broadcast:"{2}")'
                                         .format(ip_entry,
                                                 subnet.network,
                                                 subnet.broadcast))
                if gateway and str(ip) == str(gateway):
                    raise ValueError('Error. IP entry:"{0}" conflicts with gateway:"{1}"'
                                     .format(ip_entry, gateway))

    def _is_ip_in_range(self, ip, range_start, range_end):
        """
        If 'ip' is in the range 'range_start' to 'range_end' this
        method will return True, otherwise False.
        :param ip: string ip (x.x.x.x)
        :param range_start: string ip (x.x.x.x), start of ip range
        :param range_end: string ip (x.x.x.x), end of ip range
        :returns: boolean
        """
        self._validate_ip_entry_strings([ip, range_start, range_end])
        check_ip = ipaddr.IPv4Address(ip)
        range_start = ipaddr.IPv4Address(range_start)
        range_end = ipaddr.IPv4Address(range_end)
        if check_ip >= range_start and check_ip <= range_end:
            return True
        else:
            return False

    def _get_conflicting_ip_entry(self, ip_entry, existinglist):
        '''
        Check an 'ip_entry' string for conflicts with other network addresses. Return the address
        that is conflicting.
        :param ip_entry: string ip entry either: 'x.x.x.x', or range 'x.x.x.x-y.y.y.y'
        :param existinglist: list of ip entries to check against (in addition to self.subnet,
                             and self.gateway)
        :returns: string of conflicting ip
        '''
        return self._check_ip_for_list_conflicts(ip_entry=ip_entry,
                                        existing_list=existinglist,
                                        err_on_conflict=False)

    def _get_ip_entry_range(self, entry):
        """
        Takes an ip entry which is expected to be in the format "x.x.x.x" or
        range "x.x.x.x-y.y.y.y" and return a 2 item list of ip addresses to represent start, and
        end of a range. If a single IP is provided then start and end will be the same value.
        :param entry: string ip entry either: 'x.x.x.x', or range 'x.x.x.x-y.y.y.y'
        :returns: list of ips containing the range of the ip entry. ie: [start, end]
        """
        print 'getting ip_entry_range for entry:' + str(entry)
        self._validate_ip_entry_strings(entry)
        iprange =[]
        splitentry = entry.split('-')
        iprange.append(splitentry[0])
        if len(splitentry) == 1:
            iprange.append(splitentry[0])
        else:
            iprange.append(splitentry[1])
        return iprange

    def _validate_reverse_boolean(self, value):
        '''
        Method is intended to make some of the more confusing Eucalyptus properties easier for
        end users to understand by renaming the property and allowing the value(s) to reversed
        where needed to match the  naming.
        Validates the value provided is a boolean or None. Returns the reverse of the boolean,
        or None.
        '''
        #Allow disabling the property with None
        if value is None:
            return None
        assert isinstance(value, bool), \
            'Value must be of type boolean :"{0}"/"{1}"'.format(value, type(value))
        if value:
            return False
        else:
            return True
