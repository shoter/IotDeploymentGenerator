from unittest import TestCase
from IDG.jsonObject import JsonObject
from IDG.module import Module
from nose.tools import raises
from IDG.exceptions import DotInNameException
from typing import Dict

# https://python-packaging.readthedocs.io/en/latest/testing.html

class ModuleShould(TestCase):
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

    @raises(DotInNameException)
    def test_notAllowDotsInName(self):
        module = Module("name.name", "1.0", "image")
