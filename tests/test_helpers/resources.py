import json

from definitions import ROOT_DIR
from rs.machine.state import GameState


def load_resource_state(state_path: str) -> GameState:
    f = open(f"{ROOT_DIR}/tests/res/{state_path}", "r")
    state = f.read()
    f.close()
    return GameState(json.loads(state))
