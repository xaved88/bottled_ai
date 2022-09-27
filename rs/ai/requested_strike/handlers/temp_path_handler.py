from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


# Just for doing random things that we want at specific places
class TempPathHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.MAP and state.floor() == 0

    def handle(self, state: GameState) -> List[str]:
        return ["choose 1"]
