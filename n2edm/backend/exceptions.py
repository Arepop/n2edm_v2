class ItemNotFoundException(Exception):
    def __init__(self, cls):
        self.message = (
            f"{cls.__name__} instance you are looking for is not in the scope of application data."
        )

    def __str__(self):
        return self.message


class ItemNameExistsError(Exception):
    def __init__(self, cls, name):
        self.message = f"{cls.__name__} instance with that name '{name}' alredy exists. Please select other name"

    def __str__(self):
        return self.message


class RequiredValueMissingError(Exception):
    def __init__(self, cls, attribute):
        self.message = f"{cls.__name__} instance require '{attribute}' non empty value"

    def __str__(self):
        return self.message


class ScheduleItemTimeError(Exception):
    def __init__(self, cls, start_time, stop_time):
        self.message = f"{cls.__name__} time validation fail. '{start_time}' and '{stop_time}' does not meet requirements"

    def __str__(self):
        return self.message


class ScheduleItemCrossError(Exception):
    def __init__(self, cls, start_time, stop_time):
        self.message = f"{cls.__name__} time validation fail. '{start_time}' or '{stop_time}' cross other schedule items"

    def __str__(self):
        return self.message


class ItemExistsError(Exception):
    def __init__(self, cls, uid):
        self.message = (
            f"{cls.__name__} instance with uid '{uid}' alredy exists. Please select other name"
        )

    def __str__(self):
        return self.message
