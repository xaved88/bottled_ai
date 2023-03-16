from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CampfireHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) and state.screen_type() == ScreenType.REST.value

    def handle(self, state: GameState) -> List[str]:
        if state.has_relic("Pantograph") \
                and 'smith' in state.get_choice_list() \
                and (state.floor() == 15 or state.floor() == 32) \
                and state.get_player_health_percentage() >= 0.4:
            if presentation_mode:
                return [p_delay, "choose " + str(state.get_choice_list().index('smith')), p_delay]
            return ["choose " + str(state.get_choice_list().index('smith'))]

        if 'smith' not in state.get_choice_list() \
                or state.get_player_health_percentage() <= 0.6 \
                or state.floor() == 49:
            if presentation_mode:
                return [p_delay, "choose 0", p_delay_s]
            return ["choose 0"]  # 0 is rest if it's available, just whatever if not

        if presentation_mode:
            return [p_delay, "choose " + str(state.get_choice_list().index('smith')), p_delay]
        return ["choose " + str(state.get_choice_list().index('smith'))]
