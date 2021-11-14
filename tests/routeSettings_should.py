from unittest import TestCase
from IDG import RouteSettings, JsonObject
from nose.tools import raises
from IDG.exceptions import DotInNameException
from typing import Dict

# https://python-packaging.readthedocs.io/en/latest/testing.html

class RouteSettingsShould(TestCase):
    @raises(DotInNameException)
    def test_throwException_whenDotInRoute(self):
        rt = RouteSettings()
        rt.addRoute("assssasa", "ala.ma.kota")

    
