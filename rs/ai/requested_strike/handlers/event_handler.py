from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class EventHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState) -> List[str]:
        event_name = state.game_state()['screen_state']['event_name']

        ## Any custom logic for each event name would go here ##
        # if event_name == "Purifier":
        #    return ["choose 1", "choose 0"] # avoids purifying and then closes screen

        return ["choose 0"]
