from .backend.items import BaseItem, ScheduleItem, SetItem, GroupItem, TimelineItem
from .backend.sequencer import Sequencer
from .backend.validators import (
    BaseItemValidator,
    ScheduleItemValidator,
    GroupItemValidator,
    SetItemValidator,
    TimelineItemValidator,
)
from .backend.exceptions import (
    ItemNotFoundException,
    ItemExistsError,
    ItemNameExistsError,
    ScheduleItemCrossError,
)
from .backend.middleware import ItemMiddleware


class BaseItemAPI:

    def __init__(self):
        self.validator = BaseItemValidator()
        self.item_model = BaseItem
        self.middleware = ItemMiddleware()

    def create_item(self, item_data):
        new_item = self.item_model.create(**item_data)
        self.validator.validate_item(new_item)
        new_item.add()
        return new_item

    def bulk_create_items(self, items_data):
        return [self.create_item(item_data) for item_data in items_data]

    def update_item(self, uid, new_data):
        current_item = self.get_item(uid)
        old_data = current_item.as_dict()
        current_item.update(**new_data)
        try:
            self.validator.validate_item(current_item)
        except ItemNameExistsError:
            current_item.update(**old_data)
            if hasattr(current_item, "name"):
                raise ItemNameExistsError(self.item_model, current_item.name)
            raise ItemNameExistsError(self.item_model, current_item.set_item.name)
        except ScheduleItemCrossError:
            current_item.update(**old_data)
            raise ScheduleItemCrossError(
                self.item_model, current_item.start_time, current_item.stop_time
            )
        return current_item

    def remove_item(self, uid):
        item = self.get_item(uid)
        self.middleware.position_if_last_in_group(item)
        item.delete()
        return 0

    def get_item(self, uid):
        return self.item_model.get(uid=uid)

    def get_all_items(self):
        return self.item_model.all()

    def clear(self):
        for item in self.get_all_items():
            self.remove_item(item.uid)
        return 0

    def filter(self, **search_criteria):
        return self.item_model.filter(**search_criteria)


class GroupAPI(BaseItemAPI):
    def __init__(self):
        super().__init__()
        self.validator = GroupItemValidator()
        self.item_model = GroupItem


class SetAPI(BaseItemAPI):
    def __init__(self):
        super().__init__()
        self.validator = SetItemValidator()
        self.item_model = SetItem

    def create_item(self, item_data):
        if isinstance(item_data.get("group_item"), int):
            item_data["group_item"] = self._get_group(uid=item_data["group_item"])
        new_item = self.item_model.create(**item_data)
        self.validator.validate_item(new_item)
        new_item.add()
        return new_item

    def _get_group(self, uid):
        group_api = GroupAPI()
        return group_api.get_item(uid)


class ScheduleAPI(BaseItemAPI):
    def __init__(self):
        super().__init__()
        self.validator = ScheduleItemValidator()
        self.item_model = ScheduleItem

    # Frontend gives only uids if object exist, so remember to pass primary keys not names!
    def create_item(self, item_data):
        if isinstance(item_data["set_item"], int):
            item_data["set_item"] = self.get_item(uid=item_data["set_item"])
        new_item = self.item_model.create(**item_data)
        try:
            item = self.get_item(new_item.uid)
        except ItemNotFoundException:
            self.middleware.set_position(new_item)
            self.validator.validate_item(new_item)
            new_item.add()
        else:
            raise ItemExistsError(item.uid)

        return new_item

    def swap_item_positions(self, item_left, item_right):
        pass


class SequencerAPI:
    def __init__(self):
        self.sequencer = Sequencer()

    def get_sequence(self):
        return self.sequencer.decode()

    def set_number_of_cycles(self, number_of_cycles):
        return self.sequencer.set_number_of_cycles(number_of_cycles)

    def get_number_of_cycles(self):
        return self.sequencer.number_of_cycles
