from routeSettings import RouteSettings
from jsonObject import JsonObject
from module import Module
from deployment import Deployment

a = Deployment()

a.edgeAgentVersion = "2.0"
moduleA = Module("test", "1.0", "someImage")
moduleA.addEnvVariable("superVar", "ASDSAD")
moduleA.desiredProperties["test"] = "123"
moduleA.createOptions["HostConfig"] = {
    "Binds": [
        "a:x",
        "b:c"
    ]
}

a.modules.append(moduleA)

b = Deployment()
b.edgeHubVersion = "3.0"
moduleB = Module("moduleB", "3.0", "adsadsa")

b.modules.append(moduleB)

final = a.merge(b)
final.saveToFile("deployment.debug.template.json")
