from typing import List

from config import presentation_mode, p_delay_s
from rs.game.card import CardType
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class ChestHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CHEST.value \
               and state.game_state()['room_type'] == "TreasureRoom"

    def handle(self, state: GameState) -> List[str]:
        if state.has_relic("Cursed Key"):
            return ["proceed"]
        if presentation_mode:
            return [p_delay_s, "choose 0", "wait 30"]
        return ["choose 0", "wait 30"]
