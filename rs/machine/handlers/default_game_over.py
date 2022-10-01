from typing import List

from rs.game.screen_type import ScreenType
from rs.helper.logger import log_run_results
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class DefaultGameOverHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.GAME_OVER.value \
               and (state.has_command(Command.CONFIRM) or state.has_command(Command.PROCEED))

    def handle(self, state: GameState) -> List[str]:
        log_run_results(state)
        return ["proceed"]
