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
import copy
import re
import ipaddr
import socket
import math


class Network(BaseConfig):
    _vnet_mode_string = None
    def __init__(self,
                 subnet,
                 gateway,
                 public_ips=None,
                 private_ips=None,
                 name=None,
                 description=None,
                 read_file_path=None,
                 write_file_path=None,
                 property_type=None,
                 version=None,
                 network_type=None):
        description = description or "Eucalyptus Network Configuration Block. Network Mode:{0}"\
            .format(self._vnet_mode_string)
        self._subnet_ipaddr_obj = None
        self._gateway_ipaddr_obj = None

        # Network Configuration properties...
        self.network_mode_property = self.create_property(
            'mode',
            value=self._vnet_mode_string,
            description="The networking mode in which to run. "
                        "The same mode must be specified on all CCs and NCs in your cloud"
        )
        self.public_ips_property = self.create_property(
            'public-ips',
            value=[],
            validate_callback=self._validate_publicips,
            description="A list of individual and/or hyphenated ranges of public IP \n"
                        "addresses to assign to instances."
        )
        self.addresses_per_network_property = self.create_property(
            'addresses-per-net',
            value=None,
            validate_callback=self._validate_addrs_per_net,
            description="""
                        This option controls how many VM instances can simultaneously be part of
                        an individual user's security group. This option is set to a power
                        of 2 (8, 16, 32, 64, etc.) but it should never be less than 8 and it
                        cannot be larger than: (the total number of available IP addresses - 2).
                        This option is used with VNET_NETMASK to determine how the IP addresses
                        that are available to VMs are distributed among security groups. VMs
                        within a single security group can communicate directly. Communication
                        between VMs within a security group and clients or VMs in other security
                        groups is controlled by a set of firewall rules. For example, setting

                        VNET_NETMASK="255.255.0.0"
                        VNET_ADDRESSPERNET="32"
                        defines a netmask of 255.255.0.0 that uses 16 bits of the IP address
                        to specify a network number. The remaining 16 bits specify valid IP
                        addresses for that network meaning that 2^16 = 65536 IP addresses are
                        assignable on the network. Setting VNET_ADDRESSPERNET="32" tells
                        Eucalyptus that each security group can have at most
                        32 VMs in it (each VM getting its own IP address). Further, it stipulates
                        that at most 2046 security groups can be active at the same time since
                        65536 / 32 = 2048. Eucalyptus reserves two security groups for its own use.

                        In addition to subnets at Layer 3, Eucalyptus uses VLANs at Layer 2 in
                        the networking stack to ensure isolation (Managed mode only).
                        """
        )
        self.instance_dns_server_property = self.create_property(
            'dns-server',
            value=[],
            validate_callback=self._validate_ip_entry_strings,
            description="The addresses of the DNS servers to supply to instances in \n"
                        "DHCP responses."
        )
        self.instance_dns_domain_property = self.create_property(
            'instance-dns-domain',
            value=None,
            description="Internal DNS domain used for instance private DNS names"
        )
        self.private_subnets_property = self.create_property(
            json_name='private-subnets',
            description="Subnets you want Eucalyptus to route through the private \n"
                        "network rather than the public"
        )
        self.vm_mac_prefix_property = self.create_property(
            json_name='vnet-macprefix',
            value=None,
            description="This option is used to specify a prefix for MAC addresses generated \n"
                        "by Eucalyptus for VM instances. The prefix has to be in the form HH:HH \n"
                        "where H is a hexadecimal digit. Example: VNET_MACPREFIX='D0:D0'"
        )
        self._network_subnet_property = self.create_property(
            'subnet',
            value=None,
            validate_callback=self._validate_ip_entry_strings,
            description="Subnet that will be used for private addressing"
        )
        self._network_mask_property = self.create_property(
            'netmask',
            value=None,
            validate_callback=self._validate_ip_entry_strings,
            description="The netmask to be used with the private addressing subnet"
        )
        self._network_gateway_property = self.create_property(
            'gateway',
            value=None,
            validate_callback=self._validate_ip_entry_strings,
            description='Gateway to route packets for private addressing subnet'
        )
        self.private_ips_property = self.create_property(
            'private-ips',
            value=[],
            validate_callback=self._validate_privateips,
            description="Private IPs that will be handed out to instances as they launch"
        )
        self.default_dhcp_daemon_property = self.create_property(
            'dhcp-daemon',
            value=None,
            description="The ISC DHCP executable to use.\n"
                        "This is set to a distro-dependent value by packaging."
        )
        self.default_dhcp_user_property = self.create_property(
            json_name='vnet-dhcpuser',
            value=None,
            description="The user the DHCP daemon runs as on your distribution."
        )
        self.default_public_interface_property = self.create_property(
            'default_public-interface',
            value=None,
            description="On a CC, this is the name of the network interface that is connected\n"
                         "to the “public” network. \n"
                         "On an NC, this is the name of the network\n"
                         "interface that is connected to the same network as the CC. Depending\n"
                         "on the hypervisors configuration this may be a bridge or a physical\n"
                         "interface that is attached to the bridge."
        )
        self.default_private_interface_property = self.create_property(
            'vnet-privinterface',
            value=None,
            description="The name of the network interface that is on the same network as \n"
                        "the NCs. In Managed and Managed (No VLAN) modes this must be a bridge \n"
                        "for instances in different clusters but in the same security group to \n"
                        "be able to reach one another with their private addresses."
        )
        self.default_node_bridge_interface_property = self.create_property(
            'vnet_bridge',
            value=None,
            description="On an NC, this is the name of the bridge interface to which instances' \n"
                        "network interfaces should attach. A physical interface that can reach \n"
                        "the CC must be attached to this bridge. Common setting for KVM is br0."
        )
        self.default_l2tp_localip_property = self.create_property(
            'vnet-localip',
            value=None,
            description="By default the CC automatically determines which IP address to use \n"
                        "when setting up tunnels to other CCs. Set this to the IP address that \n"
                        "other CCs can use to reach this CC if tunneling does not work."
        )

        # Attempt to set properties with any values provided to init...
        self.configure_network(subnet, gateway)

        if private_ips:
            for entry in private_ips.split(','):
                self.add_private_ip_entry(entry)
        if public_ips:
            for entry in public_ips.split(','):
                self.add_public_ip_entry(entry)

        super(Network, self).__init__(name=name,
                                      description=description,
                                      read_file_path=read_file_path,
                                      write_file_path=write_file_path,
                                      property_type=property_type,
                                      version=version)



    def configure_network(self, subnet, gateway):
        """
        Method to set the local subnet and gateway properties with some checks for
        misconfiguration, conflicting, entries, etc..
        :param subnet: string ip subnet in cidr format. (ie: x.x.x.x/x )
        :param gateway: string ip gateway (ie: x.x.x.x )
        """
        orig_subnet = str(self._subnet_ipaddr_obj)
        self.set_subnet(subnet)
        try:
            self.set_gateway(gateway)
        except Exception, E:
            print 'Rolling back subnet due to error:"' + str(E)
            self.set_subnet(orig_subnet)
            raise

    @property
    def subnet(self):
        return self._subnet_ipaddr_obj

    def set_subnet(self, value):
        """
        Method to set the current subnet property. Will validate the subnet against existing
        entries and potential address conflicts, etc..
        :param value: string ip subnet in cidr format. (ie: x.x.x.x/x )
        """
        print 'Setting subnet to value:' + str(value)
        if value is None:
            if self.public_ips_property.value or self.private_ips_property.value:
                raise RuntimeError('Existing public/private ips must be cleared before '
                                   'setting subnet to None')
            print 'Setting subnet to None, clearing all values...'
            self._network_mask_property.value = None
            self._network_subnet_property = None
            self._subnet_ipaddr_obj = None
            self.set_gateway(None)
        else:
            try:
                subnet = ipaddr.IPv4Network(value)
            except:
                print 'WARNING: Failed to convert "{0}" into network. Must be in cidr ' \
                      'format:"x.x.x.x/x"'.format(value)
                raise
            # Check existing private ip list for conflicts
            for entry in self.private_ips_property.value:
                if not self._is_ip_entry_in_subnet(entry, subnet=subnet):
                    raise ValueError('Existing IP entry:"{0}" is not within new subnet:"{1}". '
                                     'Remove before changing subnet'.format(entry, subnet))
                self._check_ip_entry_for_subnet_conflicts(entry, subnet=subnet)

            # Check existing public ip list for conflicts
            for entry in self.public_ips_property.value:
                self._check_ip_entry_for_subnet_conflicts(entry, subnet=subnet)

            # Store current values in case of rollback
            network_orig = self._subnet_ipaddr_obj
            orig_mask = self._network_mask_property.value
            orig_subnet = self._network_subnet_property.value
            try:
                self._network_mask_property.value = str(subnet.netmask)
                self._network_subnet_property.value = str(subnet.network)
                self._subnet_ipaddr_obj = subnet
            except Exception as E:
                print "Error, attempting to roll back network settings. Err: '{0}'".format(E)
                self._subnet_ipaddr_obj.value = network_orig
                self._network_mask_property.value = orig_mask
                self._network_subnet_property.value = orig_subnet
                raise

    @property
    def gateway(self):
        return self._gateway_ipaddr_obj


    def set_gateway(self, value):
        """
        Sets gateway ipaddr obj and json property value. Does basic checks against the gateway
        'value' provided for potential conflicts, etc..
        :param value: string, gateway ip (ie: x.x.x.x)
        """
        print 'Setting Gateway to:' + str(value)
        if value is None:
            self._gateway_ipaddr_obj = None
            self._network_gateway_property = None
        else:
            if self.subnet is None:
                raise ValueError('Must set subnet before setting gateway')
            self._validate_ip_string(value)
            ip = ipaddr.IPv4Address(value)
            if not self._subnet_ipaddr_obj.Contains(ip):
                raise ValueError('Gateway:"{0}" not in current subnet value:"{1}"'
                                 .format(value, self.subnet))
            self._check_ip_entry_for_subnet_conflicts(str(ip))
            self._gateway_ipaddr_obj = ip
            self._network_gateway_property.value = str(ip)

    def _validate_addrs_per_net(self, value):
        if value and not math.log(int(value),2)%1:
            return value
        else:
            return None


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
