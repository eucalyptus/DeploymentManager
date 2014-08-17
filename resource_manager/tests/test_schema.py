from resource_manager.api_config import ResourceSchema
from resource_manager.api_config import PAGINATION, RESOURCE_METHODS, ITEM_METHODS, lookup_url


def test_load():
    assert PAGINATION is False
    assert RESOURCE_METHODS == ['GET', 'POST', 'DELETE']
    assert ['GET', 'PATCH', 'PUT', 'DELETE'] == ITEM_METHODS
    assert lookup_url == 'regex("[\w-]+")'


def test_machine_keys():
    schema = ResourceSchema().machine_schema
    assert 'hostname' in schema
    assert 'owner' in schema
    assert 'state' in schema


def test_machine_required():
    schema = ResourceSchema().machine_schema
    assert schema['hostname']['required']
    assert schema['state']['required']


def test_machine_unique():
    schema = ResourceSchema().machine_schema
    assert schema['hostname']['unique']


def test_machine_states():
    schema = ResourceSchema().machine_schema
    assert schema["state"]['allowed'] == ["pxe", "pxe_failed", "idle", "in_use", "needs_repair"]


def test_address_keys():
    schema = ResourceSchema().address_schema
    assert 'address' in schema
    assert 'owner' in schema


def test_address_required():
    schema = ResourceSchema().address_schema
    assert schema['address']['required']


def test_address_unique():
    schema = ResourceSchema().address_schema
    assert schema['address']['unique']