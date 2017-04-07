#!/usr/bin/python
#
# This is a sample script which was used to update tags documents in the
# mongodb from information collected from the machines (memory), and a table
# of other attributes provided by Kyle.  This can be modified to update any
# information in the mongodb, but obviously is not a generic script.
#
import json
import re

from resource_manager.client import ResourceManagerClient

# newhosts is a json formatted file of hosts and memory collected from nephoria
# newhosts looks like this (for future reference):
# (venv) [mbacchi@centos7 resource_manager]$ cat /home/mbacchi/repos/nephoria/newhosts.json | jq
#{
#  "hosts": {
#    "a-01-l.qa1.eucalyptus-systems.com": "131823348",
#    "a-36.qa1.eucalyptus-systems.com": "16255048",
#    "a-37.qa1.eucalyptus-systems.com": "16255048",
# ...
# }
#}
newhosts = "/home/mbacchi/repos/nephoria/newhosts.json"

if __name__ == "__main__":

    # These values for memory were given to me by Kyle Wade 3/13/2017
    # Some values he gave were partial (R210 vs. R210II) so I didn't add information
    # unless it was absolutely clear that the whole class of machines had a
    # specific attribute.
    memtable = {'a-xx': {'regex': "a-\d\d.qa1.eucalyptus-systems.com", 'mem': 17179869184,
                         'cpucores': 4, 'interfaces': [{'ratembps': 1000}]},
                'b-xx': {'regex': "b-\d\d.qa1.eucalyptus-systems.com", 'mem': 17179869184,
                         'cpucores': 4, 'interfaces': [{'ratembps': 1000}]},
                'c-xx': {'regex': "c-\d\d.qa1.eucalyptus-systems.com", 'mem': 17179869184,
                         'cpucores': 4, 'interfaces': [{'ratembps': 1000}]},
                'd-xx': {'regex': r'd-\d\d.qa1.eucalyptus-systems.com', 'mem': 17179869184,
                         'cpucores': 4, 'interfaces': [{'ratembps': 1000}]},
                'e-xx': {'regex': r'e-\d\d.qa1.eucalyptus-systems.com', 'mem': 17179869184,
                         'cpucores': 4},
                'g-xx-xx': {'regex': r'g-\d\d-\d\d.qa1.eucalyptus-systems.com', 'mem': 8589934592,
                            'cpucores': 2, 'cpumhz': 2200,
                            'interfaces': [{'ratembps': 1000}, {'ratembps': 1000}]},
                'h-xx': {'regex': r'h-\d\d.qa1.eucalyptus-systems.com', 'mem': 68719476736,
                         'cpucores': 8, 'cpumhz': 2400},
                'a-xx-x': {'regex': r'a-\d\d-\w.qa1.eucalyptus-systems.com', 'mem': 137438953472,
                           'cpucores': 8, 'cpumhz': 2600,
                           'interfaces': [{'ratembps': 10000}]}
                }

    with open(newhosts, "r") as file:
        collected = json.loads(file.read())

    #client = ResourceManagerClient(endpoint="http://10.111.4.100:5000")  #  PRODUCTION
    client = ResourceManagerClient(endpoint="http://127.0.0.1:5000") # USE "http://10.111.4.100:5000" for production
    ourlist = client.get_all_resources()
    for item in ourlist:
        machine = client.get_resource(item['hostname'])  #  PRODUCTION
        for mtype in memtable:
            match = re.search(memtable[mtype]['regex'], item['hostname'])
            if match:
                if 'tags' not in machine.keys():
                    machine[u'tags'] = {}
                if item['hostname'] in collected['hosts'].keys():
                    print "{}: updating to {} (collected) (vs {} table)".format(
                        item['hostname'],
                        int(collected['hosts'][item['hostname']])*1024,
                        memtable[mtype]['mem'])
                    machine[u'tags'][u'memory'] = int(collected['hosts'][item['hostname']])*1024  #  PRODUCTION
                else:
                    print "{}: updating to {} (table)".format(item['hostname'],
                                                              memtable[mtype]['mem'])
                    machine[u'tags'][u'memory'] = memtable[mtype]['mem']  #  PRODUCTION
                if 'cpucores' in memtable[mtype].keys():
                    print "cpucores: {}".format(memtable[mtype]['cpucores'])
                    machine[u'tags'][u'cpucores'] = memtable[mtype]['cpucores']  #  PRODUCTION
                if 'cpumhz' in memtable[mtype].keys():
                    print "cpumhz: {}".format(memtable[mtype]['cpumhz'])
                    machine[u'tags'][u'cpumhz'] = memtable[mtype]['cpumhz']  #  PRODUCTION
                if 'interfaces' in memtable[mtype].keys():
                    for i in memtable[mtype]['interfaces']:
                        print "interface: {} mbps".format(i['ratembps'])
                    machine[u'tags'][u'interfaces'] = memtable[mtype]['interfaces']  #  PRODUCTION
        machine.pop('_updated')  #  PRODUCTION
        machine.pop('_etag')  #  PRODUCTION
        machine.pop('_created')  #  PRODUCTION
        machine.pop('_links')  #  PRODUCTION
        print "Performing client.put_resource(json.dumps({}))".format(item['hostname'])

        # WARNING!! - DON'T ENABLE THIS UNLESS YOU WANT TO UPDATE YOUR DB!!!!
        #client.put_resource(json.dumps(machine))  #  PRODUCTION
