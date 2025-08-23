from app.domain.value_objects.base import ValueObject

class UserName(ValueObject):
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise TypeError(f'Username must be string, not {type(name)}')
        self.name = name
        super().__init__()
