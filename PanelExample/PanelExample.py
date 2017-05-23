# standard libraries
import gettext
import logging

# third party libraries
# None

# local libraries
# None

_ = gettext.gettext


class PanelExampleDelegate(object):

    def __init__(self):
        self.panel_id = "example-panel"
        self.panel_name = _("Example")
        self.panel_positions = ["left", "right"]
        self.panel_position = "right"

    def create_panel_widget(self, ui, document_controller):
        column = ui.create_column_widget()

        edit_row = ui.create_row_widget()
        edit_row.add(ui.create_label_widget(_("Edit Field")))
        edit_row.add_spacing(12)
        edit_line_edit = ui.create_line_edit_widget()
        def editing_finished(text):
            logging.debug(text)
            edit_line_edit.request_refocus()
        edit_line_edit.on_editing_finished = editing_finished
        edit_row.add(edit_line_edit)
        edit_row.add_stretch()

        button_row = ui.create_row_widget()
        button_widget = ui.create_push_button_widget(_("Push Me"))
        def button_clicked():
            edit_line_edit.text = str()
        button_widget.on_clicked = button_clicked
        button_row.add(button_widget)
        button_row.add_stretch()

        column.add_spacing(8)
        column.add(edit_row)
        column.add(button_row)
        column.add_spacing(8)
        column.add_stretch()

        return column


class PanelExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.panel_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__panel_ref = api.create_panel(PanelExampleDelegate())

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__panel_ref.close()
        self.__panel_ref = None
