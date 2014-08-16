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

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup


setup(name='deploymentmanager',
      version='0.1',
      description='Eucalyptus Deployment and Configuration Management tools',
      url='https://github.com/eucalyptus/DeploymentManager.git',
      license='Apache License 2.0',
      packages=find_packages(),
      install_requires=['paramiko', 'PrettyTable', 'eve', 'Flask',  'requests',
                        'Flask-Bootstrap', 'eve', 'PrettyTable', 'argparse'],
      tests_require=['nose', 'httpretty'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 1 - Alpha",
          "Topic :: Utilities",
          "Environment :: Console",
      ],
)
