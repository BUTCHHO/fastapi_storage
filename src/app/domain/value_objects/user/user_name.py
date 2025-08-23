from app.domain.value_objects.base import ValueObject

class UserName(ValueObject):
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'Username must be string, not {type(name)}')
        self.value = name
        super().__init__()

    def __post_init__(self):
        self.validate_name()

    def validate_name(self):
        pass

