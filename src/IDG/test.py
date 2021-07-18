from routeSettings import RouteSettings
from jsonObject import JsonObject
from module import Module

netdev = Module("netdev", "1.0", "someImage")

netdev.createOptions["HostConfig"] = {
    "Binds": [
        "operator-api:/persistent-data"
    ],
    "ExtraHosts": [
        "operator.priva.local:123",
        "iam.priva.local:213"
    ],
    "PortBindings": {
        "9000/tcp": [
            {
            "HostPort": "9000"
            }
        ]
    }
}

netdev.addEnvVariable("test", "asd")

print(netdev.__asJson().toJSON())