# -*- coding: utf-8 -*-
import unittest
from jasper import testutils
import homeassistant


class TestHomeAssistantPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = testutils.get_plugin_instance(homeassistant.HomeAssistantPlugin)

    def test_is_valid_method(self):
        self.assertTrue(self.plugin.is_valid("What is the temperature in the living room?"))
        self.assertTrue(self.plugin.is_valid("What is the living room temperature?"))
        self.assertTrue(self.plugin.is_valid("What is the humidity in the living room?"))
        self.assertTrue(self.plugin.is_valid("What is the temperature in the bedroom?"))
        self.assertTrue(self.plugin.is_valid("What is the humidity in the bedroom?"))

        self.assertFalse(self.plugin.is_valid("Turn on the living room lights"))
        self.assertFalse(self.plugin.is_valid("Turn off the living room lights"))
        self.assertFalse(self.plugin.is_valid("Turn on the bedroom light"))
        self.assertFalse(self.plugin.is_valid("Turn off the bedroom light"))

    def test_handle_method(self):
        mic = testutils.TestMic(inputs=["Turn on the kitchen lights"])
        self.plugin.handle("Turn on the kitchen lights", mic)
        self.assertEqual(len(mic.outputs), 1)
        self.assertEqual("Turning on the kitchen lights.", mic.outputs[0])
