import copy
import hashlib
from typing import List

from rs.calculator.hand_state import HandState, Play


class PlayPath:
    def __init__(self, plays: List[Play], state: HandState):
        self.plays: List[Play] = plays
        self.state: HandState = state

    def end_turn(self):
        self.state.end_turn()


def get_paths(path: PlayPath) -> List[PlayPath]:
    possibilities: List[PlayPath] = [path]
    for play in path.state.get_plays():
        new_state: HandState = copy.deepcopy(path.state)
        new_state.transform_from_play(play)
        new_plays: List[Play] = path.plays.copy()
        new_plays.append(play)
        new_path: PlayPath = PlayPath(new_plays, new_state)
        possibilities += get_paths(new_path)
    return possibilities


"""
The idea here:
- switch to a map or something where we can have control and reference throughout the stack
- come up with some sort of "meaningful state" export in the hand state
- have that go to some simple hash for comparison
- if you've already had something at that hash, don't continue path traversal.

- also, may be worth it to come up with our own copy method?
"""


def get_paths_performant(path: PlayPath, paths: dict[str, PlayPath]):
    hash = path.state.get_state_hash()
    if hash in paths:
        return
    paths[hash] = path
    for play in path.state.get_plays():
        new_state: HandState = copy.deepcopy(path.state)
        new_state.transform_from_play(play)
        new_plays: List[Play] = path.plays.copy()
        new_plays.append(play)
        new_path: PlayPath = PlayPath(new_plays, new_state)
        get_paths_performant(new_path, paths)
