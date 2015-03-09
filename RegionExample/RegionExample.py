# system imports
import gettext
import logging

# third part imports
# None

# local imports
# None

_ = gettext.gettext


class CreateSomeRegionsMenuItemDelegate(object):

    def __init__(self):
        self.menu_item_name = _("Create Some Regions")  # menu item name

    def menu_item_execute(self, document_controller):
        data_item = document_controller.target_data_item
        if data_item:
            data_item.add_rectangle_region(0.3, 0.3, 0.3, 0.4)
            data_item.add_point_region(0.8, 0.7)


class RemoveRegionMenuItemDelegate(object):

    def __init__(self):
        self.menu_item_name = _("Remove First Region")  # menu item name

    def menu_item_execute(self, document_controller):
        data_item = document_controller.target_data_item
        if data_item:
            regions = data_item.regions
            if len(regions) > 0:
                data_item.remove_region(regions[0])


class SummarizeRegionsMenuItemDelegate(object):

    def __init__(self):
        self.menu_item_name = _("Summarize Regions")  # menu item name

    def menu_item_execute(self, document_controller):
        data_item = document_controller.target_data_item
        if data_item:
            regions = data_item.regions
            for region in regions:
                if region.type == "rectangle-region":
                    logging.debug("rectangle center:%s size:%s", region.get_property("center"), region.get_property("size"))
                elif region.type == "point-region":
                    logging.debug("point position:%s", region.get_property("position"))
                elif region.type == "line-region":
                    logging.debug("point start:%s end:%s", region.get_property("start"), region.get_property("end"))
                elif region.type == "ellipse-region":
                    logging.debug("ellipse center:%s size:%s angle:%s", region.get_property("center"), region.get_property("size"), region.get_property("angle"))
                elif region.type == "interval-region":
                    logging.debug("interval start:%s end:%s", region.get_property("start"), region.get_property("end"))


class RegionExampleExtension(object):

    # required for Swift to recognize this as an extension class.
    extension_id = "nion.swift.examples.region_example"

    def __init__(self, api_broker):
        # grab the api object.
        api = api_broker.get_api(version="1", ui_version="1")

        # be sure to keep a reference or it will be closed immediately.
        self.__menu_item1_ref = api.create_menu_item(CreateSomeRegionsMenuItemDelegate())
        self.__menu_item2_ref = api.create_menu_item(RemoveRegionMenuItemDelegate())
        self.__menu_item3_ref = api.create_menu_item(SummarizeRegionsMenuItemDelegate())

    def close(self):
        # close will be called when the extension is unloaded. in turn, close any references so they get closed. this
        # is not strictly necessary since the references will be deleted naturally when this object is deleted.
        self.__menu_item1_ref.close()
        self.__menu_item2_ref.close()
        self.__menu_item3_ref.close()
