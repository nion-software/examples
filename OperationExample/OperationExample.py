"""
    An example of how to provide a live operation for data items.

    Requires Swift 0.3.3.

    This code is experimental. Please try it out but be aware that the exact technique used
    in this file may or may not be compatible with future versions of the software.
"""

# system imports
import gettext
import logging

# library imports
# None

# local imports
from nion.swift import Application
from nion.swift.model import Operation
from nion.swift.model import DataItem
from nion.ui import Geometry


# for translation
_ = gettext.gettext


class Stamp2dOperation(Operation.Operation):

    """
        Provide a source rectangle and a destination location, copy the source data to the area centered at destination.
    """

    def __init__(self):
        description = [
            { "name": _("Source"), "property": "bounds", "type": "rectangle", "default": ((0.1, 0.1), (0.2, 0.2)) },
            { "name": _("Destination"), "property": "position", "type": "point", "default": (0.5, 0.5)}
        ]
        super(Stamp2dOperation, self).__init__(_("Stamp"), "stamp-example-operation", description)
        self.region_types = { "source-region": "rectangle-region", "destination": "point-region" }
        self.region_bindings = {
            "source-region": [Operation.RegionBinding("bounds", "bounds")],
            "destination": [Operation.RegionBinding("position", "position")]
        }

    def get_processed_data(self, data_sources, values):
        # doesn't do any bounds checking
        data = data_sources[0].data
        shape = data_sources[0].data_shape
        if data is None or shape is None:
            return None
        data_copy = data.copy()
        bounds = Geometry.FloatRect.make(values.get("bounds"))  # get bounds tuple and convert to FloatRect
        position = Geometry.FloatPoint.make(values.get("position"))  # get position tuple and convert to FloatPoint
        source_origin = Geometry.IntPoint(y=bounds.top * shape[0], x=bounds.left * shape[1])  # convert to IntPoint
        source_size = Geometry.IntSize(height=bounds.height * shape[0], width=bounds.width * shape[1])  # convert to IntSize
        source_bounds = Geometry.IntRect(source_origin, source_size)
        destination_center = Geometry.IntPoint(y=position.y * shape[0], x=position.x * shape[1])  # convert to IntPoint
        destination_bounds = Geometry.IntRect.from_center_and_size(destination_center, source_size)
        source_slice = data[source_bounds.top:source_bounds.bottom, source_bounds.left:source_bounds.right]
        destination_slice = data_copy[destination_bounds.top:destination_bounds.bottom, destination_bounds.left:destination_bounds.right]
        destination_slice[:] = source_slice[:]
        return data_copy


Operation.OperationManager().register_operation("stamp-example-operation", lambda: Stamp2dOperation())

def processing_stamp(document_controller):
    display_specifier = document_controller.selected_display_specifier
    buffered_data_source = display_specifier.buffered_data_source if display_specifier else None
    if buffered_data_source and len(buffered_data_source.dimensional_shape) == 2:
        operation = Operation.OperationItem("stamp-example-operation")
        operation.establish_associated_region("source-region", buffered_data_source)
        operation.establish_associated_region("destination", buffered_data_source)
        return document_controller.add_processing_operation(display_specifier.buffered_data_source_specifier, operation, prefix=_("Stamped "))
    return DataItem.DisplaySpecifier()

def build_menus(document_controller):
    """ Make menu item for this operation. """
    document_controller.processing_menu.add_menu_item(_("Stamp (Example)"), lambda: processing_stamp(document_controller))

Application.app.register_menu_handler(build_menus) # called on import to make the menu entry for this plugin
