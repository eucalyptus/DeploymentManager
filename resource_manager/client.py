#!/usr/bin/python
import json
import urllib
import requests
import argparse
from prettytable import PrettyTable


class RequestFailureException(Exception):
    def __init__(self, response):
        self.response = response

    def __str__(self):
        status_code = self.response.status_code
        text = self.response.text
        return "{0}:{1}".format(status_code, text)


class ResourceManagerClient(object):
    FIELDS = {'machines': ["hostname", "owner", "_updated", "_id"],
              'private-addresses': ["address", "owner", "_updated", "_id"],
              'public-addresses': ["address",  "owner", "_updated", "_id"]}

    def __init__(self, resource_type='machines', endpoint='http://127.0.0.1:5000', username='admin', password='admin'):
        self.endpoint = endpoint + '/' + resource_type
        self.resource_type = resource_type
        self.key = self.FIELDS[self.resource_type][0]
        self.auth = (username, password)
        self.headers = {'content-type': 'application/json'}
        self.fields = self.FIELDS[self.resource_type]

    def create_resource(self, resource):
        resource = requests.post(self.endpoint, data=resource, headers=self.headers, auth=self.auth)
        if resource.status_code != 201:
            raise RequestFailureException(resource)

    def get_resource(self, name):
        url = self.endpoint + '/' + urllib.quote_plus(name)
        return requests.get(url, auth=self.auth).json()

    def update_resource(self, resource):
        resource_name = json.loads(resource)[self.key]
        server_response = self.get_resource(resource_name)
        identifier = server_response['_id']
        etag = server_response['_etag']
        request_url = self.endpoint + "/" + identifier
        headers = self.headers
        headers['If-Match'] = etag
        updated_resource = requests.patch(request_url, data=resource, headers=self.headers, auth=self.auth)
        if updated_resource.status_code != 200:
            raise RequestFailureException(updated_resource)

    def delete_resource(self, resource):
        resource_name = json.loads(resource)[self.key]
        server_response = self.get_resource(resource_name)
        identifier = server_response['_id']
        etag = server_response['_etag']
        request_url = self.endpoint + "/" + identifier
        headers = self.headers
        headers['If-Match'] = etag
        deleted_resource = requests.delete(request_url, data=resource, headers=self.headers, auth=self.auth)
        if deleted_resource.status_code != 200:
            raise RequestFailureException(deleted_resource)

    def print_resources(self):
        items = requests.get(self.endpoint, auth=self.auth).json()["_items"]
        table = PrettyTable(self.fields)
        for resource in items:
            table.add_row([resource.get(field, None) for field in self.fields])
        print table.get_string(fields=self.fields)

if __name__ == "__main__":
    resources = ['machines', 'public-addresses', 'private-addresses']
    operations = ['create', 'list', 'update', 'delete']
    parser = argparse.ArgumentParser(description='Access resource manager api.')
    parser.add_argument('operation', choices=operations)
    parser.add_argument('--resource-type', '-r', default="machines", help='Resource type to query',
                        choices=resources)
    parser.add_argument('--endpoint', '-e', help='API endpoint to connect to', default='http://127.0.0.1:5000')
    parser.add_argument('--json', '-j', help='JSON defining object to add/remove')
    args = parser.parse_args()
    client = ResourceManagerClient(args.resource_type, args.endpoint)
    if args.operation == 'create':
        client.create_resource(args.json)
    elif args.operation == 'list':
        client.print_resources()
    elif args.operation == 'update':
        client.update_resource(args.json)
    elif args.operation == 'delete':
        client.delete_resource(args.json)
    else:
        raise Exception("Unknown Command")
