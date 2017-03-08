import copy
import math
import random
import time

import numpy

from nion.typeshed import Interactive_1_0 as Interactive
from nion.typeshed import API_1_0 as API
from nion.typeshed import UI_1_0 as UI


def graph(interactive: Interactive, api: API):
    interactive.print("Starting graph.")
    library = api.library
    data = numpy.zeros((4, 200))
    data_item = None
    for d in library.data_items:
        if d.metadata.get("is_my_graph"):
            data_item = d
            break
    if not data_item:
        data_descriptor = api.create_data_descriptor(is_sequence=False, collection_dimension_count=1, datum_dimension_count=1)
        xdata = api.create_data_and_metadata(data, data_descriptor=data_descriptor)
        data_item = library.create_data_item_from_data_and_metadata(xdata)
        metadata = data_item.metadata
        metadata["is_my_graph"] = True
        data_item.set_metadata(metadata)
    document_controller = api.application.document_controllers[0]
    document_controller.display_data_item(data_item)
    for i in range(1000):
        time.sleep(0.05)
        if interactive.cancelled:
            break
        index = min(i, 199)
        xdata = copy.deepcopy(data_item.xdata)
        data = xdata.data
        if i >= 200:
            data[0:4, 0:199] = data[0:4, 1:200]
        data[0, index] = i % 200
        data[1, index] = random.randint(0, 200)
        data[2, index] = 100 + 75 * math.sin(2 * math.pi * 4 * i / 200)
        data[3, index] = 120 + 60 * math.cos(2 * math.pi * 3 * i / 200)
        data_item.xdata = xdata


def script_main(api_broker):
    interactive = api_broker.get_interactive(Interactive.version)  # type: Interactive
    api = api_broker.get_api(API.version, UI.version)  # type: API
    graph(interactive, api)
