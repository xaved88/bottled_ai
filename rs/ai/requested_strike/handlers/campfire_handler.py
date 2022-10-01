from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CampfireHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.REST.value

    def handle(self, state: GameState) -> List[str]:
        if 'smith' not in state.get_choice_list() \
                or state.get_player_health_percentage() <= 0.6 \
                or state.floor() == 49:
            return ["choose 0"]  # 0 is rest if it's available, just whatever if not

        return ["choose " + str(state.get_choice_list().index('smith'))]
