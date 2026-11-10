# system imports
import gettext
import logging
import typing

# third part imports
import numpy

# local libraries
from nion.swift import Facade

_ = gettext.gettext


class MenuItemDelegate(object):
    def __init__(self) -> None:
        self.menu_id = "example_menu"
        self.menu_name = _("Examples")
        self.menu_before_id = "window_menu"
        self._menu_item_name = _("Example Menu Item")

    @property
    def menu_item_name(self) -> str:
        return self._menu_item_name

    def menu_item_execute(self, document_window: Facade.DocumentWindow) -> None:
        document_window.add_data(numpy.random.randn(64, 64), _("Random 64"))
        logging.info("MenuItemDelegate menu_item_execute has been called.")

    def close(self) -> None:
        pass

class MenuExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.menu_example"

    def __init__(self, api_broker: Facade.APIBroker) -> None:
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item_ref = api.create_menu_item(MenuItemDelegate())

    def close(self) -> None:
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__menu_item_ref.close()
        self.__menu_item_ref = None
