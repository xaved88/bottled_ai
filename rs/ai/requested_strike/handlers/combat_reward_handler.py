from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

throw_away_potions = [
    'GamblersBrew',
    'SmokeBomb',
    'ElixirPotion',
    'LiquidMemories',
    'SneckoOil'
]


class CombatRewardHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.COMBAT_REWARD.value

    def handle(self, state: GameState) -> List[str]:
        # Check if we've got potions we don't like, and toss 'em out
        for idx, pot in enumerate(state.get_potions()):
            if pot['id'] in throw_away_potions:
                return ["wait 30", "potion discard " + str(idx)]

        # If a potion is waiting for us but we're full, toss out the first one
        if state.get_choice_list()[0] == "potion" and state.are_potions_full():
            return ["potion discard 0"]
        return []
