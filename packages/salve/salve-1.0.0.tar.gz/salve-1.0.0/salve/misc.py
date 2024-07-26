from multiprocessing.queues import Queue as GenericQueueClass
from pathlib import Path
from typing import TYPE_CHECKING, NotRequired, TypedDict

from token_tools import Token

COMMANDS: list[str] = [
    "autocomplete",
    "replacements",
    "highlight",
    "editorconfig",
    "definition",
    "links_and_chars",
]

COMMAND = str
AUTOCOMPLETE: COMMAND = COMMANDS[0]
REPLACEMENTS: COMMAND = COMMANDS[1]
HIGHLIGHT: COMMAND = COMMANDS[2]
EDITORCONFIG: COMMAND = COMMANDS[3]
DEFINITION: COMMAND = COMMANDS[4]
LINKS_AND_CHARS: COMMAND = COMMANDS[5]


class Message(TypedDict):
    """Base class for messages in and out of the server"""

    id: int
    type: str  # Can be "request", "response", "notification"


class Request(Message):
    """Request results/output from the server with command specific input"""

    command: str  # Can only be commands in COMMANDS
    file: str
    expected_keywords: NotRequired[list[str]]  # autocomplete, replacements
    current_word: NotRequired[str]  # autocomplete, replacements, definition
    language: NotRequired[str]  # highlight
    text_range: NotRequired[tuple[int, int]]  # highlight, links_and_chars
    file_path: NotRequired[Path | str]  # editorconfig
    definition_starters: NotRequired[
        list[tuple[str, str]]
    ]  # definition (list of regexes)


class Notification(Message):
    """Notifies the server to add/update/remove a file for usage in fulfilling commands"""

    file: str
    remove: bool
    contents: NotRequired[str]


class Response(Message):
    """Server responses to requests and notifications"""

    cancelled: bool
    command: NotRequired[str]
    result: NotRequired[list[str | Token] | dict[str, str] | Token]


if TYPE_CHECKING:
    ResponseQueueType = GenericQueueClass[Response]
    RequestQueueType = GenericQueueClass[Request | Notification]
# Else, this is CPython < 3.12. We are now in the No Man's Land
# of Typing. In this case, avoid subscripting "GenericQueue". Ugh.
else:
    ResponseQueueType = GenericQueueClass
    RequestQueueType = GenericQueueClass
