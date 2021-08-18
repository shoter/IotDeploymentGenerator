from unittest import TestCase

from IDG.module import Module

# https://python-packaging.readthedocs.io/en/latest/testing.html

class ModuleShould(TestCase):
    def properlyEmbedBasicPropsInJson(self):
        module = Module("name", "version", "image")
        json = module._asJson()
        self.assertEqual("version", json.version)
        self.assertEqual("image", json.settings.image)

    def properlyEmbedEnvironmentVariable(self):
        module = Module("name", "version", "image")
        module.addEnvVariable("key", "someVal")

        json = module._asJson()
        self.assertTrue(hasattr(json.env, "key"))
        env = json.env.key
        self.assertEqual(env.value, "someVal")

    def removeEnvironmentVariable(self):
        module = Module("name", "version", "image")
        module.addEnvVariable("key", "someVal")
        module.removeEnvVariable("key")

        json = module._asJson()

        self.assertFalse(hasattr(json.env, "key"))