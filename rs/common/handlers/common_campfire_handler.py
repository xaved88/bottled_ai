from typing import List

from presentation_config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonCampfireHandler(Handler):

    def __init__(self, high_priority_upgrades: List[str] = None, card_removal_priorities: List[str] = None):
        self.high_priority_upgrades: List[str] = [] if high_priority_upgrades is None else high_priority_upgrades
        self.card_removal_priorities: List[str] = [] if card_removal_priorities is None else card_removal_priorities

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.REST.value

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        can_rest = 'rest' in state.get_choice_list()
        can_toke = 'toke' in state.get_choice_list()
        can_lift = 'lift' in state.get_choice_list()
        can_dig = 'dig' in state.get_choice_list()
        can_smith = 'smith' in state.get_choice_list()
        can_recall = 'recall' in state.get_choice_list()

        # pantograph
        pantograph_trigger_floors = [15, 32, 49]
        pantograph_will_cover_it = state.has_relic("Pantograph") \
                                   and state.floor() in pantograph_trigger_floors \
                                   and state.get_player_health_percentage() >= 0.4
        pantograph_will_cover_floor_49 = state.has_relic("Pantograph") \
                                         and state.get_player_health_percentage() >= 0.60

        # other
        worth_healing = state.get_player_health_percentage() <= 0.6 and not pantograph_will_cover_it
        worth_healing_floor_49 = state.floor() == 49 \
                                 and state.get_player_health_percentage() <= 0.85 \
                                 and not pantograph_will_cover_floor_49
        important_upgrade_available = state.deck.contains_cards(self.high_priority_upgrades) and can_smith
        last_recall_possibility = can_recall and state.floor() == 49 and slay_heart

        choice = "0"

        if last_recall_possibility:
            choice = "recall"
        elif can_rest and (worth_healing or worth_healing_floor_49):
            choice = "rest"
        elif can_toke and state.deck.contains_curses_we_can_remove():
            choice = "toke"
        elif can_smith and important_upgrade_available:
            choice = "smith"
        elif can_recall and slay_heart:
            choice = "recall"
        elif can_lift and state.get_relic_counter("Girya") < 2:
            choice = "lift"
        elif can_dig:
            choice = "dig"
        elif can_smith:
            choice = 'smith'
        elif can_toke and state.deck.contains_cards(self.card_removal_priorities):
            choice = "toke"

        if presentation_mode:
            return HandlerAction(commands=[p_delay, "choose " + choice, p_delay])
        return HandlerAction(commands=["choose " + choice])
