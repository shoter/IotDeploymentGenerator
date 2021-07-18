from __future__ import annotations
from jsonObject import JsonObject

import copy
class Module:

    restartPolicy = "always"
    createOptions = {}
    desiredProperties = {}
    __env = {}

    def __init__(self, name, version, image):
        self.name = name
        self.version = version
        self.image = image
        self.type = "docker"
        self.status = "running"
        self.restartPolicy = "always"

    def addEnvVariable(self, key, value):
        self.__env[key] = value

    def removeEnvVariable(self, key):
        if key in self.__env.keys : del self.__env[key]

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

        


        



