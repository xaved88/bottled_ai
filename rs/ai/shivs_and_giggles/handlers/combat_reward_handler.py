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
    'SneckoOil',
    'GhostInAJar',
]

undesired_relics = [
    'Dead Branch',
    'Bottled Flame',
]


class CombatRewardHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.COMBAT_REWARD.value

    def handle(self, state: GameState) -> List[str]:

        # POTIONS
        # Chug a Fruit Juice straight away
        for idx, pot in enumerate(state.get_potions()):
            if pot['id'] == 'Fruit Juice':
                if presentation_mode:
                    return [p_delay, "potion use " + str(idx), p_delay_s]
                return ["wait 30", "potion use " + str(idx)]

        # Check if we've got a potion we don't like, and toss it out
        for idx, pot in enumerate(state.get_potions()):
            if pot['id'] in throw_away_potions:
                if presentation_mode:
                    return [p_delay, "potion discard " + str(idx), p_delay_s]
                return ["wait 30", "potion discard " + str(idx)]

        choice = 'did not choose'

        if 'gold' in state.get_choice_list():
            choice = 'gold'

        elif 'stolen_gold' in state.get_choice_list():
            choice = 'stolen_gold'

        elif 'relic' in state.get_choice_list() and state.game_state()["screen_state"]["rewards"][0]["relic"]["id"] not in undesired_relics:
            choice = 'relic'

        # potentially too fragile check for if the second relic might be desirable even though the first one isn't that I'll leave disabled for safety
        # elif state.get_choice_list().count('relic') >= 1 and \
        #         state.game_state()["screen_state"]["rewards"][1]["relic"]["id"] not in undesired_relics:
        #     choice = '1'

        elif 'potion' in state.get_choice_list() and not state.are_potions_full():
            choice = 'potion'

        elif 'card' in state.get_choice_list():
            choice = 'card'

        if choice != 'did not choose':
            if presentation_mode:
                return [p_delay, "choose " + choice, p_delay_s]
            return ["choose " + choice]

        return ["proceed"]
