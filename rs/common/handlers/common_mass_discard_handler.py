from presentation_config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

#  Didn't find a quick and easy way of handling the curses/statuses without a list. Also, intentionally left out 'void'.
cards_to_mass_discard = [
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


class CommonMassDiscardHandler(Handler):
    # Handles mass-discard cases like Gambler's Potion and Gambling Chip

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.HAND_SELECT.value \
               and state.game_state()["screen_state"]["can_pick_zero"]

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:

        if not state.has_command(Command.CHOOSE):  # For case that we chose to discard all cards.
            return HandlerAction(commands=['confirm'])

        choice_list = state.get_choice_list()

        for checked_card in choice_list:
            if checked_card in cards_to_mass_discard:
                if presentation_mode:
                    return HandlerAction(commands=[p_delay, 'choose ' + checked_card])
                return HandlerAction(commands=['choose ' + checked_card])

        if presentation_mode:
            return HandlerAction(commands=[p_delay, 'confirm'])
        return HandlerAction(commands=['confirm'])
