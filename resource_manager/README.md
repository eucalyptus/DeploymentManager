ResourceManager
======================

ResourceManager is a client library and REST API to control the allocation of resources within a datacenter. The library
requires a MongoDB database for persisting data.

Some example use cases for ResourceManager are tracking IP addresses/ranges, SAN connections, or machine allocations.

Quick Start - CentOS 6
------
* Install Chef:  ```curl -L https://www.opscode.com/chef/install.sh | bash```
* Download the [cookbook tarball](https://github.com/viglesiasce/resource-manager-cookbook/releases/download/0.2.0/resource-man-cookbooks.tgz)
* Run Chef: ```chef-solo -r resource-man-cookbooks.tgz -o 'recipe[resource-manager]'```

Managing the Server
------
As seen in the above cookbook, the server.py is run via supervisord.  This
means the log output is collected in supervisor logs, located in
/var/log/supervisor/, example:

    [root@localhost DeploymentManager]# tail /var/log/supervisor/resource-manager-api-stderr---supervisor-MLLTh7.log
    10.111.4.180 - - [06/Apr/2017 07:41:01] "GET /machines HTTP/1.1" 200 -
    10.111.4.181 - - [06/Apr/2017 07:49:12] "GET /machines HTTP/1.1" 200 -
    10.111.4.181 - - [06/Apr/2017 07:49:13] "GET /machines HTTP/1.1" 200 -
    10.111.4.180 - - [06/Apr/2017 07:51:02] "GET /machines HTTP/1.1" 200 -
    10.5.1.14 - - [06/Apr/2017 07:57:06] "GET /machines/a-15-r.qa1.eucalyptus-systems.com HTTP/1.1" 200 -
    10.5.1.14 - - [06/Apr/2017 07:57:06] "PUT /machines/577431f2421aa904db05a7df HTTP/1.1" 422 -
    10.5.1.14 - - [06/Apr/2017 07:57:52] "GET /machines/a-15-r.qa1.eucalyptus-systems.com HTTP/1.1" 200 -
    10.5.1.14 - - [06/Apr/2017 07:57:52] "PUT /machines/577431f2421aa904db05a7df HTTP/1.1" 200 -
    10.5.1.14 - - [06/Apr/2017 07:58:03] "GET /machines/a-15-r.qa1.eucalyptus-systems.com HTTP/1.1" 200 -
    10.111.4.180 - - [06/Apr/2017 08:01:01] "GET /machines HTTP/1.1" 200 -

To start or stop the server run 'supervisorctl', example showing status here:

    [root@localhost DeploymentManager]# supervisorctl status resource-manager-api
    resource-manager-api             RUNNING   pid 12552, uptime 1:01:59

Installation
------
* [Install MongoDB](http://www.mongodb.org/downloads)
* Run mongodb
* Clone this repository
* Install python dependencies: ```pip install Flask Flask-Bootstrap eve PrettyTable argparse requests```
* Run the server: ```cd resource_manager;./server.py```
* (If running in a virtualenv, run the command: ```. venv/bin/activate; cd resource_manager; python server.py```)


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

