#!/usr/bin/env python

# Copyright 2009-2014 Eucalyptus Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import json
from pprint import pformat
from shutil import copyfile
import difflib


class ConfigProperty(object):
    def __init__(self,
                 name=None,
                 description=None,
                 version=None,
                 **kwargs):
        self._json_properties = {}
        # Set name and config file path first to allow updating base values
        # from an existing file
        self.name = name
        if not name:
            self.name = self.__class__.__name__.lower()

        self.default_attributes = {}
        #Now overwrite with any params provided
        self.name = self.create_prop('name', self.name)
        self.objtype = self.create_prop('objtype', self.__class__.__name__)
        self.version = self.create_prop('version', version)
        self.description = self.create_prop('description', description)
        # self._setup(kwargs)

    def _setup(self, **kwargs):
        """
        Optional setup method to be implemented by subclasses.
        This method is called by Config.__init__().
        """
        pass

    def _get_json_property(self, property_name):
        """
        helper method for mapping json to python properties
        """
        return self._json_properties[property_name]

    def _set_json_property(self, property_name, value):
        """
        helper method for mapping json to python properties
        """
        self._json_properties[property_name] = value

    def _del_json_property(self, property_name):
        """
        helper method for mapping json to python properties
        """
        if property_name in self._json_properties:
            self._json_properties.pop(property_name)

    def __repr__(self):
        """
        Default string representation of this object will be the formatted
        json configuration
        """
        return self.to_json()

    def create_prop(self,
                 json_name,
                 value=None,
                 docstring=None,
                 validate_callback=None):
        """
        Dynamically add properties which will be used to build json
        representation of this object for configuration purposes. Allows
        values to be accessed as both a local python attribute/property of
        this object, and store that value in a formatted dict for json
        conversion. The setter can also be created with a validation
        method which is called before writing to the json dict storing the
        value. Note that the validator must return the value which will be
        stored. This allows for the value to be formatted/manipulated before
        storing.

        :param python_name: The name of the python property which will be
                            create for this config obj.
        :param json_name: The name used to store the value in self._json_dict
        :param value: optional value to store. Defaults to 'None'
        :param docstring: optional docstring to be used with creating the
                          dynamic python property
        :param validate_callback: optional method, if provided this method can
                                  be used validate or convert the value before
                                  storing.
        Example:
        In [29] def stringcheck(value)
                    assert isinstance(value, str)
                    return value
        In [30] c = Config(name='example')
        In [31] c.add_prop('my_python_string',
                    value='python doesnt like dashes',
                    json_name='my-json-string',
                    docstring='just a string',
                    validate_callback=stringcheck)
        In [32]: print c.my_python_string
        python doesnt like dashes

        In [33]: print c._to_json()
        {
            "my-json-string": "python doesnt like dashes",
            "name": "testconfig",
            "type": null,
            "version": null
        }
        In [34]: c.my_python_string = 'easy to change'

        In [35]: print c.my_python_string
        easy to change

        In [36]: print c._to_json()
        {
            "my-json-string": "easy to change",
            "name": "testconfig",
            "type": null,
            "version": null
        }
        """
        config_obj = self
        docstring = docstring or "Updates json dict for value:'{0}'"\
            .format(json_name)

        def temp_prop_getter():
            return config_obj._get_json_property(json_name)

        def temp_prop_setter(newvalue):
            print 'setting ' + str(json_name) +  ' to value:' + str(newvalue)
            # If a validation callback was provided use it, otherwise
            # allow the user to create a local method named
            # by '_validate_' + the python_name provided which will be
            # called. A validation method is optional but if defined,
            # must return the value to be set for this property.
            validate = validate_callback or getattr(config_obj,
                                                    '_validate_' + json_name,
                                                    None)
            if validate:
                newvalue = validate(newvalue)
            return config_obj._set_json_property(json_name, newvalue)

        def temp_prop_delete():
            config_obj._del_json_property(json_name)
        temp_prop = property(fget=temp_prop_getter, fset=temp_prop_setter,
                             fdel=temp_prop_delete, doc=docstring)
        #setattr(self.__class__, python_name, temp_prop)
        config_obj._set_json_property(json_name, value)
        return temp_prop

    def del_prop(self, property_name):
        prop = getattr(self, property_name, None)
        if not hasattr(prop, 'fdel'):
            raise ValueError('{0} is not a property of this object'
                             .format(property_name))
        if prop:
            prop.fdel(self)
            self.__delattr__(property_name)

    def get_attr_by_json_name(self, json_name):
        for key in self._get_keys():
            attr = getattr(self, key)
            if hasattr(attr, 'fget') and attr.fget() == json_name:
                return attr
        return None

    #todo define how validation methods for each config subclass should be used
    def validate(self):
        """
        Method to validate configuration. This would likely be checks
        against the aggregate config as individual validation checks
        should be done in each property's setter via the validation_callback
        """
        pass

    def to_json(self):
        """
        converts the local dict '_json_properties{} to json
        """
        return json.dumps(self,
                          default=lambda o: o._json_properties,
                          sort_keys=True,
                          indent=4)


