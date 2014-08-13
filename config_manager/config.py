#!/usr/bin/env python

# Copyright 2009-2014 Eucalyptus Systems, Inc.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

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


class Config(object):
    """
    Intention of this class is to provide utilities around reading and writing
    CLI environment related configuration.
    """
    def __init__(self,
                 name,
                 config_file_path=None,
                 type=None,
                 version=None,
                 **kwargs):
        '''
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
        '''
        self._json_properties = {}
        # Set name and config file path first to allow updating base values
        # from an existing file
        self.add_prop('name', name)
        self.config_file_path = config_file_path
        self.update_from_file()
        #Now overwrite with any params provided
        self.add_prop('type', type)
        self.add_prop('version', version)
        self._setup(**kwargs)

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

    def _get_formatted_conf(self):
        return pformat(vars(self))

    def _get_formatted_conf_from_file(self):
        if self.config_file_path:
            dict = self._get_dict_from_file(self.config_file_path)
            return pformat(dict)

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

    def __repr__(self):
        """
        Default string representation of this object will be the formatted
        json configuration
        """
        return self.to_json()

    def add_prop(self,
                 python_name,
                 value=None,
                 json_name=None,
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
        assert python_name
        json_name = json_name or python_name
        docstring = docstring or "Updates json dict for value:'{0}'"\
            .format(json_name)

        def temp_prop_getter(self):
            return self._get_json_property(json_name)

        def temp_prop_setter(self, newvalue):
            # If a validation callback was provided use it, otherwise
            # allow the user to create a local method named
            # by '_validate_' + the python_name provided which will be
            # called. A validation method is optional but if defined,
            # must return the value to be set for this property.
            validate = validate_callback or getattr(self,
                                                    '_validate_' + python_name,
                                                    None)
            if validate:
                newvalue = validate(newvalue)
            return self._set_json_property(json_name, newvalue)

        def temp_prop_delete(self):
            self._del_json_property(json_name)
        temp_prop = property(fget=temp_prop_getter, fset=temp_prop_setter,
                             fdel=temp_prop_delete, doc=docstring)
        setattr(self.__class__, python_name, temp_prop)
        self._set_json_property(json_name, value)

    def del_prop(self, property_name):
        prop = getattr(self, property_name, None)
        if prop:
            if isinstance(prop, property):
                self.__delattr__(property_name)
            else:
                raise ValueError('{0} is not a "property" of this obj'
                                 .format(property_name))

    def update_from_file(self, file_path=None):
        file_path = file_path or self.config_file_path
        newdict = self._get_dict_from_file(file_path=file_path)
        if newdict:
            self.__dict__.update(newdict)

    #todo define how validation methods for each config subclass should be used
    def validate(self):
        """
        Method to validate configuration. This would likely be checks
        against the aggregate config as individual validation checks
        should be done in each property's setter via the validation_callback
        """
        pass

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
        return '\n'.join(diff)

    def save(self, path=None):
        """
        Will write the json configuration to a file at path or by default at
        self.config_file_path.
        """
        path = path or self.config_file_path
        backup_path = path + '.bak'
        config_json = self.to_json()
        if os.path.isfile(path):
            copyfile(path, backup_path)
        save_file = file(path, "w")
        with save_file:
            save_file.write(config_json)
            save_file.flush()

    def to_json(self):
        """
        converts the local dict '_json_properties{} to json
        """
        return json.dumps(self,
                          default=lambda o: o._json_properties,
                          sort_keys=True,
                          indent=4)
