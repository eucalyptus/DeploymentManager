from pxe_manager.pxemanager import PxeManager
from resource_manager.client import ResourceManagerClient
import httpretty

@httpretty.activate
def test_defaults():
    client = ResourceManagerClient()
    cobbler_url = "http://cobbler.example.com/cobbler_api"
    cobbler_user = "user"
    cobbler_password = "password"
    response_body = '''<?xml version="1.0"?>
                        <methodResponse>
                           <params>
                              <param>
                                 <value><string>Some Value</string></value>
                                </param>
                            </params>
                        </methodResponse>
    '''
    distro_map = {'esxi51': 'qa-vmwareesxi51u0-x86_64',
                  'esxi50': 'qa-vmwareesxi50u1-x86_64',
                  'centos': 'qa-centos6-x86_64-striped-drives',
                  'rhel': 'qa-rhel6u5-x86_64-striped-drives'}
    httpretty.register_uri(httpretty.POST, cobbler_url,
                           body=response_body)
    pxe_manager = PxeManager(cobbler_url, cobbler_user, cobbler_password, client)
    for key, value in distro_map.iteritems():
        assert pxe_manager.distro[key] == value