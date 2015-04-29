# standard libraries
import gettext
import math
import time

# third party libraries
import numpy

# local libraries
# None


_ = gettext.gettext


class RandomCaptureHardwareSourceDelegate(object):

    def __init__(self, api):
        self.__api = api
        self.hardware_source_id = "random_capture"
        self.hardware_source_name = _("Random Capture")

    def start_acquisition(self):
        self.x_phase = 0.0
        self.y_phase = 0.0
        self.x_frequency = 3.0
        self.y_frequency = 1.2

    def stop_acquisition(self):
        pass

    def acquire_data_and_metadata(self):
        api = self.__api
        time.sleep(0.1)
        data = numpy.random.randn(256, 256)
        ramp_x, ramp_y = numpy.ogrid[0:256, 0:256]
        data *= numpy.sin(2 * math.pi * self.x_frequency * ramp_x / 256 + self.x_phase) * numpy.cos(2 * math.pi * self.y_frequency * ramp_y / 256 + self.y_phase)
        self.x_phase += 0.08
        self.y_phase += 0.05
        return api.create_data_and_metadata_from_data(data)


class RandomCaptureExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.random_capture_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        # be sure to keep a reference or it will be closed immediately.
        self.__hardware_source_ref = api.create_hardware_source(RandomCaptureHardwareSourceDelegate(api))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__hardware_source_ref.close()
        self.__hardware_source_ref = None
