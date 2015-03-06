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

# local libraries
# None


# for translation
_ = gettext.gettext


class Stamp2dOperationDelegate(object):

    def __init__(self, api):
        self.__api = api
        self.operation_id = "stamp-example-operation"
        self.operation_name = _("Stamp (Example)")
        self.operation_prefix = _("Stamped ")
        default_source_rectangle = (0.1, 0.3), (0.2, 0.3)  # must be plain tuple; origin (y, x), size (height, width)
        default_position = 0.5, 0.6  # must be plain tuple: y, x
        self.operation_description = [
            {"name": _("Source Rectangle"), "property": "bounds", "type": "rectangle", "default": default_source_rectangle},
            {"name": _("Destination Position"), "property": "position", "type": "point", "default": default_position}
        ]
        self.operation_region_bindings = {
            "source-region": {"type": "rectangle-region", "bindings": [{"bounds": "bounds"}]},
            "destination": {"type": "point-region", "bindings": [{"position": "position"}]}
        }

    def close(self):
        # close will be called if the extension is unloaded.
        pass

    def can_apply_to_data(self, data_and_metadata):
        return data_and_metadata.is_data_2d

    def get_processed_data_and_metadata(self, data_and_metadata, parameters):
        api = self.__api
        data = data_and_metadata.data
        shape = data_and_metadata.data_shape
        data_copy = data.copy()
        bounds_origin, bounds_size = parameters.get("bounds")  # origin, size
        bounds_origin_y, bounds_origin_x = bounds_origin  # y, x
        bounds_size_height, bounds_size_width = bounds_size  # height, width
        bounds_top = bounds_origin_y
        bounds_height = bounds_size_height
        bounds_left = bounds_origin_x
        bounds_width = bounds_size_width
        position_y, position_x = parameters.get("position")  # y, x
        source_origin_y = int(bounds_top * shape[0])
        source_origin_x = int(bounds_left * shape[1])
        source_size_height = int(bounds_height * shape[0])
        source_size_width = int(bounds_width * shape[1])
        source_bounds_top = source_origin_y
        source_bounds_left = source_origin_x
        source_bounds_bottom = source_origin_y + source_size_height
        source_bounds_right = source_origin_x + source_size_width
        destination_center_y = int(position_y * shape[0])
        destination_center_x = int(position_x * shape[1])
        destination_bounds_top = int(destination_center_y - source_size_height * 0.5)
        destination_bounds_bottom = destination_bounds_top + source_size_height
        destination_bounds_left = int(destination_center_x - source_size_width * 0.5)
        destination_bounds_right = destination_bounds_left + source_size_width
        source_slice = data[source_bounds_top:source_bounds_bottom, source_bounds_left:source_bounds_right]
        destination_slice = data_copy[destination_bounds_top:destination_bounds_bottom, destination_bounds_left:destination_bounds_right]
        destination_slice[:] = source_slice[:]
        intensity_calibration = data_and_metadata.intensity_calibration
        dimensional_calibrations = data_and_metadata.dimensional_calibrations
        metadata = data_and_metadata.metadata
        return api.create_data_and_metadata_from_data(data_copy, intensity_calibration, dimensional_calibrations, metadata)


class OperationExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.operation_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__operation_ref = api.create_unary_operation(Stamp2dOperationDelegate(api))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__operation_ref.close()
        self.__operation_ref = None
