__author__ = 'clarkmatthew'

import json


class Namespace(object):
    """
    Convert dict (if provided) into attributes and return a somewhat
    generic object
    """
    def __init__(self, newdict=None):
        if newdict:
            for key in newdict:
                value = newdict[key]
                try:
                    if isinstance(value, dict):
                        setattr(self, Namespace(value), key)
                    else:
                        setattr(self, key, value)
                except:
                    print '"{0}" ---> "{1}" , type: "{2}"'.format(key,
                                                                  value,
                                                                  type(value))
                    raise

    def _get_keys(self):
        return vars(self).keys()

    def _to_json(self):
        return json.dumps(self,
                          default=lambda o: o.__dict__,
                          sort_keys=True,
                          indent=4)
