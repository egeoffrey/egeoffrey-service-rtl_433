# egeoffrey-service-rtl_433

This is an eGeoffrey service package.

## Description

Interact with an attached RTL-SDR device.

## Install

To install this package, run the following command from within your eGeoffrey installation directory:
```
egeoffrey-cli install egeoffrey-service-rtl_433
```
After the installation, remember to run also `egeoffrey-cli start` to ensure the Docker image of the package is effectively downloaded and started.
To validate the installation, go and visit the *'eGeoffrey Admin'* / *'Packages'* page of your eGeoffrey instance. All the modules, default configuration files and out-of-the-box contents if any will be automatically deployed and made available.
## Content

The following modules are included in this package.

For each module, if requiring a configuration file to start, its settings will be listed under *'Module configuration'*. Additionally, if the module is a service, the configuration expected to be provided by each registered sensor associated to the service is listed under *'Service configuration'*.

To configure each module included in this package, once started, click on the *'Edit Configuration'* button on the *'eGeoffrey Admin'* / *'Modules'* page of your eGeoffrey instance.
- **service/rtl_433**: interact with an attached RTL-SDR device
  - Module configuration:
    - *command**: the command for running rtl_433 executable (e.g. /usr/local/bin/rtl_433)
    - *arguments**: the arguments for running the rtl_433 command (e.g. -F json -U)
  - Service configuration:
    - Mode 'push':
      - *filter*: filter in provided data in a key1=value1&key2=value2 format (e.g. model=Generic Sensor&id=3d c1 5c)
      - *measure*: the key whose value has to be retrieved

## Contribute

If you are the author of this package, simply clone the repository, apply any change you would need and run the following command from within this package's directory to commit your changes and automatically push them to Github:
```
egeoffrey-cli commit "<comment>"
```
After taking this action, remember you still need to build (see below) the package (e.g. the Docker image) to make it available for installation.

If you are a user willing to contribute to somebody's else package, submit your PR (Pull Request); the author will take care of validating your contributation, merging the new content and building a new version.

## Build

Building is required only if you are the author of the package. To build a Docker image and automatically push it to [Docker Hub](https://hub.docker.com/r/egeoffrey/egeoffrey-service-rtl_433), run the following command from within this package's directory:
```
egeoffrey-cli build egeoffrey-service-rtl_433
```
To function properly, when running in a Docker container, the following additional configuration settings has to be added to e.g. your docker-compose.yml file (when installing through egeoffrey-cli, this is not needed since done automatically upon installation):
```
privileged: true
```

## Uninstall

To uninstall this package, run the following command from within your eGeoffrey installation directory:
```
egeoffrey-cli uninstall egeoffrey-service-rtl_433
```
Remember to run also `egeoffrey-cli start` to ensure the changes are correctly applied.
## Tags

The following tags are associated to this package:
```
service rtl_433 rtl_sdr
```

## Version

The version of this egeoffrey-service-rtl_433 is 1.0-16 on the master branch.
