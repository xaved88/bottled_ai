from typing import List

from rs.calculator.comparator import SbcComparator
from rs.calculator.game_state_converter import create_hand_state
from rs.calculator.hand_state import PLAY_DISCARD
from rs.calculator.helper import pickle_deepcopy
from rs.calculator.play_path import PlayPath, get_paths
from rs.machine.state import GameState


def get_best_battle_path(game_state: GameState, comparator: SbcComparator) -> PlayPath:
    original_state = create_hand_state(game_state)
    paths = {}
    get_paths(PlayPath([], pickle_deepcopy(original_state)), paths)

    best_path = None
    for path in paths.values():
        path.state.end_turn()
        if best_path is None:
            best_path = path
        else:
            if comparator.does_challenger_defeat_the_best(best_path.state, path.state, original_state):
                best_path = path

    return best_path


def get_best_battle_action(game_state: GameState, comparator: SbcComparator) -> List[str]:
    path = get_best_battle_path(game_state, comparator)

    if path.plays:
        next_move = path.plays[0]
        if next_move[1] == -1:
            return [f"play {next_move[0] + 1}"]
        if next_move[1] == PLAY_DISCARD:
            return [f"choose {next_move[0]}"]
        return [f"play {next_move[0] + 1} {next_move[1]}"]
    return []
