import json

from definitions import ROOT_DIR
from rs.machine.state import GameState
from rs.machine.the_bots_memory_book import TheBotsMemoryBook


def load_resource_state(state_path: str, set_new_game: bool = True, memory_book: TheBotsMemoryBook = None) -> GameState:
    if memory_book is None:
        memory_book = TheBotsMemoryBook()
        memory_book.set_new_game_state()
    f = open(f"{ROOT_DIR}/tests/res/{state_path}", "r")
    state = f.read()
    f.close()
    return GameState(json.loads(state), memory_book)
