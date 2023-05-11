from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

undesired_relics = [
    'Dead Branch',
    'Bottled Flame',
]

# most important on top
desired_potions = [
    'fairy in a bottle',
    'fruit juice',
    'cultist potion',
    'power potion',
    'duplication potion',
    'distilled chaos',
    'blessing of the forge',
    'attack potion',
    'dexterity potion',
    'regen potion',
    'energy potion',
    'entropic brew',
    'heart of iron',
    'essence of steel',
    'fear potion',
    'fire potion',
    'liquid bronze',
    'skill potion',
    'strength potion',
    'ancient potion',
    'blood potion',
    'weak potion',
    'poison potion',
    'swift potion',
    'colorless potion',
    'flex potion',
    'gambler\u0027s brew',
    'speed potion',
    'block potion',
    'explosive potion',
    'cunning potion',
    'ghost in a jar',
    'smoke bomb',
    'elixir potion',
    'liquid memories',
    'snecko oil',
]
desired_potions.reverse()


class CombatRewardHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.COMBAT_REWARD.value

    def handle(self, state: GameState) -> List[str]:

        all_available_potions = []
        # Chug a Fruit Juice straight away
        for idx, pot in enumerate(state.get_potions_by_name()):
            if pot == 'fruit juice':
                if presentation_mode:
                    return [p_delay, "potion use " + str(idx), p_delay_s]
                return ["wait 30", "potion use " + str(idx)]

        # Do pickups
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

        elif 'potion' in state.get_choice_list():
            if state.are_potions_full():
                for least_desired_potion in desired_potions:
                    if least_desired_potion not in state.get_all_available_potions_by_name():
                        continue
                    if least_desired_potion in state.get_reward_potions_by_name():
                        break
                    for idx, pot in enumerate(state.get_potions_by_name()):
                        if pot == least_desired_potion:
                            return ["wait 30", "potion discard " + str(idx)]

                    # edge-case:
                    # full potions + two waiting potions: one strongly desired (more than our inventory potions), and one not desired (less than our inventory potions)
                    # in this case we will simply ignore the potions instead of juggling to pick up the strongly desired potion

            else:
                choice = 'potion'

        elif 'card' in state.get_choice_list():
            choice = 'card'

        if choice != 'did not choose':
            if presentation_mode:
                return [p_delay, "choose " + choice, p_delay_s]
            return ["choose " + choice]

        return ["proceed"]
