ResourceManager
======================

ResourceManager is a client library and REST API to control the allocation of resources within a datacenter. The library
requires a MongoDB database for persisting data.

Some example use cases for ResourceManager are tracking IP addresses/ranges, SAN connections, or machine allocations.

Quick Start - CentOS 6
------
* Install Chef:  ```curl -L https://www.opscode.com/chef/install.sh | bash```
* Download the [cookbook tarball](https://github.com/viglesiasce/resource-manager-cookbook/releases/download/0.1.0/resource-man-cookbooks.tgz)
* Run Chef: ```chef-solo -r resource-man-cookbooks.tgz -o 'recipe[resource-manager]'```

Installation
------
* [Install MongoDB](http://www.mongodb.org/downloads)
* Run mongodb
* Clone this repository
* Install python dependencies: ```pip install Flask Flask-Bootstrap eve PrettyTable```
* Run the server: ```cd resource_manager;./server.py```


Data Layout in DB
------
Data is persisted in MongoDB which is a JSON document data store. Machines, public addresses and private
addresses are currently implemented. Public and private addresses share the same schema:

    machine_schema = {
        'hostname': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'owner': {
            'type': 'string'
        },
        'state': {
            'type': 'string',
            'allowed': ["pxe", "pxe_failed","idle","needs_repair"]
        }
    }

    address_schema = {
        'address': {
            'type': 'string',
            'required': True,
            'unique': True,
        },
        'owner': {
            'type': 'string'
        }
    }

Interacting with the server
------
A sample client CLI has been constructed in client.py that allows for CRUD operations as follows

    ### List machines (default resource type)
    ./client.py list

    ### Add a machine
    ./client.py create --json '{"hostname":"my-machine", "owner": "tony"}'

    ### Update a machine
    ./client.py update --json '{"hostname":"my-machine", "owner": ""}'

    ### Delete a machine
    ./client.py create --json '{"hostname":"my-machine"}'

    ### List public addresses
    ./client.py list -r public-addresses

This client can also be accessed programatically as a library as follows:

    from resource_manager.client import ResourceManagerClient
    client = ResourceManagerClient()
    client.print_resources()

