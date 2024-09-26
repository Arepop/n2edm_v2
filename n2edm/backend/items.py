from .interface.items import *
from .exceptions import ItemNotFoundException
from functools import total_ordering
from uuid import uuid1


class BaseItem(IBaseItem):
    """Main class for creating objects in application. Inherit after this class to create your own BaseItem class.
    Containt all required functions for crud of objects, as well as additional data for serializing (Models dependency).
    Args:
        set_id: id of a set in database
        set_name: user readable name for quick selecting data
        items: List of all itmes in scope
    """

    set_id: str = None
    set_name: str = None
    items: list = []

    def __init__(self, *args, **kwargs):
        """Class instance constructor."""
        BaseItem.set_id = kwargs.get("set_id", id(BaseItem))
        self.uid: int = None

        for arg, value in kwargs.items():
            getattr(self, arg)
            setattr(self, arg, value)

    def __repr__(self) -> str:
        """Text representation of class instance

        Returns:
            str: Text format of class instance
        """
        rv = f"{self.__class__.__name__}{self.__dict__}"
        return rv

    def set_uid(self):
        """Sets item its primary key"""
        self.uid = uuid1().int

    @classmethod
    def all(cls) -> tuple:
        """Returnes all objects of given class

        Returns:
            tuple: tuple of all objects in given class
        """
        if cls == BaseItem:
            return cls.items
        return list(filter(lambda obj: type(obj) == cls, cls.items))

    @classmethod
    def get(cls, *args, **kwargs):
        """Gets single object based on given arguments

        Raises:
            ItemNotFoundException: If there is no objects in scope error rises
            AttributeError: Attribute does not exist in object hence it cannot be read

        Returns:
            BaseItem: found object
        """
        matched_items = cls.filter(*args, **kwargs)
        if not matched_items:
            raise ItemNotFoundException(cls)

        return matched_items[0]

    @classmethod
    def filter(cls, *args, **search_criteria):
        """Filters and search for all objects with matching criteria

        Raises:
            AttributeError: Attribute does not exist in object hence it cannot be read

        Returns:
            list: List of matched objects
        """
        matched_objects = []
        for obj in cls.all():
            for key, value in search_criteria.items():
                if getattr(obj, key) != value:
                    break
            else:
                matched_objects.append(obj)

        return matched_objects

    @classmethod
    def create(cls, *args, **kwargs) -> int:
        """Creates object instance based on given data

        Returns:
            BaseItem: instance of an BaseItem class
        """
        new_object = cls(**kwargs)
        return new_object

    def add(self):
        """Adds self to scope of application"""
        if not self.uid:
            self.set_uid()
        BaseItem.items.append(self)

    def update(self, *args, **kwargs) -> object:
        """Updates existing object with given data

        Raises:
            AttributeError: Attribute does not exist in object hence it cannot be updated

        Returns:
            Object: updated instance of an Object class
        """
        for arg, value in kwargs.items():
            setattr(self, arg, value)

    def delete(self):
        """Simply removes itself from object list"""
        BaseItem.items.remove(self)

    def as_dict(self):
        """Gives item in dict format

        Returns:
            dict: dict with item attributes
        """
        class_attributes = {"set_id": self.set_id, "set_name": self.set_name}
        class_attributes.update(self.__dict__)

        for key in class_attributes.keys():
            class_attributes[key.lstrip("_")] = class_attributes.pop(key)
        return class_attributes


class GroupItem(BaseItem, IGroupItem):
    def __init__(self, *args, **kwargs):
        self.name: str = None
        self.position: int = None
        super().__init__(*args, **kwargs)

    @property
    def position(self):
        """Returns position of GroupItem in schedule

        Returns:
            int: Position of GroupItem
        """
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        for set_item in self.get_set_items():
            set_item.position = position

    def get_set_items(self):
        """Gives all set_itemsItems contained in GroupItem

        Returns:
            list: List of all SetItems that share same GroupItem
        """
        return SetItem.filter(group_item=self)

    def children(self):
        """Gives us all ScheduleItem that shares the same gorup

        Returns:
            list: List of schedule items
        """
        return ScheduleItem.filter(group_item=self)

    def delete(self):
        """Remove item from scome"""
        for child in self.get_set_items():
            child.delete()
        super().delete()


class SetItem(BaseItem, ISetItem):
    def __init__(self, *args, **kwargs):
        self.name: str = None
        self.group_item: GroupItem = None
        self.initial_scpi_command: str = None
        self.final_scpi_command: str = None
        self.duration: int = None
        self.color: str = None
        self.params: str = None
        self.position: str = None
        super().__init__(*args, **kwargs)

    @property
    def position(self):
        if self.group_item:
            return self.group_item.position
        return self._position

    @position.setter
    def position(self, position):
        if not self.group_item:
            self._position = position
        else:
            self._position = self.group_item.position

    def children(self):
        """Gives all ScheduleItems contained in SetItem

        Returns:
            generator: Generator of all ScheduleItems that share same SetItem
        """
        all_children = ScheduleItem.filter(set_item=self)
        return all_children

    def delete(self):
        for child in self.children():
            child.delete()
        super().delete()

    def siblings(self):
        if self.group_item:
            sib = self.group_item.get_set_items()
            sib.remove(self)
            return sib
        return None


@total_ordering
class ScheduleItem(BaseItem, IScheduleItem):
    def __init__(self, *args, **kwargs):
        """Constructor for class instance"""
        self.set_item: SetItem = None
        self.start_time: int = None
        self.stop_time: int = None
        self.sequence: str = "main"
        self.continuous: bool = False
        super().__init__(*args, **kwargs)

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __eq__(self, other):
        try:
            return self.uid == other.uid
        except AttributeError as e:
            super().__eq__(other)

    def siblings(self):
        """Returns closest siblings To start time in order left to right.
        Where left is closest to ScheduleItem start and right is closest to left.
        """
        children = self.group_item.children() if self.group_item else self.set_item.children()
        if self not in children:
            children.append(self)
        children = sorted(children)
        sib_l = children[children.index(self) - 1] if children.index(self) > 0 else None
        sib_r = (
            children[children.index(self) + 1]
            if children.index(self) < len(children) - 1
            else None
        )
        siblings_rv = (sib_l, sib_r)
        if sib_l or sib_r:
            return siblings_rv
        return None

    @property
    def position(self):
        return self.set_item.position

    @property
    def color(self):
        return self.set_item.color

    @property
    def group_item(self):
        return self.set_item.group_item


@total_ordering
class TimelineItem(BaseItem, IScheduleItem):
    def __init__(self, *args, **kwargs):
        """Constructor for class instance"""
        self.start_time: int = None
        self.stop_time: int = None
        self.text: str = None
        self.position: int = -1
        self.color: str = None
        super().__init__(*args, **kwargs)

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __eq__(self, other):
        return self.start_time == other.start_time
