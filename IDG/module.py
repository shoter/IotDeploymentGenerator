from __future__ import annotations
from IDG.jsonObject import JsonObject
from IDG.exceptions import DotInNameException

import copy
class Module:

    def __init__(self, name, version, image):
        self.name = name
        self.version = version
        self.image = image
        self.type = "docker"
        self.status = "running"
        self.restartPolicy = "always"
        self.desiredProperties = {}
        self.createOptions = {}
        self.__env = {}
        _checkModule(self)

    def addEnvVariable(self, key, value):
        self.__env[key] = value

    def removeEnvVariable(self, key):
        self.__env.pop(key)

    @property
    def HostConfig(self):
        if "HostConfig" not in self.createOptions:
            self.createOptions["HostConfig"] = {}
        return self.createOptions["HostConfig"]

    @HostConfig.setter
    def HostConfig(self, value):
        if "HostConfig" not in self.createOptions:
            self.createOptions["HostConfig"] = {}
        self.createOptions["HostConfig"] = value

    @property
    def NetworkingConfig(self):
        if "NetworkingConfig" not in self.createOptions:
            self.createOptions["NetworkingConfig"] = {}
        return self.createOptions["NetworkingConfig"]

    @NetworkingConfig.setter
    def NetworkingConfig(self, value):
        if "NetworkingConfig" not in self.createOptions:
            self.createOptions["NetworkingConfig"] = {}
        self.createOptions["NetworkingConfig"] = value

    def clone(self) -> Module:
        ret = Module(self.name, self.version, self.image)
        ret.restartPolicy = f"{self.restartPolicy}"
        ret.createOptions = copy.deepcopy(self.createOptions)
        ret.desiredProperties = copy.deepcopy(self.desiredProperties)
        ret.__env = copy.deepcopy(self.__env)
        return ret


    def _asJson(self):
        json = JsonObject()

        json.version = self.version
        json.type = self.type
        json.status = self.status
        json.restartPolicy = self.restartPolicy

        envDict = {}
        for key,val in self.__env.items():
            envDict[key] = {
                "value": val
            }

        json.env = envDict



        settings = json.settings = JsonObject()
        settings.image = self.image
        settings.createOptions = self.createOptions

        return json


def _checkModule(module : Module):
    if "." in module.name:
        raise DotInNameException("Module name cannot contain dots in the name")