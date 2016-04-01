# -*- coding: utf-8 -*-
import unittest
from jasper import testutils
import hue


class TestHuePlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = testutils.get_plugin_instance(hue.HuePlugin)

    def test_is_valid_method(self):
        self.assertTrue(self.plugin.is_valid("Turn on the living room lights"))
        self.assertTrue(self.plugin.is_valid("Living room lights on"))
        self.assertTrue(self.plugin.is_valid("Turn off the living room lights"))
        self.assertTrue(self.plugin.is_valid("Dim the living room lights"))
        self.assertTrue(self.plugin.is_valid("Dim living room lights"))
        self.assertTrue(self.plugin.is_valid("Turn on the bedroom lights"))
        self.assertTrue(self.plugin.is_valid("Turn off the bedroom lights"))
        self.assertTrue(self.plugin.is_valid("Dim the bedroom lights"))
        self.assertFalse(self.plugin.is_valid("Turn on the lights"))

    def test_handle_method(self):
        mic = testutils.TestMic(inputs=["Turn on the kitchen lights"])
        self.plugin.handle("Turn on the kitchen lights", mic)
        self.assertEqual(len(mic.outputs), 1)
        self.assertEqual("Turning on the kitchen lights.", mic.outputs[0])