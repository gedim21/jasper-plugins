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
            ip = '192.168.1.1'

        """
        try:
            self._bridge = Bridge(ip)
            self._lights = self._bridge.get_light_objects()
        except PhueRequestTimeout as e:
            self._bridge = None
            self._lights = None
        """

    def get_priority(self):
        return 10

    def get_phrases(self):
        return [self.gettext("LIVING ROOM"),
                self.gettext("BEDROOM"),
                self.gettext("KITCHEN"),
                self.gettext("LIGHT"),
                self.gettext("DIM")]

    def handle(self, text, mic):
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """
        if self._bridge is None:
            mic.say(self.gettext("Sorry, but your bridge is not reachable at this moment."))
            return

        if re.search(r'\bliving room\b', text, re.IGNORECASE):
            if re.search(r'\bon\b', text, re.IGNORECASE):
                mic.say("Turning on the living room lights.")
                self._bridge.set_group('Living Room', on)
            elif re.search(r'\boff\b', text, re.IGNORECASE) or re.search(r'\bof\b', text, re.IGNORECASE):
                mic.say("Turning off the living room lights.")
                self._bridge.set_group('Living Room', off)
            elif re.search(r'\bdim\b', text, re.IGNORECASE):
                mic.say("Dimming the living room lights.")
                self._bridge.set_group('Living Room', dim)
            else:
                mic.say("Sorry, I didn't understand that.")

        elif re.search(r'\bkitchen\b', text, re.IGNORECASE):
            if re.search(r'\bon\b', text, re.IGNORECASE):
                mic.say("Turning on the kitchen lights.")
                self._bridge.set_light('Kitchen', on)
            elif re.search(r'\boff\b', text, re.IGNORECASE) or re.search(r'\bof\b', text, re.IGNORECASE):
                mic.say("Turning off the kitchen lights.")
                self._bridge.set_light('Kitchen', off)
            elif re.search(r'\bdim\b', text, re.IGNORECASE):
                mic.say("Dimming the kitchen lights.")
                self._bridge.set_light('Kitchen', dim)
            else:
                mic.say("Sorry, I didn't understand that.")

        elif re.search(r'\bbedroom\b', text, re.IGNORECASE):
            if re.search(r'\bon\b', text, re.IGNORECASE):
                mic.say("Turning on the bedroom lights.")
                self._bridge.set_light('Bedroom', on)
            elif re.search(r'\boff\b', text, re.IGNORECASE) or re.search(r'\bof\b', text, re.IGNORECASE):
                mic.say("Turning off the bedroom lights.")
                self._bridge.set_light('Bedroom', off)
            elif re.search(r'\bdim\b', text, re.IGNORECASE):
                mic.say("Dimming the bedroom lights.")
                self._bridge.set_light('Bedroom', dim)
            else:
                mic.say("Sorry, I didn't understand that.")
        else:
            mic.say("Sorry, I didn't understand that.")

    def is_valid(self, text):
        """
        Returns True if the input is related to hue control

        Arguments:
        text -- user-input, typically transcribed speech
        """
        textContainsAnyRoom = re.search(r'\bliving room|kitchen|bedroom\b', text, re.IGNORECASE)
        textContainsLightWord = re.search(r'\blights|light\b', text, re.IGNORECASE)
        isValid = textContainsLightWord and textContainsAnyRoom
        return isValid
