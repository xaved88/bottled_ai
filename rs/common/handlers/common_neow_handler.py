from typing import List

from presentation_config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

# We don't cover choice 2, which is an option constructed out of a buff AND a debuff. 3 is always relic swap.
default_desired_choices = [
    'obtain a random common relic',
    'upgrade a card',
    'obtain 100 gold',
    'choose a card to obtain',
    'enemies in your next three combats have 1 hp',
    'remove a card from your deck',
    'obtain 3 random potions',
    'max hp +8',
    'transform a card',
    'lose your starting relic obtain a random boss relic',
    'obtain a random rare card',
    'choose a colorless card to obtain',
]


class CommonNeowHandler(Handler):

    def __init__(self, desired_choices: List[str] = None):
        self.desired_choices: List[str] = default_desired_choices if desired_choices is None else desired_choices

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value \
               and state.has_command(Command.CHOOSE) \
               and state.game_state()['screen_state']['event_id'] == "Neow Event"

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        if "leave" in state.get_choice_list():
            if presentation_mode:
                return HandlerAction(commands=[p_delay_s, "choose 0"])
            return HandlerAction(commands=["choose 0"])

        choice_list = state.get_choice_list()

        for choice in self.desired_choices:
            if choice in choice_list:
                if presentation_mode:
                    return HandlerAction(commands=[p_delay, "choose " + choice, "wait 30"])
                return HandlerAction(commands=["choose " + choice, "wait 30"])
