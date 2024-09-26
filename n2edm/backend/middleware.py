from .items import GroupItem, SetItem

class ItemMiddleware:
    def __init__(self):
        self.position = 0
        
    def position_if_last_in_group(self, item):
        if type(item) == GroupItem:
            item.position = None
        elif not item.siblings():
            if item.group_item:
                item.group_item.position = None
            elif type(item) == SetItem:
                item.position = None
            else:
                item.set_item.position = None
        else:
            return 0

        if not item.position:
            self.reposition()
        return 0

    def reposition(self):
        all_items = [item for item in GroupItem.all() + SetItem.filter(group_item=None) if item.position is not None]
        sorted_items = sorted(all_items, key=lambda item: item.position)
        for new_position, item in enumerate(sorted_items):
            item.position = new_position
        self.position -= 1
        return 0
    
    def set_position(self, new_item):
        if new_item.position == None and new_item.group_item:
            new_item.group_item.position = self.position
            self.position += 1
        elif new_item.position == None:
            new_item.set_item.position = self.position
            self.position += 1
        return 0
    