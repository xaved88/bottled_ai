import json
from typing import List, Optional

from rs.api.client import Client
from rs.helper.logger import init_run_logging, log_to_run
from rs.helper.seed import get_seed_string
from rs.machine.handlers.default_cancel import DefaultCancelHandler
from rs.machine.handlers.default_choose import DefaultChooseHandler
from rs.machine.handlers.default_confirm import DefaultConfirmHandler
from rs.machine.handlers.default_end import DefaultEndHandler
from rs.machine.handlers.default_leave import DefaultLeaveHandler
from rs.machine.handlers.default_play import DefaultPlayHandler
from rs.machine.handlers.default_shop import DefaultShopHandler
from rs.machine.handlers.default_wait import DefaultWaitHandler
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

DEFAULT_GAME_HANDLERS = [
    DefaultLeaveHandler(),
    DefaultShopHandler(),
    DefaultChooseHandler(),
    DefaultConfirmHandler(),
    DefaultPlayHandler(),
    DefaultEndHandler(),
    DefaultCancelHandler(),
    DefaultWaitHandler(),
]


class Game:

    def __init__(self, client: Client, ai_handlers: List[Handler]):
        self.client = client
        self.handlers = ai_handlers + DEFAULT_GAME_HANDLERS
        self.lastState: Optional[GameState] = None

    def start(self, seed: str = ""):
        start_message = "start Ironclad"
        if seed:
            start_message += " 0 " + seed
        self.__send_command(start_message)
        state_seed = get_seed_string(self.lastState.game_state()['seed'])
        init_run_logging(state_seed)
        self.__send_command("choose 0")

    def run(self):
        log_to_run("Starting Run")
        while self.lastState.is_game_running():  # todo -> bring this out to an actual end condition
            handled = False
            for handler in self.handlers:
                if handler.can_handle(self.lastState):
                    log_to_run("Handler: " + str(handler))
                    commands = handler.handle(self.lastState)
                    for command in commands:
                        self.__send_command(command)
                        # self.__send_command("wait 30")  # for slowing things down so you can see what's going on!
                    handled = True
                    break
            if not handled:
                log_to_run("Dying from not knowing what to do next")
                raise Exception("ah I didn't know what to do!")

    def __send_command(self, command: str):
        self.lastState = GameState(json.loads(self.client.send_message(command)))
