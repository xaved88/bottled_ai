from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

# We don't cover choice 2, which is an option constructed out of a buff AND a debuff. 3 is always relic swap.
desired_choices = [
    'upgrade a card',
    'obtain a random common relic',
    'obtain 100 gold',
    'choose a card to obtain',
    'obtain 3 random potions',
    'choose a colorless card to obtain',
    'max hp +8',
    'obtain a random rare card',
    'enemies in your next three combats have 1 hp',
    'remove a card from your deck',
    'transform a card',
    'lose your starting relic obtain a random boss relic',
]


class NeowHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value \
               and state.has_command(Command.CHOOSE) \
               and state.game_state()['screen_state']['event_id'] == "Neow Event"

    def handle(self, state: GameState) -> List[str]:
        if "leave" in state.get_choice_list():
            return ["choose 0"]

        choice_list = state.game_state()["choice_list"]

        for choice in desired_choices:
            if choice in choice_list:
                return ["choose " + choice, "wait 30"]
