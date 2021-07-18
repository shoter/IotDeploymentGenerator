from jsonObject import JsonObject
from __future__ import annotations
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

    def clone(self, other : Module) -> Module:
        ret = Module()
        ret.restartPolicy = f"{other.restartPolicy}"
        ret.createOptions = copy.deepcopy(other.createOptions)
        ret.desiredProperties = copy.deepcopy(other.desiredProperties)
        ret.__env = copy.deepcopy(other.__env)
        return ret


    def __asJson(self):
        json = JsonObject()
        moduleContent = JsonObject()
        setattr(json, self.name, moduleContent)

        moduleContent.version = self.version
        moduleContent.type = self.type
        moduleContent.status = self.status
        moduleContent.restartPolicy = self.restartPolicy

        envDict = {}
        for key,val in self.__env.items():
            envDict[key] = {
                "value": val
            }

        moduleContent.env = envDict



        settings = moduleContent.settings = JsonObject()
        settings.image = self.image
        settings.createOptions = self.createOptions

        return json

        


        



