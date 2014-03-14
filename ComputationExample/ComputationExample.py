"""
    An example of how to provide a computation algorithm that gets applied to a data item.

    Requires Swift 0.1.6.

    This code is experimental. Please try it out but be aware that the exact technique used
    in this file may or may not be compatible with future versions of the software.
"""

# system imports
# None

# library imports
import numpy

# local imports
from nion.swift import Application


def data_item_computation_min_max_position(data_item):
    """
        Functions of the form data_item_computation_xyz will be found.
        These functions should return a dictionary of property / value
        pairs.
    """

    # check to make sure our data is 1-d and scalar.
    if data_item.is_data_1d and data_item.is_data_scalar_type:
        # grab the numpy array from the data item
        data = data_item.data

        # calculate min/max positions
        pos_min = numpy.argmin(data)
        pos_max = numpy.argmax(data)

        # return the results as a dictionary
        return {"pos-min": pos_min, "pos-max": pos_max}

    # if not 1d and scalar, return None
    return None


Application.app.register_data_item_computation(data_item_computation_min_max_position)
