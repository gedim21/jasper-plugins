# -*- coding: utf-8 -*-
from jasper import plugin
import requests
import re


class HomeAssistantPlugin(plugin.SpeechHandlerPlugin):
    def __init__(self, *args, **kwargs):
        super(HomeAssistantPlugin, self).__init__(*args, **kwargs)

        try:
            self._ha_url = self.profile['home-assistant']['url']
        except:
            self._ha_url = 'http://localhost:8123'

    def get_priority(self):
        return 5

    def get_phrases(self):
        return [self.gettext("LIVING ROOM"),
                self.gettext("BEDROOM"),
                self.gettext("TEMPERATURE"),
                self.gettext("HUMIDITY")]

    def handle(self, text, mic):
        """
        Responds to user-input, typically speech text, by telling a joke.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        """

    def is_valid(self, text):
        """
        Returns True if the input is related to hue control

        Arguments:
        text -- user-input, typically transcribed speech
        """
        return any(p.lower() in text.lower() for p in self.get_phrases())
