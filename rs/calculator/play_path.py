from typing import List

from rs.calculator.battle_state import BattleState, Play
from rs.calculator.helper import pickle_deepcopy


class PlayPath:
    def __init__(self, plays: List[Play], state: BattleState):
        self.plays: List[Play] = plays
        self.state: BattleState = state

    def end_turn(self):
        self.state.end_turn()


def get_paths(path: PlayPath, paths: dict[str, PlayPath]):
    path_state = path.state.get_state_hash()
    if path_state in paths:
        return
    paths[path_state] = path
    # resolve any open discards
    if path.state.amount_to_discard:
        plays = path.state.get_discards()
    else:
        plays = path.state.get_plays()
    for play in plays:
        new_state: BattleState = pickle_deepcopy(path.state)
        new_state.transform_from_play(play, is_first_play=not path.plays)
        new_plays: List[Play] = path.plays.copy()
        new_plays.append(play)
        new_path: PlayPath = PlayPath(new_plays, new_state)
        get_paths(new_path, paths)


def get_paths_bfs(state: BattleState, max_path_count: int):
    explored_paths: dict[str, PlayPath] = {}
    unexplored_paths = [PlayPath([], pickle_deepcopy(state))]

    while len(explored_paths) < max_path_count:
        # as long as there are unexplored paths, keep progressing
        if len(unexplored_paths) == 0:
            break
        path = unexplored_paths.pop()

        # if we've already seen something similar, don't continue with this path
        path_state = path.state.get_state_hash()
        if path_state in explored_paths:
            continue
        # otherwise keep it
        explored_paths[path_state] = path

        # and then queue up all the next states that could happen
        if path.state.amount_to_discard:
            plays = path.state.get_discards()
        else:
            plays = path.state.get_plays()

        for play in plays:
            new_state: BattleState = pickle_deepcopy(path.state)
            new_state.transform_from_play(play, is_first_play=not path.plays)
            new_plays: List[Play] = path.plays.copy()
            new_plays.append(play)
            unexplored_paths.append(PlayPath(new_plays, new_state))

    return explored_paths
