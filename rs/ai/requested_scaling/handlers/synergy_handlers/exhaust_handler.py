from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.current_action import CurrentAction
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

#  Didn't find a quick and easy way of handling the curses/statuses without a list. Also, intentionally left out 'void'.
cards_to_exhaust = [
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
    'strike',
    'strike+',
    'defend',
    'defend+',
]


class ExhaustHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        screen_type = state.screen_type()
        action = state.current_action()

        if state.screen_type() == ScreenType.HAND_SELECT.value and \
                state.current_action() == CurrentAction.EXHAUSTACTION.value:
            return True

    def handle(self, state: GameState) -> List[str]:

        if not state.has_command(Command.CHOOSE):  # For case that we chose to discard all cards.
            return ['confirm']

        choice_list = state.get_choice_list()

        for checked_card in choice_list:
            if checked_card in cards_to_exhaust:
                if presentation_mode:
                    return [p_delay, 'choose ' + checked_card]

                return ['choose ' + checked_card]
            else:
                pass
        
        """For now, if no valid card is able to be exhausted, just exhaust the firs card"""
        for checked_card in choice_list:
            return ['choose ' + checked_card]
        
        
        if presentation_mode:
            return [p_delay, 'confirm']
        return ['confirm']
