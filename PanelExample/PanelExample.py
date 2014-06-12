# standard libraries
import gettext
import logging

# third party libraries
# None

# local libraries
from nion.swift import Panel
from nion.swift import Workspace
from nion.swift.model import DataItem
from nion.ui import Binding

_ = gettext.gettext


class PanelExample(Panel.Panel):

    def __init__(self, document_controller, panel_id, properties):
        super(PanelExample, self).__init__(document_controller, panel_id, "Example")

        ui = document_controller.ui

        # user interface

        column = ui.create_column_widget()

        edit_row = ui.create_row_widget()
        edit_row.add(ui.create_label_widget(_("Edit Field")))
        edit_row.add_spacing(12)
        edit_line_edit = ui.create_line_edit_widget()
        def editing_finished(text):
            logging.debug(text)
            edit_line_edit.select_all()
        edit_line_edit.on_editing_finished = editing_finished
        edit_row.add(edit_line_edit)
        edit_row.add_stretch()

        button_row = ui.create_row_widget()
        button_widget = ui.create_push_button_widget(_("Push Me"))
        def button_clicked():
            edit_line_edit.text = unicode()
        button_widget.on_clicked = button_clicked
        button_row.add(button_widget)
        button_row.add_stretch()

        column.add_spacing(8)
        column.add(edit_row)
        column.add(button_row)
        column.add_spacing(8)
        column.add_stretch()

        self.widget = column


workspace_manager = Workspace.WorkspaceManager()
workspace_manager.register_panel(PanelExample, "example-panel", _("Example"), ["left", "right"], "right" )
