from typing import Dict
from IDG import jsonObject
from IDG.jsonObject import JsonObject
from routeSettings import RouteSettings
from module import Module
from __future__ import annotations

class RegistryCredential:
    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password

    def asJson(self):
        json = JsonObject()
        json.address = self.address
        json.username = self.username
        json.password = self.password

    def clone(self) -> RegistryCredential:
        return RegistryCredential(self.address, self.username, self.password)


class Deployment:

    minDockerVersion : str = "v1.25"
    edgeAgentVersion: str =  "1.0"
    edgeHubVersion: str = "1.0"
    loggingOptions: str = ""
    routeSettings = RouteSettings()

    __registryCredentials: Dict[str, RegistryCredential] = {}
    modules : list[Module] = []


    def __init__(self, other : Deployment = None()):
        if other != None():
            self.minDockerVersion = f"{other.minDockerVersion}"
            self.edgeAgentVersion = f"{other.edgeAgentVersion}"
            self.edgeHubVersion = f"{other.edgeHubVersion}"
            self.loggingOptions = f"{other.loggingOptions}"
            self.__registryCredentials = {key: value.clone() for key,value in other.__registryCredentials.items()}
            self.modules = [m.clone() for m in other.modules]
            return self


    def addRegistryCredentials(self, name,  address, username, password) -> None:
        self.__registryCredentials[name] = RegistryCredential(address, username, password)

    def toJson(self) -> str:
        self.__asJson().toJSON()

    def saveToFile(self, path) -> None:
        file = open(path, "w")
        file.write(self.toJson())
        file.close()

    def merge(self : Deployment, other: Deployment ) -> Deployment:
        ret = Deployment(self)

        for m in other.modules:
            if m.name not in [x.name for x in ret.modules]:
                ret.modules.append(m)

        ret.routeSettings.__merge(other.routeSettings)

        return ret


    def __asJson(self) -> JsonObject:
        json = JsonObject()

        json["$schema-template"] = "2.0.0",
        json.modulesContent = {}

        regCreds = {}
        for key, value in self.__registryCredentials.items():
            regCreds[key] = value.asJson()

        moduleJsonObjs = []
        for m in self.modules:
            moduleJsonObjs.append(m.__asJson())


        json.moduleContent["$edgeAgent"] = {
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

        json["$edgeHub"] = self.routeSettings.asJson().toJSON()

        for m in self.modules:
            if m.desiredProperties:
                json[m.name] = m.desiredProperties

        return json


