import numpy

from PIL import Image

from nion.typeshed import Interactive_1_0 as Interactive
from nion.typeshed import API_1_0 as API
from nion.typeshed import UI_1_0 as UI

def script_main(api_broker):
    interactive = api_broker.get_interactive(Interactive.version)  # type: Interactive
    api = api_broker.get_api(API.version, UI.version)  # type: API
    data_item = api.application.document_controllers[0].target_data_item
    data = data_item.data
    if len(data.shape) == 3:
        name = interactive.get_string("TIFF series name:", "Image")
        for z in range(data.shape[0]):
            layer = data[z, ...]
            layer = (255 * (layer - numpy.amin(layer)) / numpy.ptp(layer)).astype(numpy.uint8)
            Image.fromarray(layer).save("/Users/cmeyer/Desktop/movies/{}_{}.tiff".format(name, z))
