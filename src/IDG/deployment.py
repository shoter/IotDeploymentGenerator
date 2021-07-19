from __future__ import annotations
from typing import Dict
from IDG.jsonObject import JsonObject
from IDG.routeSettings import RouteSettings
from IDG.module import Module


class RegistryCredential:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password

    def asJson(self) -> JsonObject:
        json = JsonObject()
        json.address = self.address
        json.username = self.username
        json.password = self.password
        return json

    def clone(self) -> RegistryCredential:
        return RegistryCredential(self.address, self.username, self.password)


class Deployment:

    def __init__(self, other : Deployment = None):
        self.minDockerVersion = "v1.25"
        self.edgeAgentVersion = "1.0"
        self.edgeHubVersion = "1.0"
        self.loggingOptions = ""
        self.routeSettings : RouteSettings = RouteSettings()
        self.__registryCredentials: Dict[str, RegistryCredential] = {}
        self._modules : list[Module] = []
        if other != None:
            self.minDockerVersion = other.minDockerVersion
            self.edgeAgentVersion = other.edgeAgentVersion
            self.edgeHubVersion = other.edgeHubVersion
            self.loggingOptions = other.loggingOptions
            self.__registryCredentials = {key: value.clone() for key,value in other.__registryCredentials.items()}
            self._modules = [m.clone() for m in other._modules]
            self.routeSettings = RouteSettings(other.routeSettings)


    def addRegistryCredentials(self, name,  address, username, password) -> None:
        self.__registryCredentials[name] = RegistryCredential(address, username, password)

    def addModule(self : Deployment, module : Module) -> Deployment:
        self._modules.append(module)
        return self

    def removeModule(self: Deployment, moduleName: str) -> Deployment:
        self._modules = [m for m in self._modules if m.name == moduleName]
        return self

    def toJson(self) -> str:
        self.__asJson().toJSON()

    def saveToFile(self, path) -> None:
        file = open(path, "w")
        file.write(self.__asJson().toJSON())
        file.close()

    def merge(self : Deployment, other: Deployment ) -> Deployment:
        ret = Deployment(self)

        for m in other._modules:
            if m.name not in [x.name for x in ret._modules]:
                ret._modules.append(m)

        ret.routeSettings._merge(other.routeSettings)

        return ret


    def __asJson(self) -> JsonObject:
        json = JsonObject()

        setattr(json, "$schema-template", "2.0.0")
        json.modulesContent = {}

        regCreds = {}
        for key, value in self.__registryCredentials.items():
            regCreds[key] = value.asJson()



        moduleJsonObjs = {}
        for m in self._modules:
            moduleJsonObjs[m.name] = m._asJson()


        json.modulesContent["$edgeAgent"] = {
            "properties.desired": {
                "schemaVersion": "1.0",
                "runtime": {
                    "type": "docker",
                    "settings": {
                        "minDockerVersion": self.minDockerVersion,
                        "loggingOptions": self.loggingOptions,
                        "registryCredentials": regCreds
                    }
                },
                "systemModules": {
                    "edgeAgent": {
                        "type": "docker",
                        "settings": {
                            "image": f"mcr.microsoft.com/azureiotedge-agent:{self.edgeAgentVersion}",
                        }
                    },
                    "edgeHub": {
                        "type": "docker",
                        "status": "running",
                        "restartPolicy": "always",
                        "settings": {
                            "image": f"mcr.microsoft.com/azureiotedge-hub:{self.edgeHubVersion}",
                            "createOptions": {
                                "HostConfig": {
                                    "PortBindings": {
                                        "5671/tcp": [
                                            {
                                                "HostPort": "5671"
                                            }
                                        ],
                                        "8883/tcp": [
                                            {
                                                "HostPort": "8883"
                                            }
                                        ],
                                        "443/tcp": [
                                            {
                                                "HostPort": "443"
                                            }
                                        ]
                                    }
                                }
                            }
                        }
                    }

                },
                "modules": moduleJsonObjs
                
            }
        }


        json.modulesContent["$edgeHub"] = self.routeSettings._asJson()

        for m in self._modules:
            if m.desiredProperties:
                json.modulesContent[m.name] = {
                    "properties.desired": m.desiredProperties
                }

        return json


