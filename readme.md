# IDG - IoT Deployment Generator

[![PyPI version](https://badge.fury.io/py/IoT-Deployment-Generator.svg)](https://badge.fury.io/py/IoT-Deployment-Generator)


Library used to create [Azure IoT Edge deployment templates](https://docs.microsoft.com/en-us/azure/iot-edge/module-composition?view=iotedge-2020-11) with python code. 

## Table of contents

- [IDG - IoT Deployment Generator](#idg---iot-deployment-generator)
  * [Table of contents](#table-of-contents)
  * [Library dependencies](#library-dependencies)
  * [Installation](#installation)
  * [Required imports](#required-imports)
  * [Module documentation](#module-documentation)
    + [Creating module](#creating-module)
    + [Changing miscellaneous settings of module](#changing-miscellaneous-settings-of-module)
    + [Setting HostConfig for module](#setting-hostconfig-for-module)
    + [Setting desired properties for module](#setting-desired-properties-for-module)
    + [Adding environment variable to module](#adding-environment-variable-to-module)
    + [Removing environment variable to module](#removing-environment-variable-to-module)
    + [Cloning module](#cloning-module)
  * [Deployment documentation](#deployment-documentation)
    + [Creating deployment](#creating-deployment)
    + [Changing miscellaneous settings of deployment](#changing-miscellaneous-settings-of-deployment)
    + [Adding module to deployment](#adding-module-to-deployment)
    + [Removing module from deployment](#removing-module-from-deployment)
    + [Adding registry credential to deployment](#adding-registry-credential-to-deployment)
    + [Adding route to deployment](#adding-route-to-deployment)
    + [Changing storeAndForwardConfiguration inside edgeHub configuration](#changing-storeandforwardconfiguration-inside-edgehub-configuration)
    + [Merging deployment](#merging-deployment)
    + [Converting deployment into string](#converting-deployment-into-string)
    + [Saving deployment to deployment template file](#saving-deployment-to-deployment-template-file)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>





## Library dependencies

None

## Installation

In order to install the library you need to execute following command:

```
pip install IoT-Deployment-Generator
```

## Required imports

It is the best to use following imports when working with IDG:

```
from IDG.deployment import Deployment
from IDG.module import Module
```

## Module documentation

### Creating module

In order to create module you need to specify its name, version and image.

```
module = Module("module_name", "1.0.0", "image_str")
```

- image_str represents image which is used inside deployment template.
    - As it is template you can refer to modules inside solution to load them. exxample: `${MODULEDIR<../some_module>}`

### Changing miscellaneous settings of module

Below you will find all settings you can change inside module:

```
module.type = "docker"
module.status = "running"
module.restartPolicy = "always"
```

### Setting HostConfig for module

```
module.createOptions["HostConfig"] = {
            "Binds": [
            "volumeA:/somewhere"
        ],
        "PortBindings": {
            "8080/tcp": [{
                "HostPort": "9080"
            }]
        }
}
```

another syntax:

```
module.HostConfig = {
            "Binds": [
            "volumeA:/somewhere"
        ],
        "PortBindings": {
            "8080/tcp": [{
                "HostPort": "9080"
            }]
        }
}
```


### Setting desired properties for module

```
module.desiredProperties = {
    "propertyA" : 123,
    "propertyB" : "IamB"
}
```

### Adding environment variable to module

```
module.addEnvVariable("env_name", "env_value")
```


### Removing environment variable to module

```
module.removeEnvVariable("env_name")
```

### Cloning module

```
clonedModule = module.clone()
```

Cloned module is going to be a deep copy of initial module.


## Deployment documentation

### Creating deployment

Contains default deployment settings with edgeAgent and edgeHub initial settings.

```
deployment = Deployment()
```


### Changing miscellaneous settings of deployment

Below you will find all settings you can change inside deployment:

```
deployment.minDockerVersion = "v1.25"
deployment.edgeAgentVersion = "1.0"
deployment.edgeHubVersion = "1.0"
deployment.loggingOptions = ""
```

### Adding module to deployment

```
deployment.addModule(module)
```

### Removing module from deployment

```
deployment.removeModule("module_name")
```

it is going to remove module which has `module_name` inside `module.name`

### Adding registry credential to deployment

```
deployment.addRegistryCredentials("credential_name", "repo_address", "repo_username", "repo_pass")
```

### Adding route to deployment

```
deployment.routeSettings.addRoute("routeName", "ROM /messages/modules/someModule/outputs/* into $upstream")
```

### Changing storeAndForwardConfiguration inside edgeHub configuration

```
deployment.routeSettings.timeToLiveSecs = 7200
```

### Merging deployment

If you have 2 separate deployments you can merge them.

```

deploymentA = Deployment()
deploymentB = Deployment()

merged = deploymentA.merge(deploymentB)

```

In this case following things are going to happen:
- `merged` is going to have all modules from `deploymentA` and every module from `deploymentB` which name does not exist in `deploymentA`
- `merged` is going to have all routes from `deploymentA` and every route from `deploymentB` which name does not exist in `deploymentA`
- `merged` is going to have all registry credentials from `deploymentA` and every credential from `deploymentB` which name does not exist in `deploymentA`
- Other value settings are going to be taken solely from `deploymentA`.
- `deploymentA` and `deploymentB` are unaffected by this operation.

### Converting deployment into string

```
stringifiedJson = deployment.toJson()
```

### Saving deployment to deployment template file
```
deployment.saveToFile("deployment.debug.template.json")
```
