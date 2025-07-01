class FieldUniqueViolation(Exception):
    def __init__(self, **kwargs):
        msg = f'Record with kwargs {kwargs} is violating unique flag'
        super().__init__(msg)

