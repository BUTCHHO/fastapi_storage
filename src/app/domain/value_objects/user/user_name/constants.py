import re
from typing import Final

USERNAME_MAX_LEN: Final[int] = 25
USERNAME_MIN_MEN = 2




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
