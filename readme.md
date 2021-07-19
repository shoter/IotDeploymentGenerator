# IDG - IoT Deployment Generator

- [IDG - IoT Deployment Generator](#idg---iot-deployment-generator)
  * [Module](#module)
    + [Creating module](#creating-module)
    + [Setting HostConfig for module](#setting-hostconfig-for-module)
    + [Adding environment variable to module](#adding-environment-variable-to-module)
    + [Removing environment variable to module](#removing-environment-variable-to-module)
    + [Cloning module](#cloning-module)
    + [Adding module to deployment](#adding-module-to-deployment)
  * [Deployment](#deployment)
    + [Creating deployment](#creating-deployment)
    + [Removing module from deployment](#removing-module-from-deployment)
    + [Adding registry credential to deployment](#adding-registry-credential-to-deployment)
    + [Adding route to deployment](#adding-route-to-deployment)
    + [Merging deployment](#merging-deployment)
    + [Converting deployment into string](#converting-deployment-into-string)
    + [Saving deployment to deployment template file](#saving-deployment-to-deployment-template-file)

<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>






## Module

### Creating module

In order to create module you need to specify its name, version and image.

```
module = Module("module_name", "1.0.0", "image_str")
```

- image_str represents image which is used inside deployment template.
    - As it is template you can refer to modules inside solution to load them. exxample: `${MODULEDIR<../some_module>}`

### Setting HostConfig for module

```
module.desiredProperties["HostConfig"] = {
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

### Adding module to deployment

```
deployment.addModule(module)
```

## Deployment

### Creating deployment

Contains default deployment settings with edgeAgent and edgeHub initial settings.

```
deployment = Deployment()
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