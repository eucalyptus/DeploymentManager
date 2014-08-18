#!/usr/bin/env python

from config_manager.eucalyptus import Eucalyptus
from config_manager.eucalyptus.topology import Topology
from config_manager.eucalyptus.topology.cluster import Cluster

topology = Topology(name='topo')

cluster1 = Cluster('one')
cluster2 = Cluster('two')

topology.add_clusters([cluster1, cluster2])

# print topology

eucalyptus = Eucalyptus()
eucalyptus.log_level.value = 'DEBUG'
eucalyptus.eucalyptus_repo.value = 'this://iseucalyptus.repo'
eucalyptus.euca2ools_repo.value = 'this://iseuca2ools.repo'
eucalyptus.enterprise_repo.value = 'this://isenterprise.repo'
eucalyptus.enterprise.value = {'clientcert': 'temp'}
eucalyptus.nc.value = {'max-cores': 16}
eucalyptus.network.value = {'temp': 'temp network value'}

eucalyptus.system_properties.value = {
    'bootstrap.webservices.use_dns_delegation': True,

}


eucalyptus.topology.value = topology

print topology

# print eucalyptus
#
# print "================\n\n"
#
# print eucalyptus.to_json()
