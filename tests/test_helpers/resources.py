import json

from definitions import ROOT_DIR
from rs.machine.custom_state import set_new_game_state, set_new_turn_state, set_new_battle_state, CustomState
from rs.machine.state import GameState


def load_resource_state(state_path: str) -> GameState:
    set_new_game_state()
    f = open(f"{ROOT_DIR}/tests/res/{state_path}", "r")
    state = f.read()
    f.close()
    return GameState(json.loads(state))
