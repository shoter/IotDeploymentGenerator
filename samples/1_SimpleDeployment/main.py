from IDG.deployment import Deployment
from IDG.module import Module

deployment = Deployment()

# Iot Edge Module 1
IotEdgeModule1 = Module("IotEdgeModule1", "1.0.0",
                        "${MODULEDIR<../IotEdgeModule1>}")

# Sensor
SimulatedTemperatureSensor = Module("SimulatedTemperatureSensor", "1.0",
                                    "mcr.microsoft.com/azureiotedge-simulated-temperature-sensor:1.0")
SimulatedTemperatureSensor.addEnvVariable("MessageCount", "10000")

# BloB Storage
AzureBlobStorageonIoTEdge = Module(
    "AzureBlobStorageonIoTEdge", "1.0", "mcr.microsoft.com/azure-blob-storage:latest")
AzureBlobStorageonIoTEdge.createOptions["HostConfig"] = {
    "PortBindings": {
        "11002/tcp": [{
            "HostPort": "11002"
        }]
    }
}
AzureBlobStorageonIoTEdge.desiredProperties = {
    "deviceToCloudUploadProperties": {
        "uploadOn": True,
        "uploadOrder": "OldestFirst",
        "deleteAfterUpload": True,
        "storageContainersForUpload": {
            "abc": {
                "target": "cba"
            }
        }
    }
}
AzureBlobStorageonIoTEdge.addEnvVariable("LOCAL_STORAGE_ACCOUNT_NAME", "iotblob")

# Test Web App
TestWebApp = Module("TestWebApp", "1.0.0", "${MODULEDIR<../TestWebApp>}")

# Routes
deployment.routeSettings.addRoute("moduleToWebApp", "FROM /messages/modules/IotEdgeModule1/outputs/temp INTO BrokeredEndpoint(\"/modules/TestWebApp/inputs/mytemp\")")
deployment.routeSettings.addRoute("sensorToIotEdgeModule1", "FROM /messages/modules/SimulatedTemperatureSensor/outputs/temperatureOutput INTO BrokeredEndpoint(\"/modules/TestWebApp/inputs/mytemp\")")

# Adding modules to deployment

deployment.addModule(IotEdgeModule1)
deployment.addModule(SimulatedTemperatureSensor)
deployment.addModule(AzureBlobStorageonIoTEdge)
deployment.addModule(TestWebApp)

# Saving
deployment.saveToFile("deployment.debug.template.json")
