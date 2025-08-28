import re

MAX_FILENAME_LENGTH = 100
MIN_FILENAME_LENGTH = 1


FILENAME_PATTERN = re.compile(r'^(?!\.)(?!.*\.\.)(?!.*\.$)[A-Za-z0-9_-]+$')
