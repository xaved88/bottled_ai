from typing import List

from config import presentation_mode, p_delay
from rs.ai.shivs_and_giggles.handlers.shop_purchase_handler import standard_cards_to_purge
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonCampfireHandler(Handler):

    def __init__(self, high_priority_upgrades: List[str] = None):
        self.high_priority_upgrades: List[str] = [] if high_priority_upgrades is None else high_priority_upgrades

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.REST.value

    def handle(self, state: GameState) -> HandlerAction:
        can_rest = 'rest' in state.get_choice_list()
        can_toke = 'toke' in state.get_choice_list()
        can_lift = 'lift' in state.get_choice_list()
        can_dig = 'dig' in state.get_choice_list()
        can_smith = 'smith' in state.get_choice_list()

        worth_healing = state.get_player_health_percentage() <= 0.6
        pantograph_will_cover_it = state.has_relic("Pantograph") \
                                   and (state.floor() == 15 or state.floor() == 32) \
                                   and state.get_player_health_percentage() >= 0.4
        important_upgrade_available = state.deck.contains_cards(self.high_priority_upgrades) and can_smith

        choice = "0"

        if can_rest and ((worth_healing and not pantograph_will_cover_it) or state.floor() == 49):
            choice = "rest"
        elif can_toke and state.deck.contains_curses():
            choice = "toke"
        elif can_lift and not important_upgrade_available and state.get_relic_counter("Girya") < 2:
            choice = "lift"
        elif can_dig and not important_upgrade_available:
            choice = "dig"
        elif can_smith:
            choice = 'smith'
        elif can_toke and state.deck.contains_cards(standard_cards_to_purge):
            choice = "toke"

        if presentation_mode:
            return HandlerAction(commands=[p_delay, "choose " + choice, p_delay])
        return HandlerAction(commands=["choose " + choice])
