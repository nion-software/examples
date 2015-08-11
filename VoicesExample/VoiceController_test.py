# run from folder containing VoicesExample
# python -m unittest VoicesExample.VoiceController_test

import unittest

from . import VoiceController
from . import VoiceModel

class TestVoiceControllerClass(unittest.TestCase):

    def test_initial_messages_appear(self):

        voice_ref = [None]
        messages_ref = [None]
        voice_list_ref = [None]

        def voice_changed(voice):
            voice_ref[0] = voice

        def messages_changed(messages):
            messages_ref[0] = messages

        def voice_list_changed(voice_list):
            voice_list_ref[0] = voice_list

        vc = VoiceController.VoiceController(VoiceModel.voices)
        vc.on_voice_changed = voice_changed
        vc.on_messages_changed = messages_changed
        vc.on_voice_list_changed = voice_list_changed
        vc.initialize_state()

        self.assertEqual(voice_ref[0], "Alice")
        self.assertEqual(messages_ref[0], dict())
        self.assertEqual(len(voice_list_ref[0]), 3)

        vc.handle_voice_changed("Carol")
        vc.handle_send_message("This is Carol.")

        self.assertEqual(voice_ref[0], "Carol")
        self.assertEqual(len(messages_ref[0]), 1)