class Config(ConfigProperty):
    """
    Intention of this class is to provide utilities around reading and writing
    CLI environment related configuration.
    """
    def __init__(self,
                 name,
                 description=None,
                 config_file_path=None,
                 objtype=None,
                 version=None,
                 **kwargs):
        """
        Creates a base Config() object. This object is a basic python
        representation of a textual configuration(file). This configuration
        is currently described using JSON. This class provides utilities to
        read, write, map, save, compare, and validate python attributes to a
        json configuration.
        :param name: string. The name of this config section
        :param config_file_path: Optional.string. Local path this config obj
                                 should read/write
        :param type: Optional. string. Identifier for this config object.
        :param version: Optional. string. can be used to version a config
        :param kwargs: Optional set of key word args which will be passed to
                       to the local user defined _setup() method.
        """
        # Set name and config file path first to allow updating base values
        # from an existing file
        super(Config, self).__init__(name=name,
                                     description=description,
                                     objtype=objtype,
                                     version=version,
                                     kwargs=kwargs)
        self.config_file_path = config_file_path
        self.update_from_file()
        self.default_attributes = {}

    def _get_formatted_conf(self):
        return pformat(vars(self))

    def _get_keys(self):
        return vars(self).keys()

    def _get_dict_from_file(self, file_path=None):
        """
        Attempts to read in json from an existing file, load and return as
        a dict
        """
        file_path = file_path or self.config_file_path
        newdict = None
        if os.path.exists(str(file_path)) and os.path.getsize(str(file_path)):
            if not os.path.isfile(file_path):
                raise ValueError('config file exists at path and is not '
                                 'a file:' + str(file_path))
            conf_file = open(file_path, 'rb')
            with conf_file:
                data = conf_file.read()
            if data:
                try:
                    newdict = json.loads(data)
                except ValueError as ve:
                    ve.args = (['Failed to load json config from: "{0}". '
                                'ERR: "{1}"'.format(file_path, ve.message)])
                    raise
        return newdict

    def update_from_file(self, file_path=None):
        file_path = file_path or self.config_file_path
        if not file_path:
            return
        newdict = self._get_dict_from_file(file_path=file_path)
        if newdict:
            for key in newdict:
                value = newdict[key]
                if not key in self._json_properties:
                    print ('warning "{0}" not found in json properties for '
                           'class: "{1}"'.format(key, self.__class__))
                else:
                    attr = self.get_attr_by_json_name(key)
                    if not attr:
                        print 'warning local attribute with json_name "{0}" ' \
                              'not found'.format(key)
                    else:
                        attr.fset(value)

    #todo define how/if this method should be used, examples, etc..
    def send(self, filehandle=None):
        """
        Method which defines how, where, when etc a config should be written.
        For writing to a local path use self.save(), this method is a
        placeholder for possibly writing to a remote server, or submitting
        the json configuration to another process, etc..
        """
        pass

    def diff(self, file_path=None):
        """
        Method to show current values vs those (saved) in a file.
        Will return a formatted string to show the difference
        """
        #Create formatted string representation of dict values
        text1 = self.to_json().splitlines()
        #Create formatted string representation of values in file
        file_path = file_path or self.config_file_path
        file_dict = self._get_dict_from_file(file_path=file_path) or {}
        text2 = json.dumps(file_dict, sort_keys=True, indent=4).splitlines()
        diff = difflib.unified_diff(text2, text1, lineterm='')
        return str('\n'.join(diff))

    def save(self, path=None):
        """
        Will write the json configuration to a file at path or by default at
        self.config_file_path.
        """
        path = path or self.config_file_path
        if not path:
            raise ValueError('Path/config_file_path has not been set '
                             'or provided.')
        backup_path = path + '.bak'
        config_json = self.to_json()
        if os.path.isfile(path):
            copyfile(path, backup_path)
        save_file = file(path, "w")
        with save_file:
            save_file.write(config_json)
            save_file.flush()



    def add_config(self, service_config):
        self.default_attributes.update(
            {service_config.__class__.__name__.lower(): service_config}
        )

    def to_dict(self):
        return dict(name=self.name,
                    description=self.description,
                    default_attributes=self.default_attributes)


class DMJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()
        else:
            return json.JSONEncoder.default(self, obj)

