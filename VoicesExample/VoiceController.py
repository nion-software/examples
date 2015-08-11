# standard libraries
import gettext

# third party libraries
# None

class VoiceController(object):

    def __init__(self, voices_model):
        self.__voices_model = voices_model
        self.__voice = None
        self.on_voice_list_changed = None
        self.on_voice_changed = None
        self.on_messsages_changed = None

    def initialize_state(self):
        voices = self.__voices_model.voices
        self.__voice = voices[0]

        self.on_voice_list_changed(voices)
        self.on_voice_changed(self.__voice)
        self.on_messages_changed(self.__voices_model.messages)

        self.__voices_model.listeners.append(self)

    def message_changed(self, voice, message):
        self.on_messages_changed(self.__voices_model.messages)

    def handle_voice_changed(self, voice):
        assert voice in self.__voices_model.voices
        self.__voice = voice
        self.on_voice_changed(self.__voice)

    def handle_send_message(self, message):
        self.__voices_model.send_message(self.__voice, message)
