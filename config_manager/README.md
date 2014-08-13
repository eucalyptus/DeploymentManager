Config Manager
================

Configuration Management Tool for Eucalyptus Deployment

Configuration Manager intended to provide a client library/API to allow basic
python representations of textual configuration(files) used to deploy and
manage Eucalyptus clouds. This is intended to be used with the existing
Eucalyptus QA deployment mechanisms/libs; 'Resource Manager',
'Deployer/MotherBrain', 'PXE manager/Cobbler', 'Chef', and an orchestrator which
is currently Jenkins.
This configuration is primarily described using JSON.

Goals
------

This library hopes to provide utilities which:
* read from an existing configuration, validate and objectify in python
* write/print/save a json representation of the current object tree to local path
* map json to pthon attributes
* sharing/repeat deployments. Allow a subset of configuration used elsewhere to
  define the base config for new deployements
* compare config. Provide diff like utilities to compare different configuration,
  and/or the current configuration in memory vs the saved configuraiton on disk.
* validate python attributes to and from a configuration. This can be used to
  help catch and avoid mis-configurations.
* allow users to avoid manually creating large and complex json configurations
* allow other tools/interfaces (GUIs, CLIs, CI, etc) to have a single
  set of libs they can use to deploy and manage a Eucalyptus cloud.

The library is intended to help QA identify areas of Eucalyptus deployment
which can be improved. This library should only provide 'workarounds' as a
temporary measure. Please open tickets against Eucalyptus and/or any related
software if improvements have a better fit elsewhere.

Installation
------
python setup.py install

Basic Usage:
------
(Coming soon)


Examples:
------
(Coming soon)





