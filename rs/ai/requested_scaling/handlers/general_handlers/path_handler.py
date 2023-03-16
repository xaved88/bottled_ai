from typing import List

from rs.game.map import Map
from rs.game.screen_type import ScreenType
from rs.helper.logger import log, log_to_run
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

#Deprecated - we're consistently using the smart path handler instead
class PathHandler(Handler):

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

        # Sort the paths by our priorities (note that the highest priority = the last sort, in this case)
        game_map.sort_paths_by_questions_and_shops()
        game_map.sort_paths_by_campfires()
        game_map.sort_paths_by_elites()

        return ["choose " + str(game_map.get_path_choice_from_choices(state.get_choice_list()))]
