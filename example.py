import json
from deploymentmanager import DeploymentManager, Config, DMJSONEncoder

dm = DeploymentManager()

config = Config()
print json.dumps(config.to_dict(), cls=DMJSONEncoder)