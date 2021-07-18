from __future__ import annotations
from typing import Dict
from jsonObject import JsonObject

class RouteSettings:
    __routes: Dict[str, str] = {}
    timeToLiveSecs = 7200

    def __init__(self, other : RouteSettings = None):
        if other != None:
            self.timeToLiveSecs = other.timeToLiveSecs
            self._merge(other)

    def addRoute(self, name, route):
        self.__routes[name] = route

    def removeRoute(self, name):
        if name in self.__routes.keys : self.__routes.remove(name)

    def _merge(self, other : RouteSettings) -> None:
        for name, route in other.__routes.items():
            if name not in self.__routes.keys():
                self.addRoute(name, route)

    def _asJson(self):
        json = JsonObject()

        propertiesDesired = JsonObject()
        setattr(json, "properties.desired", propertiesDesired )

        propertiesDesired.schemaVersion = "1.0"
        propertiesDesired.routes = self.__routes

        storeConf = JsonObject()
        propertiesDesired.storeAndForwardConfiguration = storeConf
        storeConf.timeToLiveSecs = self.timeToLiveSecs

        return json








