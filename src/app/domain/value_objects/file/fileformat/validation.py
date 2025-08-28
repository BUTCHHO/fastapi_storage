from app.domain.value_objects.file.fileformat.constants import ALLOWED_FILE_FORMATS
from app.domain.exceptions.file import FileFormatError


def validate_file_format(file_format_value):
    if file_format_value not in ALLOWED_FILE_FORMATS:
        raise FileFormatError(f'{file_format_value} file format is not allowed')
