#!/usr/bin/env python

import json

from config_manager.config import BaseConfig
from config_manager.eucalyptus.enterprise import Enterprise
from config_manager.eucalyptus.packages import Packages
from config_manager.eucalyptus.system_properties import SystemProperties
from config_manager.eucalyptus.network import Network
from config_manager.eucalyptus import Eucalyptus
from config_manager.eucalyptus.topology import Topology
from config_manager.eucalyptus.topology.cloud_controller import CloudController
from config_manager.eucalyptus.topology.ufs import UserFacingServices
from config_manager.eucalyptus.topology.walrus import Walrus
from config_manager.eucalyptus.topology.cluster import Cluster
from config_manager.config import DMJSONEncoder

topology = Topology()

# build one/multiple clusters
cluster1 = Cluster('PARTI00',
                   cc_hostname='10.111.1.404',
                   sc_hostname='10.111.1.404')

cluster2 = Cluster('PARTI01',
                   cc_hostname='10.111.1.405',
                   sc_hostname='10.111.1.405')

clc = CloudController('10.111.100.201')
walrus = Walrus('10.111.101.200')
ufs = UserFacingServices(["10.111.100.202", "10.111.100.203"])

topology.add_user_facing_services(ufs)
topology.add_cluster([cluster1, cluster2])
topology.add_cloud_controller(clc)
topology.add_walrus(walrus)

# build network and add to Eucalyptus
network = Network()

# add System Properties
system_properties = SystemProperties()
system_properties.add_property('bootstrap.webservices.use_dns_delegation', True)

enterprise = Enterprise(clientcert="much/cert", clientkey="such/key")

packages = Packages(eucalyptus_repo='http://release-repo.eucalyptus-systems.com/'
                                    'releases/eucalyptus/4.0/centos/6/x86_64/',
                    euca2ools_repo='http://release-repo.eucalyptus-systems.com/'
                                   'releases/euca2ools/3.1/centos/6/x86_64/')

# build Eucalyptus
eucalyptus = Eucalyptus()
eucalyptus.set_log_level('DEBUG')
eucalyptus.add_topology(topology)
eucalyptus.add_network(network)
eucalyptus.add_system_properties(system_properties)
# eucalyptus.add_node_controller_params()
eucalyptus.add_enterprise_credentials(enterprise)
eucalyptus.add_packages(packages)

# finally build a config and add Attributes
config = BaseConfig('my-awesome-config', description='my awesome config')
config.add_config(eucalyptus)

# print json.dumps(eucalyptus.to_dict(),
#                  cls=DMJSONEncoder,
#                  indent=2, sort_keys=True)

print json.dumps(config.to_dict(), cls=DMJSONEncoder, indent=2, sort_keys=True)
