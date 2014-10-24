"""
Swift scripting example: Process (live operation)
Purpose: This is a template plugin.  Please use it to implement your wildest hopes and dreams.
Author: Michael Sarahan, Nion, March 2014
"""

# 3rd party library imports
import gettext

# Nion imports
from nion.swift import Application
from nion.swift.model import Operation

# Imports from any modules you make


# for translation
_ = gettext.gettext

# This should be a unique identifier for your process.  Try to be descriptive, but not generic (don't conflict with other plugins)
script_id = _("your-process-operation")
# this is the text that the menu will display
process_name = _("Process operation")
# The prefix to prepend to the result image name:
process_prefix = _("Your process done to ")

# you can define any functions to be used in your processing here.
# They do not need to be defined in the class itself.
# By defining them here, you can debug them more easily by directly importing them into your testing environment.
def your_processing_function(data, point_parameter=None, scalar_parameter=0.3, integer_parameter=1):
    # return a copy of the data
    return data.copy()

# From here down, we're using a standard layout so that Swift knows how to execute your process.
# the most important part is the process method, which is where you'll need to add calls to your processing function(s).

class ProcessOperation(Operation.Operation):
    """
    A Swift plugin for you to use.
    """
    def __init__(self):
        # description tells the UI what elements to create for the parameters panel.
        # If you have no parameters, you don't need this.
        description = [
                    { "name": _("Point Example"), "property": "point_example", "type": "point", "default": (0.25, 0.25) },
                    { "name": _("Scalar Example"), "property": "scalar_example", "type": "scalar", "default": 0.3 },
                    { "name": _("Integer Example"), "property": "integer_example", "type": "integer-field", "default": 1 }
                ]
        # runs superclass initialization methods
        super(ProcessOperation, self).__init__(process_name, script_id, description)
        # if you have no parameters, just use this instead:
        #super(ProcessOperation, self).__init__(process_name, script_id)

        # we also have to define data members corresponding to the descriptions above:
        self.point_example = (0.25, 0.25)
        self.scalar_example = 0.3
        self.integer_example = 1

    def process(self, data):
        """
        Swift calls this method when you click on the menu entry for this process,
        and also whenever the parameters for this process or the underlying data change.

        This is where you'll call your methods to actually operate on the data.
        This method should always return a new copy of data
        """
        # a tuple
        point_example = self.get_property("point_example")
        # a floating point scalar
        scalar_example = self.get_property("scalar_example")
        # an integer
        integer_example = self.get_property("integer_example")
        return your_processing_function(data, point_example, scalar_example, integer_example)

    def get_processed_data_shape_and_dtype(self, data_shape, data_dtype):
        """
        Swift needs to know how your process changes the data type and shape, if it changes these.
        If you don't change the data type nor shape, you can delete this method.

        The input parameters are the original input data shape and type.
        The return parameters should be the processed data shape and dtype (in that order!)
        """
        return data_shape, data_dtype

    def get_processed_dimensional_calibrations(self, data_shape, data_dtype, dimensional_calibrations):
        """
        Swift needs to know how your process changes the data type and shape, if it changes these.
        If you don't change calibrations (no new axes, no removed axes), you can just delete this method.

        The input parameters are the original input data shape, type, and list of calibrations
        The return parameters should be the list of calibrations for the processed data.
        """
        return dimensional_calibrations


# The following is code for making this into a menu entry on the processing menu.  You shouldn't need to change it.

def build_menus(document_controller):
    """
    makes the menu entry for this plugin
    """
    operation_callback = lambda: document_controller.add_processing_operation_by_id(script_id, prefix=process_prefix)
    document_controller.processing_menu.add_menu_item(process_name, operation_callback)

Application.app.register_menu_handler(build_menus) # called on import to make the menu entry for this plugin
Operation.OperationManager().register_operation(script_id, lambda: ProcessOperation())
