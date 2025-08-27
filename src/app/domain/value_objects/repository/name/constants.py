import re
from typing import Final

REPONAME_MAX_LEN: Final[int] = 25
REPONAME_MIN_LEN = 3




PATTERN_START: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Z0-9]",
)
PATTERN_ALLOWED_CHARS: Final[re.Pattern[str]] = re.compile(
    r"[a-zA-Z0-9._-]*",
)
PATTERN_NO_CONSECUTIVE_SPECIALS: Final[re.Pattern[str]] = re.compile(
    r"^[a-zA-Z0-9]+([._-]?[a-zA-Z0-9]+)*[._-]?$",
)
PATTERN_END: Final[re.Pattern[str]] = re.compile(
    r".*[a-zA-Z0-9]$",
)
