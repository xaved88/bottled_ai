from typing import List

from config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

cards_to_discard = [

    'strike',
    'strike+',
    'defend',
    'defend+',
    'ascender\'s bane',
    'clumsy',
    'curse of the bell',
    'decay',
    'doubt',
    'injury',
    'necronomicurse',
    'normality',
    'pain',
    'parasite',
    'pride',
    'regret',
    'shame',
    'writhe',
    'burn',
    'burn+'
    'dazed',
    'wound',
    'slimed',
]


class DiscardHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        if state.screen_type() == ScreenType.HAND_SELECT.value \
                and state.game_state()["screen_state"]["can_pick_zero"]:
            return True

    def handle(self, state: GameState) -> List[str]:

        if not state.has_command(Command.CHOOSE):  # For case that we chose to discard all cards.
            return ['confirm']

        choice_list = state.get_choice_list()

        for checked_card in choice_list:
            if checked_card in cards_to_discard:
                if presentation_mode:
                    return [p_delay, 'choose ' + checked_card]
                return ['choose ' + checked_card]

        if presentation_mode:
            return [p_delay, 'confirm']
        return ['confirm']
