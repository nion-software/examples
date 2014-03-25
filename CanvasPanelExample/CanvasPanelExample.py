# standard libraries
import gettext
import logging

# third party libraries
# None

# local libraries
from nion.swift import Panel
from nion.swift import Workspace
from nion.swift.model import DataItem
from nion.ui import CanvasItem
from nion.ui import UserInterfaceUtility

_ = gettext.gettext


class ExampleCanvasItem(CanvasItem.AbstractCanvasItem):

    """ Draws our example canvas; roughly based no HTML5 canvas API. """

    def _repaint(self, drawing_context):

        # canvas size
        canvas_width = self.canvas_size[1]
        canvas_height = self.canvas_size[0]

        drawing_context.save()
        drawing_context.begin_path()
        drawing_context.move_to(0, 0)
        drawing_context.line_to(0, canvas_height)
        drawing_context.line_to(canvas_width, canvas_height)
        drawing_context.line_to(canvas_width, 0)
        drawing_context.close_path()
        gradient = drawing_context.create_linear_gradient(0, 0, 0, canvas_height)
        gradient.add_color_stop(0, '#FF8')
        gradient.add_color_stop(1, '#8F8')
        drawing_context.fill_style = gradient
        drawing_context.fill()
        drawing_context.restore()

        drawing_context.save()
        drawing_context.font = 'normal 11px serif'
        drawing_context.text_align = 'center'
        drawing_context.text_baseline = 'middle'
        drawing_context.fill_style = '#000'
        drawing_context.fill_text(_("Some Title"), canvas_width/2, canvas_height/2+1)
        drawing_context.restore()



class CanvasPanelExample(Panel.Panel):

    """ Make a panel to hold the canvas """

    def __init__(self, document_controller, panel_id, properties):
        super(CanvasPanelExample, self).__init__(document_controller, panel_id, "Canvas Example")

        ui = document_controller.ui

        # user interface

        self.root_canvas_item = CanvasItem.RootCanvasItem(document_controller.ui, properties={"min-height": 40, "max-height": 40})
        self.root_canvas_item.add_canvas_item(ExampleCanvasItem())

        column = self.ui.create_column_widget()
        column.add(self.root_canvas_item.canvas)

        self.widget = column

    def close(self):
        self.root_canvas_item.close()


workspace_manager = Workspace.WorkspaceManager()
workspace_manager.register_panel(CanvasPanelExample, "canvas-example-panel", _("Canvas Example"), ["left", "right"], "right", {"width": 320, "height": 40})
