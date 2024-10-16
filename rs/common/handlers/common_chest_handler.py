from typing import List

from presentation_config import presentation_mode, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonChestHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CHEST.value \
               and state.game_state()['room_type'] == "TreasureRoom"

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        if state.has_relic("Cursed Key") and state.get_relic_counter("Omamori") >= 1:
            return HandlerAction(commands=["choose 0", "wait 30"])
        if state.has_relic("Cursed Key") and state.deck.contains_curses_of_any_kind():
            return HandlerAction(commands=["proceed"])
        if presentation_mode:
            return HandlerAction(commands=[p_delay_s, "choose 0", "wait 30"])
        return HandlerAction(commands=["choose 0", "wait 30"])
