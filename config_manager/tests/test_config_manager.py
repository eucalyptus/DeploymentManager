from config_manager.eucalyptus.network import Network
from config_manager.eucalyptus.packages import Packages
from config_manager.eucalyptus import Eucalyptus
from config_manager.eucalyptus.topology import Topology
from mock import mock_open


def test_init():
    Eucalyptus()


def test_setters():
    eucalyptus = Eucalyptus()
    log_level = "TEST-LEVEL"
    eucalyptus.set_log_level(log_level)
    assert eucalyptus.log_level.value == log_level


def test_add_topology():
    eucalyptus = Eucalyptus()
    topology = Topology(name="Test Topo")
    eucalyptus.add_topology(topology)
    assert eucalyptus.topology.name is topology.name


def test_add_package_config():
    eucalyptus = Eucalyptus()
    eucalyptus_repo = 'eucalyptus-repo'
    euca2ools_repo = 'euca2ools-repo'
    packages = Packages(eucalyptus_repo, euca2ools_repo)
    eucalyptus.add_packages(packages)
    assert eucalyptus.eucalyptus_repo == eucalyptus_repo
    assert eucalyptus.euca2ools_repo == euca2ools_repo


def test_add_network():
    eucalyptus = Eucalyptus()
    network_json = '{}'
    network_json_file = mock_open()
    network = Network(network_json_file, network_json)
    eucalyptus.add_network(network)
