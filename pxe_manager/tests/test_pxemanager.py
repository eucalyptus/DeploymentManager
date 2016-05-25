from pxe_manager.pxemanager import PxeManager
from resource_manager.client import ResourceManagerClient
import httpretty


@httpretty.activate
def test_defaults():
    host_client = ResourceManagerClient()
    pub_ip_client = ResourceManagerClient(resource_type='public-addresses')
    priv_ip_client = ResourceManagerClient(resource_type='private-addresses')
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
    distro_map = {'centos': 'centos6-x86_64-raid0',
                  'rhel': 'rhel6u6-x86_64-raid0',
                  'centos7': 'centos7-x86_64-raid0',
                  'centos70': 'centos7u0-x86_64-raid0',
                  'rhel7': 'rhel7-x86_64-raid0'}
    httpretty.register_uri(httpretty.POST, cobbler_url,
                           body=response_body)
    pxe_manager = PxeManager(cobbler_url, cobbler_user, cobbler_password, host_client, pub_ip_client, priv_ip_client)
    for key, value in distro_map.iteritems():
        assert pxe_manager.distro[key] == value
