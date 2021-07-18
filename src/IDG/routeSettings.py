from os import add_dll_directory
from typing import Dict
from jsonObject import JsonObject
from __future__ import annotations

class RouteSettings:
    __routes: Dict[str, str] = {}
    timeToLiveSecs = 7200

    def addRoute(self, name, route):
        self.__routes[name] = route

    def removeRoute(self, name):
        if name in self.__routes.keys : self.__routes.remove(name)

    def __merge(self, other : RouteSettings) -> None:
        for name, route in other.__routes.items():
            if name not in self.__routes.keys():
                self.addRoute(name, route)

    def asJson(self):
        json = JsonObject()

        propertiesDesired = json["properties.desired"] = JsonObject()

        propertiesDesired.schemaVersion = "1.0"
        propertiesDesired.routes = self.__routes

        storeConf = JsonObject()
        propertiesDesired.storeAndForwardConfiguration = storeConf
        storeConf.timeToLiveSecs = self.timeToLiveSecs

        return json








