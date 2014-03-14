# system imports
import gettext
import logging

# local imports
from nion.swift import Application

_ = gettext.gettext


# represents a global function, not associated with a document controller
def global_function():
    logging.info("global_function has been called.")


# represents a function, associated with a document controller
def document_controller_command(document_controller):
    document_model = document_controller.document_model
    logging.info("document_controller_command has been called.")
    logging.info("document model contains %s data items", len(document_model.data_items))


def pane_command(document_controller):
    data_item = document_controller.selected_data_item
    logging.info("pane_command has been called.")
    if data_item is not None:
        logging.info("selected data item shape is %s", data_item.spatial_shape)
    else:
        logging.info("no data item is selected")


# the build_menus function will be called whenever a new document window is created.
# it will be passed the document_controller.
def build_menus(document_controller):
    # check to see if the document controller already has an example menu member.
    example_menu = document_controller.get_or_create_menu("example_menu", _("Examples"), "window_menu")

    # the lambda function will be called when the user chooses this menu item.
    example_menu.add_menu_item(_("Call Global Function..."), lambda: global_function())

    # the lambda function passes document controller from this scope.
    example_menu.add_menu_item(_("Call Document Controller Command..."),
                               lambda: document_controller_command(document_controller))

    # the lambda function passes document controller from this scope.
    example_menu.add_menu_item(_("Call Data Pane Command..."), lambda: pane_command(document_controller))


# register the menu handler with the application.
Application.app.register_menu_handler(build_menus)
