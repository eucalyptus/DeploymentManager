#!/usr/bin/env python

import json
from configmanager import DeploymentManager, Config, DMJSONEncoder
from configmanager import Clusters, Cluster

config = Config()
print json.dumps(config.to_dict(), cls=DMJSONEncoder)

clusters = Clusters()

cluster = Cluster('PARTI00')
# print cluster



