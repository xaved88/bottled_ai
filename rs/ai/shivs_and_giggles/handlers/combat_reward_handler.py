from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

throw_away_potions = [
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
        # Check if we've got a potion we don't like, and toss it out
        for idx, pot in enumerate(state.get_potions()):
            if pot['id'] in throw_away_potions:
                if presentation_mode:
                    return [p_delay, "potion discard " + str(idx), p_delay_s]
                return ["wait 30", "potion discard " + str(idx)]

        # If a potion is waiting for us, but we're full, toss out the first one
        if state.get_choice_list()[0] == "potion" and state.are_potions_full():
            if presentation_mode:
                return [p_delay, "potion discard 0", p_delay_s]
            return ["potion discard 0"]
        return []
