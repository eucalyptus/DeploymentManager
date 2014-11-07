#!/usr/bin/env python
from config_manager.eucalyptus import Eucalyptus
from config_manager.eucalyptus.enterprise import Enterprise
from config_manager.eucalyptus.topology import Topology
from config_manager.eucalyptus.topology.cluster import Cluster
from config_manager.eucalyptus.topology.cluster.nodecontroller import NodeController


eucalyptus = Eucalyptus()
topology = Topology()

eucalyptus.add_repositories(eucalyptus_repo="http://this.is.eucalyptus.repo",
                            euca2ools_repo="http://this.is.euca2ools.repo",
                            enterprise_repo="http://this.is.enterprise.repo")

eucalyptus.set_log_level('INFO')
eucalyptus.set_bind_addr_value(True)
topo = Topology()
eucalyptus.add_topology(topo)
#cluster = topo.create_cluster('CLUSTER1', hypervisor='kvm')
# node_controller = cluster.create_node(ip='1.1.1.1')
# node_controller.max_cores.value = 32
# node_controller.cache_size.value = 10000
#
#
# enterprise = Enterprise()
# enterprise.set_credentials(clientkey="myclientkey",
#                            clientcert="myclientcert")
#
# eucalyptus.add_enterprise_credentials(enterprise)
#
# print "### JSON with Hidden(!) Attributes: ###"
# print eucalyptus.to_json(show_all=True)
# print "\n### Actual JSON: ###"
# print eucalyptus.to_json()
