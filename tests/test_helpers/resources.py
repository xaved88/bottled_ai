import json

from definitions import ROOT_DIR
from rs.machine.state import GameState
from rs.machine.the_bots_memory_book import TheBotsMemoryBook


def load_resource_state(state_path: str, memory_book: TheBotsMemoryBook = None) -> GameState:
    if memory_book is None:
        memory_book = TheBotsMemoryBook.new_default()
    f = open(f"{ROOT_DIR}/tests/res/{state_path}", "r")
    state = f.read()
    f.close()
    return GameState(json.loads(state), memory_book)
