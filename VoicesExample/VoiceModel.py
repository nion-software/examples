class VoiceModel(object):

    def __init__(self):
        self.voices = ["Alice", "Bob", "Carol"]
        self.messages = dict()
        self.listeners = list()

    def send_message(self, voice, message):
        assert voice in self.voices, "Something went wrong"
        self.messages[voice] = str(message)
        for listener in self.listeners:
            listener.message_changed(message, voice)

voices = VoiceModel()
