#!/usr/bin/python
from eve import Eve
from eve.auth import BasicAuth
from flask_bootstrap import Bootstrap
from eve_docs import eve_docs


class ResourceManagerBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        if method == 'GET':
            # Allow read-only access without a password
            return True
        else:
            # all the other resources are secured
            return username == 'admin' and password == 'admin'

app = Eve(settings="./api_config.py", auth=ResourceManagerBasicAuth)
Bootstrap(app)
app.register_blueprint(eve_docs, url_prefix='/docs')
app.run(host='0.0.0.0')
