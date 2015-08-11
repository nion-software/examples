# standard libraries
import contextlib
import gettext
import logging
import threading
import time

# third party libraries
# None

# local libraries
# None


_ = gettext.gettext


class MenuItem1Delegate(object):

    def __init__(self, api, scan):
        self.__api = api
        self.menu_item_name = _("Record 1")  # menu item name

    def menu_item_execute(self, document_controller):
        scan = self.__api.get_hardware_source_by_id("scan_controller", "1")

        # record style 1 is a synchronous call to record and grab the frames.
        def do_record():
            frame_parameters = scan.get_default_frame_parameters()
            frame_parameters["size"] = 600, 600  # y, x
            logging.debug(scan.record()[0].dimensional_shape)

        # record should be done in a thread so it doesn't lock the UI
        # threading.Thread(target=record_style1).start()
        threading.Thread(target=do_record).start()


class MenuItem2Delegate(object):

    def __init__(self, api, scan):
        self.__api = api
        self.menu_item_name = _("Record 2")  # menu item name

    def menu_item_execute(self, document_controller):
        scan = self.__api.get_hardware_source_by_id("scan_controller", "1")

        # record style 2 allows you to start the record, do other things, and grab the
        # frames at the end.
        def do_record():
            frame_parameters = scan.get_default_frame_parameters()
            frame_parameters["size"] = 500, 500  # y, x
            channels_enabled = [True, True, False, False]
            with contextlib.closing(scan.create_record_task(frame_parameters=frame_parameters, channels_enabled=channels_enabled)) as record_task:
                logging.debug(record_task.grab()[0].dimensional_shape)

        # record should be done in a thread so it doesn't lock the UI
        # threading.Thread(target=record_style1).start()
        threading.Thread(target=do_record).start()


class MenuItem3Delegate(object):

    def __init__(self, api, scan):
        self.__api = api
        self.menu_item_name = _("Record 3")  # menu item name

    def menu_item_execute(self, document_controller):
        scan = self.__api.get_hardware_source_by_id("scan_controller", "1")
        camera = self.__api.get_hardware_source_by_id("simulator_2d", "1")

        # record style 2 allows you to start the record, do other things, and grab the
        # frames at the end.
        def do_record():
            frame_parameters = scan.get_default_frame_parameters()
            frame_parameters["size"] = 500, 500  # y, x
            channels_enabled = [True, True, False, False]
            with contextlib.closing(scan.create_record_task(frame_parameters=frame_parameters, channels_enabled=channels_enabled)) as record_task:
                logging.debug("start %s", time.time())
                camera_parameters = camera.get_default_frame_parameters()
                camera_parameters["exposure_ms"] = 10
                with contextlib.closing(camera.create_view_task(frame_parameters=camera_parameters)) as camera_view:
                    while not record_task.is_finished:
                        logging.debug("%s: %s", time.time(), camera_view.grab_next_to_finish()[0].dimensional_shape)
                logging.debug(record_task.grab()[0].dimensional_shape)
                logging.debug("end %s", time.time())

        # record should be done in a thread so it doesn't lock the UI
        # threading.Thread(target=record_style1).start()
        threading.Thread(target=do_record).start()


class ScanAcquisitionExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.scan_acquisition"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")
        scan = api.get_hardware_source_by_id("scan_controller", "1")
        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item1_ref = api.create_menu_item(MenuItem1Delegate(api, scan))
        self.__menu_item2_ref = api.create_menu_item(MenuItem2Delegate(api, scan))
        self.__menu_item3_ref = api.create_menu_item(MenuItem3Delegate(api, scan))

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__menu_item1_ref.close()
        self.__menu_item1_ref = None
        self.__menu_item2_ref.close()
        self.__menu_item2_ref = None
        self.__menu_item3_ref.close()
        self.__menu_item3_ref = None
