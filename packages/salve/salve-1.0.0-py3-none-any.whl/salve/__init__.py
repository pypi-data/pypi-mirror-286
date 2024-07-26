from beartype.claw import beartype_this_package

beartype_this_package()

from .ipc import IPC  # noqa: F401, E402
from .misc import (  # noqa: F401, E402
    AUTOCOMPLETE,
    COMMANDS,
    DEFINITION,
    EDITORCONFIG,
    HIGHLIGHT,
    LINKS_AND_CHARS,
    REPLACEMENTS,
    Response,
)
from .server_functions import is_unicode_letter  # noqa: F401, E402
