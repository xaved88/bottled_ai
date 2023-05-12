from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

cards_to_skip_girya_for_upgrading = [
        'Accuracy',
]


class CampfireHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.REST.value

    def handle(self, state: GameState) -> List[str]:

        choice = "smith"

        if state.has_relic("Girya") \
                and 'lift' in state.get_choice_list() \
                and state.get_player_health_percentage() > 0.6 \
                and state.get_relic_counter("Girya") < 2 \
                and not (
                state.deck.contains_cards(cards_to_skip_girya_for_upgrading) and 'smith' in state.get_choice_list()):
            choice = "lift"

        # heal or default
        if 'smith' not in state.get_choice_list() \
                or state.get_player_health_percentage() <= 0.6 \
                or state.floor() == 49:
            choice = "0"  # 0 is rest if it's available, just whatever if not

        if state.has_relic("Pantograph") \
                and 'smith' in state.get_choice_list() \
                and (state.floor() == 15 or state.floor() == 32) \
                and state.get_player_health_percentage() >= 0.4:
            choice = "smith"

        if presentation_mode:
            return [p_delay, "choose " + choice, p_delay]
        return ["choose " + choice]
