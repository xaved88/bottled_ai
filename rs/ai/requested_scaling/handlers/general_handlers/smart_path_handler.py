from typing import List

from config import presentation_mode, p_delay, slow_pathing
from rs.game.map import Map
from rs.game.screen_type import ScreenType
from rs.helper.logger import log
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartPathHandler(Handler):

    # maybe configure some preferences here
    def __init__(self):
        pass

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.MAP.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState) -> List[str]:
        # Get the math and paths set up
        n = state.game_state()["screen_state"]["current_node"]
        current_position = str(n["x"]) + "_" + str(n["y"])
        game_map = Map(state.get_map(), current_position, state.game_state()['floor'])

        # Sort the paths by our priorities
        game_map.sort_paths_by_reward_to_survivability(state)

        """
        log("---------------", "path_analysis")
        log("FLOOR: " + str(state.floor()), "path_analysis")
        smart_path = [room.type.value for room in game_map.paths[-1].rooms]
        log("Smart Path: [" + ", ".join(smart_path) + "]", "path_analysis")
        log("Smart Path reward: " + str(game_map.paths[-1].reward) + ", survivability: " +  str(game_map.paths[-1].survivability), "path_analysis")
        #"""

        # this will actually screw us with winged boots, as there are more choices and we'd be picking from a different list...
        if presentation_mode or slow_pathing:
            return [p_delay, "choose " + str(game_map.get_path_choice_from_choices(state.get_choice_list()))]
        return ["choose " + str(game_map.get_path_choice_from_choices(state.get_choice_list()))]
