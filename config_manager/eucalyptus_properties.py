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

from namespace import Namespace
import config_manager


class EucalyptusProperty(object):

    def __init__(self,
                 name,
                 properties_manager,
                 value=None,
                 validate_callback=None,
                 reset_callback=None,
                 default_value=config_manager.DEFAULT_NOT_DEFINED):
        assert isinstance(properties_manager, EucalyptusProperties)
        self._value = None
        self.properties_manager = properties_manager
        self.name = name
        if validate_callback:
            self.validate = validate_callback
        if reset_callback:
            self.reset = reset_callback
        self.value = value
        self.default_value = default_value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, newvalue):
        newvalue = self.validate(newvalue)
        self._value = newvalue

    def delete(self):
        self.configmanager.delete_eucalyptus_property(self)

    def validate(self, value):
        return value

    def reset_to_default(self):
        if self.default_value == self.DEFAULT_NOT_DEFINED:
            return
        else:
            self.value = self.default_value

    def update(self):
        value = self.validate(self.value)

    def __repr__(self):
        val_str = str(self.value)
        return '{0}:(:"{1}", "{2}")'.format(self.__class__.__name__,
                                            self.name,
                                            val_str)


class EucalyptusProperties(Namespace):

    def __setattr__(self, key, value):
        # Set some constraints/checks for handling EucalyptusProperty attributes
        if isinstance(value, EucalyptusProperty):
            propertyobj = value
            if self.get_property_by_property_string(propertyobj.name):
                raise ValueError("Property already exists with name:'{0}'".format(propertyobj.name))
        if self.get_property_by_name(key):
            raise ValueError('EucalyptusProperty obj is ready only, did you mean: '
                             '"{0}.value = {1}" ?'.format(key, value))
        self.__dict__[key] = value

    def create_property(self,
                        name,
                        property_string,
                        value=None,
                        validate_callback=None,
                        reset_callback=None,
                        default_value=config_manager.DEFAULT_NOT_DEFINED):
        if getattr(self, name, None):
            raise ValueError('EucalyptusProperties object has existing property with name:"{0}"'
                             .format(name))
        self.__setattr__(name, EucalyptusProperty(name=property_string,
                                                  properties_manager=self,
                                                  value=value,
                                                  validate_callback=validate_callback,
                                                  reset_callback=reset_callback,
                                                  default_value=default_value))

    def get_property_by_name(self, name):
        props = self.get_all_properties(name)
        if props:
            return props[0]
        return None

    def get_property_by_property_string(self, property_string):
        props = self.get_all_properties(property_string=property_string)
        if props:
            return props[0]
        return None

    def get_all_properties(self, name=None, property_string=None):
        props = []
        for key in self._get_keys():
            # First sort out by the attribute's name if name was provided as a filter
            if name is not None and key != name:
                continue
            attr = self.__getattribute__(key)
            if isinstance(attr, EucalyptusProperty):
                # Filter out matching property_strings if property_string was provided as a filter
                if property_string is not None and attr.name != property_string:
                    continue
                props.append(attr)
        return props

    def delete_property(self, name=None, property_string=None):
        prop = self.get_property(name)
        if prop:
            self.__delattr__(name)

    def get_eucalyptus_property_dict(self, show_all=True):
        prop_dict = {}
        for prop in self.get_all_properties():
            if show_all or prop.value is not None:
                prop_dict[prop.name] = prop.value
        return prop_dict
