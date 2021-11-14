from unittest import TestCase
from IDG.jsonObject import JsonObject
from typing import Dict

from IDG.module import Module

# https://python-packaging.readthedocs.io/en/latest/testing.html

class ModuleShould(TestCase):
    def test_is_true(self):
        self.assertTrue(True)

    def test_properlyEmbedBasicPropsInJson(self):
        module = Module("name", "version", "image")
        json = module._asJson()
        self.assertEqual("version", json.version)
        self.assertEqual("image", json.settings.image)

    def test_properlyEmbedEnvironmentVariable(self):
        module = Module("name", "version", "image")
        module.addEnvVariable("key", "someVal")

        json : JsonObject = module._asJson()
        self.assertTrue("key" in json.env)
        env = json.env["key"]
        self.assertEqual(env["value"], "someVal")

    def test_removeEnvironmentVariable(self):
        module = Module("name", "version", "image")
        module.addEnvVariable("key", "someVal")
        module.removeEnvVariable("key")

        json = module._asJson()

        self.assertFalse(hasattr(json.env, "key"))