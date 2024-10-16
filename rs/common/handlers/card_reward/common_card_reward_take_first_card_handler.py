from typing import List

from presentation_config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


# This handler will always just take the first card offered - useful for messing around with lots of cards
class CommonCardRewardTakeFirstCardHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT" or
                    state.game_state()["room_phase"] == "COMBAT")

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        return HandlerAction(commands=["choose 0", "wait 30"])
