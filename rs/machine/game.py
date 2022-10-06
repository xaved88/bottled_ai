import json
from typing import List, Optional

from rs.api.client import Client
from rs.helper.controller import await_controller
from rs.helper.general import can_handle_screenshots
from rs.helper.logger import init_run_logging, log_to_run, log_snapshot
from rs.helper.seed import get_seed_string
from rs.machine.default_game_over import DefaultGameOverHandler
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
        self.last_state: Optional[GameState] = None
        self.game_over_handler: DefaultGameOverHandler = DefaultGameOverHandler()

    def start(self, seed: str = "", take_snapshots: bool = False):
        self.run_elites = []
        self.last_elite = ""
        self.run_bosses = []
        self.last_boss = ""
        self.take_snapshots = take_snapshots and can_handle_screenshots()

        start_message = "start Ironclad"
        if seed:
            start_message += " 0 " + seed
        self.__send_command(start_message)
        state_seed = get_seed_string(self.last_state.game_state()['seed'])
        init_run_logging(state_seed)
        self.__send_command("choose 0")

    def run(self):
        log_to_run("Starting Run")
        while self.last_state.is_game_running():  # todo -> bring this out to an actual end condition
            await_controller()
            self.__handle_state_based_logging()
            handled = False
            # Handle Game Over
            if self.game_over_handler.can_handle(self.last_state):
                commands = self.game_over_handler.handle(self.last_state, self.run_elites, self.run_bosses)
                for command in commands:
                    self.__send_command(command)
                break
            # All other behaviours
            for handler in self.handlers:
                if handler.can_handle(self.last_state):
                    log_to_run("Handler: " + str(handler))
                    commands = handler.handle(self.last_state)
                    if not commands:
                        continue
                    for command in commands:
                        self.__send_command(command)
                        # self.__send_command("wait 30")  # for slowing things down so you can see what's going on!
                    handled = True
                    break
            if not handled:
                log_to_run("Dying from not knowing what to do next")
                raise Exception("ah I didn't know what to do!")

    def __send_command(self, command: str):
        if self.take_snapshots and self.last_state and 'game_state' in self.last_state.json and 'floor' in self.last_state.game_state():
            log_snapshot(self.last_state.floor(), command)

        self.last_state = GameState(json.loads(self.client.send_message(command)))

    def __handle_state_based_logging(self):
        monsters = self.last_state.get_monsters()
        if self.last_state.game_state()['room_type'] == 'MonsterRoomElite':
            if monsters:
                self.last_elite = monsters[0]['name']
            elif self.last_elite:
                self.run_elites.append(self.last_elite)
                self.last_elite = ""
        if self.last_state.game_state()['room_type'] == 'MonsterRoomBoss':
            if monsters:
                self.last_boss = monsters[0]['name']
            elif self.last_boss:
                self.run_bosses.append(self.last_boss)
                self.last_boss = ""
