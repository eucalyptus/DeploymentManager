#!/usr/bin/env python
from config_manager.eucalyptus import Eucalyptus
from config_manager.eucalyptus.enterprise import Enterprise
from config_manager.eucalyptus.topology import Topology
from config_manager.eucalyptus.topology.cluster import Cluster
from config_manager.eucalyptus.topology.cluster.nodes import NodeController


eucalyptus = Eucalyptus()
topology = Topology()

eucalyptus.add_repositories(eucalyptus_repo="http://this.is.eucalyptus.repo",
                            euca2ools_repo="http://this.is.euca2ools.repo",
                            enterprise_repo="http://this.is.enterprise.repo")

eucalyptus.set_log_level('INFO')
eucalyptus.set_bind_addr_value(True)

node_controller = NodeController()
node_controller.max_cores.value = 32
node_controller.cache_size.value = 10000

eucalyptus.node_controller_properties(node_controller)

enterprise = Enterprise()
enterprise.set_credentials(clientkey="myclientkey",
                           clientcert="myclientcert")

eucalyptus.add_enterprise_credentials(enterprise)

cluster1 = Cluster('PARTI00')
cluster2 = Cluster('PARTI01')
topology.add_clusters([cluster1, cluster2])

eucalyptus.add_topology(topology)

print eucalyptus.to_json()
