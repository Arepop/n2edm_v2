from .items import BaseItem, GroupItem, SetItem, ScheduleItem, TimelineItem
from .exceptions import (
    ItemNotFoundException,
    ItemNameExistsError,
    RequiredValueMissingError,
    ScheduleItemTimeError,
    ScheduleItemCrossError,
)


class BaseItemValidator:

    def __init__(self):
        self.item_model: BaseItem = BaseItem
        self.required_fields = []

    def validate_item(self, itm: BaseItem):
        self.validate_required_data(itm)
        return 0

    def validate_required_data(self, itm: BaseItem):
        for field in self.required_fields:
            if getattr(itm, field) == None:
                raise RequiredValueMissingError(self.item_model, field)


class GroupItemValidator(BaseItemValidator):

    def __init__(self):
        self.item_model: GroupItem = GroupItem
        self.required_fields = ["name"]

    def validate_name(self, itm: BaseItem) -> bool:
        try:
            self.item_model.get(name=itm.name)
        except ItemNotFoundException as e:
            return 0
        else:
            raise ItemNameExistsError(self.item_model, itm.name)

    def validate_item(self, itm: GroupItem):
        super().validate_item(itm)
        self.validate_name(itm)
        return 0


class SetItemValidator(BaseItemValidator):

    def __init__(self):
        self.item_model: SetItem = SetItem
        self.required_fields = ["name", "initial_scpi_command"]

    def validate_name(self, itm: SetItem):
        try:
            valid_item = self.item_model.get(name=itm.name, group_item=itm.group_item)
        except ItemNotFoundException as e:
            return 0
        else:
            if valid_item is itm:
                return 0
            raise ItemNameExistsError(self.item_model, itm.name)

    def validate_item(self, itm: GroupItem):
        super().validate_item(itm)
        self.validate_name(itm)
        return 0


class ScheduleItemValidator(BaseItemValidator):

    def __init__(self):
        self.item_model: ScheduleItem = ScheduleItem
        self.required_fields = ["set_item", "start_time", "stop_time", "sequence", "continuous"]

    def validate_item(self, itm: ScheduleItem):
        super().validate_item(itm)
        self.validate_schedule_item_start_stop_time(itm)
        self.validate_schedule_item_crossing(itm)
        return 0

    def validate_schedule_item_start_stop_time(self, itm: ScheduleItem):
        if itm.start_time < 0 and itm.stop_time < itm.start_time:
            raise ScheduleItemTimeError(self.item_model, itm.start_time, itm.stop_time)
        return 0

    def validate_schedule_item_crossing(self, itm: ScheduleItem):
        left_s, right_s = itm.siblings() if itm.siblings() else (None, None)
        if left_s:
            if itm.start_time < left_s.stop_time:
                raise ScheduleItemCrossError(self.item_model, itm.start_time, itm.stop_time)

        if right_s:
            if itm.stop_time > right_s.start_time:
                raise ScheduleItemCrossError(self.item_model, itm.start_time, itm.stop_time)

        return 0


class TimelineItemValidator(ScheduleItemValidator):
    def __init__(self):
        self.item_model: TimelineItem = TimelineItem
        self.required_fields = ["start_time", "stop_time", "text", "color"]
