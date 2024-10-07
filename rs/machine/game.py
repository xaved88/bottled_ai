import json
from typing import Optional

from rs.api.client import Client
from rs.helper.controller import await_controller
from rs.helper.logger import init_run_logging, log_to_run
from rs.helper.seed import get_seed_string
from rs.machine.ai_strategy import AiStrategy
from rs.machine.default_game_over import DefaultGameOverHandler
from rs.machine.handlers.default_cancel import DefaultCancelHandler
from rs.machine.handlers.default_choose import DefaultChooseHandler
from rs.machine.handlers.default_confirm import DefaultConfirmHandler
from rs.machine.handlers.default_end import DefaultEndHandler
from rs.machine.handlers.default_leave import DefaultLeaveHandler
from rs.machine.handlers.default_play import DefaultPlayHandler
from rs.machine.handlers.default_shop import DefaultShopHandler
from rs.machine.handlers.default_wait import DefaultWaitHandler
from rs.machine.state import GameState
from rs.machine.the_bots_memory_book import TheBotsMemoryBook

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

    def __init__(self, client: Client, strategy: AiStrategy):
        self.client = client
        self.strategy = strategy
        self.the_bots_memory_book = TheBotsMemoryBook()
        self.last_state: Optional[GameState] = None
        self.game_over_handler: DefaultGameOverHandler = DefaultGameOverHandler()

    def start(self, seed: str = ""):
        self.the_bots_memory_book.set_new_game_state()
        self.run_elites = []
        self.last_elite = ""
        self.run_bosses = []
        self.last_boss = ""
        start_message = f"start {self.strategy.character.value}"
        if seed:
            start_message += " 0 " + seed
        self.__send_setup_command(start_message)
        state_seed = get_seed_string(self.last_state.game_state()['seed'])
        init_run_logging(state_seed)
        self.__send_command("choose 0")

    def run(self):
        log_to_run("Starting Run")
        while self.last_state.is_game_running():
            await_controller(self.last_state)
            self.__handle_state_based_logging()
            handled = False
            # Handle Game Over
            if self.game_over_handler.can_handle(self.last_state):
                commands = self.game_over_handler.handle(self.last_state, self.run_elites, self.run_bosses, self.strategy.name)
                for command in commands:
                    self.__send_command(command)
                break
            # All other behaviours
            for handler in self.strategy.handlers + DEFAULT_GAME_HANDLERS:
                if handler.can_handle(self.last_state):
                    log_to_run("Handler: " + str(handler))
                    action = handler.handle(self.last_state, self.strategy.slay_heart)
                    if not action:
                        continue
                    if action.memory_book is not None:
                        self.the_bots_memory_book = action.memory_book
                        log_to_run("Memory of next action: " + str(vars(self.the_bots_memory_book)))
                    for command in action.commands:
                        self.__send_command(command)
                    handled = True
                    break
            if not handled:
                log_to_run("Dying from not knowing what to do next")
                raise Exception("ah I didn't know what to do!")

    def __send_command(self, command: str):
        self.last_state = GameState(json.loads(self.client.send_message(command)), self.the_bots_memory_book)

    def __send_silent_command(self, command: str):
        self.last_state = GameState(json.loads(self.client.send_message(command, silent=True)),
                                    self.the_bots_memory_book)

    def __send_setup_command(self, command: str):
        self.last_state = GameState(json.loads(self.client.send_message(command, before_run=True)),
                                    self.the_bots_memory_book)

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
