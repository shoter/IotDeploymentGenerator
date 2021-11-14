from __future__ import annotations
from typing import Dict
from IDG.jsonObject import JsonObject

class RouteSettings:
    def __init__(self, other : RouteSettings = None):
        self._routes = {}
        self.timeToLiveSecs = 7200

        if other != None:
            self.timeToLiveSecs = other.timeToLiveSecs
            self._merge(other)


    def addRoute(self, name, route):
        self._routes[name] = route

    def removeRoute(self, name):
        if name in self._routes.keys : self._routes.remove(name)

    def _merge(self, other : RouteSettings) -> None:
        for name, route in other._routes.items():
            if name not in self._routes.keys():
                self.addRoute(name, route)

    def _asJson(self):
        json = JsonObject()

        propertiesDesired = JsonObject()
        setattr(json, "properties.desired", propertiesDesired )

        propertiesDesired.schemaVersion = "1.0"
        propertiesDesired.routes = self._routes

        storeConf = JsonObject()
        propertiesDesired.storeAndForwardConfiguration = storeConf
        storeConf.timeToLiveSecs = self.timeToLiveSecs

        return json








