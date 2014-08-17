import json
import httpretty
import urllib

from resource_manager.client import ResourceManagerClient


def test_init():
    ResourceManagerClient()


def test_defaults(resource='machines'):
    client = ResourceManagerClient(resource)
    assert client.resource_type == resource
    defaults = dict(endpoint='http://127.0.0.1:5000/machines', resource_type='machines', key='hostname',
                    auth=('admin', 'admin'), headers={'content-type': 'application/json'},
                    fields=["hostname", "owner", "state", "job_id", "_updated", "_id"])
    for attribute, value in defaults.iteritems():
        try:
            assert value == client.__getattribute__(attribute)
        except AssertionError:
            raise AssertionError("Default for {0} should be:{1}\n"
                                 "Received: {2}".format(attribute, client.__getattribute__(attribute), value))


@httpretty.activate
def test_get():
    client = ResourceManagerClient()
    resource = 'test_machine'
    response_body = '{"_id": "my_id"}'
    httpretty.register_uri(httpretty.GET, client.endpoint + "/" + resource,
                           body=response_body)
    assert client.get_resource(resource) == json.loads(response_body)


@httpretty.activate
def test_create():
    client = ResourceManagerClient()
    resource = "{\"hostname\":\"resource\"}"
    httpretty.register_uri(httpretty.POST, client.endpoint, status=201)
    client.create_resource(resource)


@httpretty.activate
def test_delete():
    client = ResourceManagerClient()
    resource = "{\"hostname\":\"resource\"}"
    response_body = '{"_id": "my_id", "_etag":"2341341234"}'
    httpretty.register_uri(httpretty.GET, client.endpoint + "/resource",
                           body=response_body)
    response_body = '{"_id": "my_id"}'
    httpretty.register_uri(httpretty.DELETE, client.endpoint + "/my_id",
                           body=response_body)
    client.delete_resource(resource)


@httpretty.activate
def test_update():
    client = ResourceManagerClient()
    resource = "{\"hostname\":\"resource\"}"
    response_body = '{"_id": "my_id", "_etag":"2341341234"}'
    httpretty.register_uri(httpretty.GET, client.endpoint + "/resource",
                           body=response_body)
    response_body = '{"_id": "my_id"}'
    httpretty.register_uri(httpretty.PATCH, client.endpoint + "/my_id",
                           body=response_body)
    client.update_resource(resource)


@httpretty.activate
def test_find_resources():
    client = ResourceManagerClient()
    field = 'some_field'
    value = 'some_value'
    url = client.endpoint + "?where=" + field + "==" + urllib.quote("\"" + value + "\"")
    response_body = "{}"
    httpretty.register_uri(httpretty.GET, url, body=response_body)
    client.find_resources(field, value)


@httpretty.activate
def test_get_all_resources():
    client = ResourceManagerClient()
    url = client.endpoint
    response_body = "{\"_items\":[]}"
    httpretty.register_uri(httpretty.GET, url, body=response_body)
    assert isinstance(client.get_all_resources(), list)
