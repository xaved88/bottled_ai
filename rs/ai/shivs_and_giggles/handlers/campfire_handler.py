from typing import List

from config import presentation_mode, p_delay
from rs.ai.shivs_and_giggles.handlers.shop_purchase_handler import standard_cards_to_purge
from rs.game.card import CardType
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

high_prio_upgrades = [
    'Accuracy',
]


class CampfireHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.REST.value

    def handle(self, state: GameState) -> List[str]:

        if 'rest' in state.get_choice_list() \
                and (state.get_player_health_percentage() <= 0.6 and not pantograph_will_cover_it(state)) \
                or state.floor() == 49:
            choice = "rest"

        elif 'toke' in state.get_choice_list() \
                and state.deck.contains_type(CardType.CURSE):
            choice = "toke"

        elif 'lift' in state.get_choice_list() \
                and state.get_relic_counter("Girya") < 2 \
                and not (state.deck.contains_cards(high_prio_upgrades) and 'smith' in state.get_choice_list()):
            choice = "lift"

        elif 'dig' in state.get_choice_list() \
                and not (state.deck.contains_cards(high_prio_upgrades) and 'smith' in state.get_choice_list()):
            choice = "dig"

        elif 'smith' in state.get_choice_list():
            choice = 'smith'

        elif 'toke' in state.get_choice_list() \
                and 'smith' not in state.get_choice_list() \
                and state.deck.contains_cards(standard_cards_to_purge):
            choice = "toke"

        else:
            choice = "0"

        if presentation_mode:
            return [p_delay, "choose " + choice, p_delay]
        return ["choose " + choice]


def pantograph_will_cover_it(state: GameState) -> bool:
    if state.has_relic("Pantograph") \
            and (state.floor() == 15 or state.floor() == 32) \
            and state.get_player_health_percentage() >= 0.4:
        return True
    return False
