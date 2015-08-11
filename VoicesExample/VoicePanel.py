# standard libraries
import gettext

# third party libraries
# None

# local libraries
from . import VoiceController
from . import VoiceModel

_ = gettext.gettext


class VoicesPanelDelegate(object):

    def __init__(self, panel_id, name):
        self.panel_id = panel_id
        self.panel_name = name
        self.panel_positions = ["left", "right"]
        self.panel_position = "right"

    def create_panel_widget(self, ui, document_controller):

        def combo_box_changed(text):
            controller.handle_voice_changed(text)

        combo_box = ui.create_combo_box_widget()
        combo_box.on_current_text_changed = combo_box_changed

        message_line_edit = ui.create_line_edit_widget()

        def send_message():
            controller.handle_send_message(message_line_edit.text)
            message_line_edit.text = str()

        send_button = ui.create_push_button_widget(_("Send"))
        send_button.on_clicked = send_message

        messages_label = ui.create_label_widget()

        column = ui.create_column_widget()

        voice_row = ui.create_row_widget()
        voice_row.add(combo_box)
        voice_row.add_stretch()

        send_message_row = ui.create_row_widget()
        send_message_row.add(message_line_edit)
        send_message_row.add_spacing(8)
        send_message_row.add(send_button)
        send_message_row.add_stretch()

        messages_row = ui.create_row_widget()
        messages_row.add(messages_label)

        column.add_spacing(8)
        column.add(voice_row)
        column.add(send_message_row)
        column.add(messages_row)
        column.add_spacing(8)
        column.add_stretch()

        def voice_changed(voice):
            combo_box.item = voice

        def messages_changed(messages):
            parts = list()
            for voice, message in messages.items():
                parts.append(voice[0] + ": " + message)  # "A: Hello"
            messages_label.text = "\n".join(parts)

        def voice_list_changed(voice_list):
            combo_box.items = voice_list

        controller = VoiceController.VoiceController(VoiceModel.voices)
        controller.on_voice_changed = voice_changed
        controller.on_messages_changed = messages_changed
        controller.on_voice_list_changed = voice_list_changed
        controller.initialize_state()

        return column

class VoicesPanel1Extension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.panel_voices1"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__panel_ref = api.create_panel(VoicesPanelDelegate("voices1-panel", _("Voices 1")))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__panel_ref.close()
        self.__panel_ref = None


class VoicesPanel2Extension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.panel_voices2"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__panel_ref = api.create_panel(VoicesPanelDelegate("voices2-panel", _("Voices 2")))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__panel_ref.close()
        self.__panel_ref = None
