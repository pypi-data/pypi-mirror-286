from logging import Logger
from multiprocessing.queues import Queue as GenericClassQueue
from time import sleep

from pyeditorconfig import get_config
from token_tools import Token, normal_text_range

from .misc import (
    COMMANDS,
    Notification,
    Request,
    RequestQueueType,
    Response,
    ResponseQueueType,
)
from .server_functions import (
    find_autocompletions,
    get_definition,
    get_highlights,
    get_replacements,
    get_special_tokens,
)


class Server:
    """Handles input from the user and returns output from special functions. Not an external API."""

    def __init__(
        self,
        response_queue: GenericClassQueue,
        requests_queue: GenericClassQueue,
        logger: Logger,
    ) -> None:
        self.logger: Logger = logger
        self.logger.info("Starting server setup")
        self.response_queue: ResponseQueueType = response_queue
        self.requests_queue: RequestQueueType = requests_queue
        self.all_ids: list[int] = []
        self.newest_ids: dict[str, int] = {}
        self.newest_requests: dict[str, Request | None] = {}
        for command in COMMANDS:
            self.newest_ids[command] = 0
            self.newest_requests[command] = None

        self.files: dict[str, str] = {}

        self.logger.info("Server setup complete")

        while True:
            self.run_tasks()
            sleep(0.0025)

    def simple_id_response(self, id: int, cancelled: bool = True) -> None:
        self.logger.debug(f"Creating simple response for id {id}")
        response: Response = {
            "id": id,
            "type": "response",
            "cancelled": cancelled,
        }
        self.logger.debug(f"Sending simple response for id {id}")
        self.response_queue.put(response)
        self.logger.info(f"Simple response for id {id} sent")

    def parse_line(self, message: Request | Notification) -> None:
        self.logger.debug("Parsing Message from user")
        id: int = message["id"]
        match message["type"]:
            case "notification":
                self.logger.debug("Mesage is of type notification")
                file: str = message["file"]  # type: ignore
                if message["remove"]:  # type: ignore
                    self.logger.info(f"File {file} was requested for removal")
                    self.files.pop(file)
                    self.logger.info(f"File {file} has been removed")
                    return
                contents: str = message["contents"]  # type: ignore
                self.files[file] = contents
                self.logger.info(
                    f"File {file} has been updated with new contents"
                )
                self.simple_id_response(id, False)
                self.logger.debug(
                    f"Notification response for id {id} has been sent"
                )
            case "request":
                self.logger.info(f"Mesage with id {id} is of type request")
                self.all_ids.append(id)
                command: str = message["command"]  # type: ignore
                self.newest_ids[command] = id
                self.newest_requests[command] = message  # type: ignore
                self.logger.debug("Request stored for parsing")
            case _:
                self.logger.warning(
                    f"Unknown type {type}. Sending simple response"
                )
                self.simple_id_response(id)
                self.logger.debug(f"Simple response for id {id} sent")

    def cancel_all_ids_except_newest(self) -> None:
        self.logger.info("Cancelling all old id's")
        ids = [
            id["id"]
            for id in list(self.newest_requests.values())
            if id is not None
        ]
        for id in self.all_ids:
            if id in ids:
                self.logger.debug(f"Id {id} is newest of its command")
                continue
            self.logger.debug(
                f"Id {id} is an old request, sending simple respone"
            )
            self.simple_id_response(id)

        self.all_ids = []
        self.logger.debug("All ids list reset")

    def handle_request(self, request: Request) -> None:
        command: str = request["command"]
        id: int = self.newest_ids[command]
        file: str = request["file"]
        result: list[str | Token] | dict[str, str] = []
        cancelled: bool = False

        match request["command"]:
            case "autocomplete":
                self.logger.info("Finding completions for request")
                result = find_autocompletions(
                    full_text=self.files[file],
                    expected_keywords=request["expected_keywords"],  # type: ignore
                    current_word=request["current_word"],  # type: ignore
                )
            case "replacements":
                self.logger.info("Getting replacements for request")
                result = get_replacements(
                    full_text=self.files[file],
                    expected_keywords=request["expected_keywords"],  # type: ignore
                    replaceable_word=request["current_word"],  # type: ignore
                )
            case "highlight":
                self.logger.info("Getting normal highlights for request")
                pre_refined_result: list[Token] = get_highlights(
                    full_text=self.files[file],
                    language=request["language"],  # type: ignore
                    text_range=request["text_range"],  # type: ignore
                )
                result.extend([token for token in pre_refined_result])
            case "editorconfig":
                self.logger.info("Getting editorconfig info for request")
                result = get_config(request["file_path"])  # type: ignore
            case "definition":
                self.logger.info("Getting definition for request")
                result = get_definition(
                    self.files[file],
                    request["definition_starters"],  # type: ignore
                    request["current_word"],  # type: ignore
                )
            case "links_and_chars":
                self.logger.info("Searching for Links and chars")
                result = get_special_tokens(
                    self.files[file],
                    normal_text_range(self.files[file], request["text_range"])[  # type: ignore
                        1
                    ],
                )
            case _:
                self.logger.warning(f"Command {command} not recognized")
                cancelled = True

        response: Response = {
            "id": id,
            "type": "response",
            "cancelled": cancelled,
            "command": command,
            "result": result,
        }
        self.logger.debug("Response created")
        self.response_queue.put(response)
        self.newest_ids[command] = 0
        self.logger.info(f"Response sent for request of command {command}")

    def run_tasks(self) -> None:
        if self.requests_queue.empty():
            return

        self.logger.debug("New request in queue")
        while not self.requests_queue.empty():
            self.logger.debug("Parsing request")
            self.parse_line(self.requests_queue.get())

        if not self.all_ids:
            self.logger.debug("All requests were notifications")

        self.logger.debug("Cancelling all old id's")
        self.cancel_all_ids_except_newest()

        # Actual work
        for request in list(self.newest_requests.values()):
            if request is None:
                continue
            command: str = request["command"]
            self.logger.info(f"Handling request of command {command}")
            self.handle_request(request)
            self.newest_requests[command] = None
            self.logger.debug("Request completed")
