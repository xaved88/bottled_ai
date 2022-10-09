import copy
from typing import List

from rs.calculator.hand_state import HandState, Play


class PlayPath:
    def __init__(self, plays: List[Play], state: HandState):
        self.plays: List[Play] = plays
        self.state: HandState = state

    def end_turn(self):
        self.state.end_turn()


def get_paths(path: PlayPath) -> List[PlayPath]:
    # todo -> some sort of state.resolve/end turn thing. all the counters need to decrease, poison damage, take damage from monsters, etc.
    possibilities: List[PlayPath] = [path]
    for play in path.state.get_plays():
        new_state: HandState = copy.deepcopy(path.state)
        new_state.transform_from_play(play)
        new_plays: List[Play] = path.plays.copy()
        new_plays.append(play)
        new_path: PlayPath = PlayPath(new_plays, new_state)
        possibilities += get_paths(new_path)
    return possibilities
