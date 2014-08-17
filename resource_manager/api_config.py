RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
PAGINATION = False
lookup_url = 'regex("[\w-]+")'


class ResourceSchema(object):
    machine_schema = {
        'hostname': {
            'type': 'string',
            'required': True,
            'unique': True

        },
        'owner': {
            'type': 'string'
        },
        'state': {
            'type': 'string',
            'required': True,
            'allowed': ["pxe", "pxe_failed", "idle", "in_use", "needs_repair"]
        },
        'job_id': {
            'type': 'string'
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

    machines = {
        'item_title': 'machine',
        'additional_lookup': {
            'url': lookup_url,
            'field': 'hostname'
        },
        'schema': machine_schema
    }

    public_addresses = {
        'item_title': 'public-address',
        'additional_lookup': {
            'url': lookup_url,
            'field': 'address'
        },
        'schema': address_schema
    }

    private_addresses = {
        'item_title': 'private-address',
        'additional_lookup': {
            'url': lookup_url,
            'field': 'address'
        },
        'schema': address_schema
    }


schema = ResourceSchema()
DOMAIN = {
    'machines': schema.machines,
    'public-addresses': schema.public_addresses,
    'private-addresses': schema.private_addresses
}
