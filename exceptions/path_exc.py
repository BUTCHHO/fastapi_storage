class PathGoesBeyondLimits(Exception):
    def __init__(self, path):
        msg = f'path {path} is goes beyond the permitted limits'
        super().__init__(msg)