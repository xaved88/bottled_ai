from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CombatRewardHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.COMBAT_REWARD.value

    def handle(self, state: GameState) -> List[str]:
        # ONLY IF CHOOSE 0 is a potion
        if state.get_choice_list()[0] == "potion" and state.are_potions_full():
            return ["potion discard 0"]
        return []
