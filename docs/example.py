#!/usr/bin/env python

import json
from config_manager import Config, Network, Walrus, MidoNet
from config_manager import Cluster, Topology, Eucalyptus, SystemProperties
from config_manager import CloudController, DMJSONEncoder, DefaultAtrributes


# config
#     => attributes
#         => eucalyptus
#             => system_properties
#             => nc
#             => network
#             => enterprise
#             => topology
#                 => clc
#                 => walrus
#                 => user-facing
#                 => clusters
#                     => cluster
#

# build one/multiple clusters
cluster1 = Cluster('PARTI00',
                   cc_hostname='10.111.1.404',
                   sc_hostname='10.111.1.404')

cluster2 = Cluster('PARTI01',
                   cc_hostname='10.111.1.405',
                   sc_hostname='10.111.1.405')

# build a Topology and add Clusters
topology = Topology()
topology.add_cluster([cluster1, cluster2])

clc = CloudController('10.111.100.100')
topology.add_cloud_controller(clc)

walrus = Walrus('10.111.101.100')

# build network and add to Eucalyptus
network = Network()

# add System Properties
system_properties = SystemProperties()
system_properties.add_property('bootstrap.webservices.use_dns_delegation', True)

# build Eucalyptus
eucalyptus = Eucalyptus()
eucalyptus.add_topology(topology)
eucalyptus.add_network(network)
eucalyptus.add_system_properties(system_properties)
## eucalyptus.add_node_controller_params()
## eucalyptus.add_enterprise_credentials()

midonet = MidoNet()


# finally build a config and add Attributes
config = Config()
config.add_midonet(midonet)

# print json.dumps(eucalyptus.to_dict(), cls=DMJSONEncoder, indent=2, sort_keys=True)

print json.dumps(config.to_dict(), cls=DMJSONEncoder, indent=2, sort_keys=True)



