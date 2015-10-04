# standard libraries
import gettext
import logging

# third party libraries
# None

# local libraries
# None

_ = gettext.gettext


class CanvasWidgetDelegate(object):

    """ Draws our example canvas; roughly based no HTML5 canvas API. """

    def __init__(self):
        pass

    def _repaint(self, drawing_context, canvas_size):
        # canvas size
        canvas_width = canvas_size.width
        canvas_height = canvas_size.height

        drawing_context.save()
        drawing_context.begin_path()
        drawing_context.move_to(0, 0)
        drawing_context.line_to(0, canvas_height)
        drawing_context.line_to(canvas_width, canvas_height)
        drawing_context.line_to(canvas_width, 0)
        drawing_context.close_path()
        gradient = drawing_context.create_linear_gradient(canvas_width, canvas_height, 0, 0, 0, canvas_height)
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



class CanvasPanelDelegate(object):
    """ Example panel with a canvas item embedded. """

    def __init__(self):
        self.panel_id = "canvas-example-panel"
        self.panel_name = _("Canvas Example")
        self.panel_positions = ["left", "right"]
        self.panel_position = "right"
        self.panel_properties = {"min-width": 320, "min-height": 40, "max-height": 40}

    def close(self):
        # close will be called if the extension is unloaded.
        pass

    def create_panel_widget(self, ui, document_controller):
        canvas_widget_delegate = CanvasWidgetDelegate()
        canvas_widget = ui.create_canvas_widget(height=40)
        canvas_widget.on_repaint = canvas_widget_delegate._repaint
        return canvas_widget


class CanvasPanelExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.canvas_panel_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__panel_ref = api.create_panel(CanvasPanelDelegate())

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__panel_ref.close()
        self.__panel_ref = None
