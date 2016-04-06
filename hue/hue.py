# -*- coding: utf-8 -*-
from jasper import plugin
from phue import Bridge, PhueRequestTimeout
import re

on = {'transitiontime': 10, 'on': True, 'bri': 250}
off = {'transitiontime': 10, 'on': False}
dim = {'transitiontime': 75, 'bri': 75}


class HuePlugin(plugin.SpeechHandlerPlugin):
    def __init__(self, *args, **kwargs):
        super(HuePlugin, self).__init__(*args, **kwargs)

        try:
            ip = self.profile['hue']['ip']
        except KeyError:
            ip = '192.168.2.101'

        try:
            self._bridge = Bridge(ip)
            self._lights = self._bridge.get_light_objects()
            self._groups = self._bridge.groups
            self._light_names = []
            self._group_names = []
            for light in self._lights:
                self._light_names.append(light.name)

            for group in self._groups:
                self._group_names.append(group.name)
        except PhueRequestTimeout:
            self._bridge = None
            self._lights = None
            self._light_names = []
            self._group_names = []

    def get_priority(self):
        return 10

    def get_phrases(self):
        return self._light_names + self._group_names + ['ON', 'OFF', 'DIM']

    def handle(self, text, mic):
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        :param text: -- user-input, typically transcribed speech
        :param mic: -- used to interact with the user (for both input and output)
        """
        if self._bridge is None:
            mic.say(self.gettext("Sorry, but your bridge is not reachable at this moment."))
            return

        if re.search(r'\bliving room\b', text, re.IGNORECASE):
            if re.search(r'\bon\b', text, re.IGNORECASE):
                self.turn_on_group('Living Room', mic)
            elif re.search(r'\boff\b', text, re.IGNORECASE) or re.search(r'\bof\b', text, re.IGNORECASE):
                self.turn_off_group('Living Room', mic)
            elif re.search(r'\bdim\b', text, re.IGNORECASE):
                self.dim_group('Living Room', mic)
            else:
                mic.say("Sorry, I didn't understand that.")

        elif re.search(r'\bkitchen\b', text, re.IGNORECASE):
            if re.search(r'\bon\b', text, re.IGNORECASE):
                self.turn_on_light('Kitchen light', mic)
            elif re.search(r'\boff\b', text, re.IGNORECASE) or re.search(r'\bof\b', text, re.IGNORECASE):
                self.turn_off_light('Kitchen light', mic)
            elif re.search(r'\bdim\b', text, re.IGNORECASE):
                self.dim_light('Kitchen light', mic)
            else:
                mic.say("Sorry, I didn't understand that.")

        elif re.search(r'\bbedroom\b', text, re.IGNORECASE):
            if re.search(r'\bon\b', text, re.IGNORECASE):
                self.turn_on_light('Bedroom light', mic)
            elif re.search(r'\boff\b', text, re.IGNORECASE) or re.search(r'\bof\b', text, re.IGNORECASE):
                self.turn_off_light('Bedroom light', mic)
            elif re.search(r'\bdim\b', text, re.IGNORECASE):
                self.dim_light('Bedroom light', mic)
            else:
                mic.say("Sorry, I didn't understand that.")
        else:
            mic.say("Sorry, I didn't understand that.")

    def is_valid(self, text):
        """
        Returns True if the input is related to hue control

        Arguments:
        :param text: user-input, typically transcribed speech
        """
        text_matches_a_light = False
        for light_name in self._light_names:
            if re.search(light_name, text, re.IGNORECASE):
                text_matches_a_light = True
                break

        text_matches_a_group = False
        for group_name in self._group_names:
            if re.search(group_name, text, re.IGNORECASE):
                text_matches_a_group = True
                break

        is_valid = text_matches_a_light or text_matches_a_group
        return is_valid

    def turn_on_light(self, light_name, mic):
        mic.say("Turning on " + light_name)
        self._bridge.set_light(light_name, on)

    def turn_off_light(self, light_name, mic):
        mic.say("Turning off " + light_name)
        self._bridge.set_light(light_name, off)

    def dim_light(self, light_name, mic):
        mic.say("Dimming " + light_name)
        self._bridge.set_light(light_name, dim)

    def turn_on_group(self, group_name, mic):
        mic.say("Turning on group " + group_name)
        self._bridge.set_light(group_name, on)

    def turn_off_group(self, group_name, mic):
        mic.say("Turning off group " + group_name)
        self._bridge.set_light(group_name, off)

    def dim_group(self, group_name, mic):
        mic.say("Dimming group " + group_name)
        self._bridge.set_light(group_name, dim)
