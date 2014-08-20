#!/usr/bin/env python
from config_manager.eucalyptus import Eucalyptus
from config_manager.eucalyptus.enterprise import Enterprise
from config_manager.eucalyptus.topology import Topology
from config_manager.eucalyptus.topology.cluster import Cluster


eucalyptus = Eucalyptus()
topology = Topology()

eucalyptus.add_repositories(eucalyptus_repo="http://this.is.eucalyptus.repo",
                            euca2ools_repo="http://this.is.euca2ools.repo",
                            enterprise_repo="http://this.is.enterprise.repo")

enterprise = Enterprise()

enterprise.set_credentials(clientkey="myclientkey",
                           clientcert="myclientcert")

eucalyptus.add_enterprise_credentials(enterprise)

cluster1 = Cluster('PARTI00')
cluster2 = Cluster('PARTI01')
topology.add_clusters([cluster1, cluster2])

eucalyptus.add_topology(topology)

print eucalyptus.to_json()
