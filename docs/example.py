#!/usr/bin/env python

import json
from config_manager import DeploymentManager, Config, DMJSONEncoder
from config_manager import Clusters, Cluster

config = Config()
print json.dumps(config.to_dict(), cls=DMJSONEncoder)

clusters = Clusters()

cluster = Cluster('PARTI00')
# print cluster



