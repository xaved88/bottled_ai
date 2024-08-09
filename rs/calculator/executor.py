from typing import List, Optional

from rs.calculator.battle_state import PLAY_DISCARD, Play, PLAY_EXHAUST
from rs.calculator.game_state_converter import create_battle_state
from rs.calculator.interfaces.comparator_interface import ComparatorInterface
from rs.calculator.play_path import PlayPath, get_paths_bfs
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState
from rs.machine.the_bots_memory_book import TheBotsMemoryBook


def get_best_battle_path(game_state: GameState, comparator: ComparatorInterface, max_path_count) -> PlayPath:
    original_state = create_battle_state(game_state)
    paths = get_paths_bfs(original_state, max_path_count)
    best_path = None
    for path in paths.values():
        path.state.end_turn()
        if best_path is None:
            best_path = path
        else:
            if comparator.does_challenger_defeat_the_best(best_path.state, path.state, original_state):
                best_path = path

    return best_path


def get_best_battle_action(game_state: GameState, comparator: ComparatorInterface, max_path_count: int = 11_000) -> \
        Optional[HandlerAction]:
    path = get_best_battle_path(game_state, comparator, max_path_count)

    if path and path.plays:
        next_move = path.plays[0]

        # create a temp state for finding the state of the custom state after the chosen action
        state = create_battle_state(game_state)
        state.transform_from_play(next_move, is_first_play=False)  # not sure if it's ok that I'm setting that false
        memory_book = TheBotsMemoryBook(memory_by_card=state.memory_by_card.copy(), memory_general=state.memory_general.copy())

        if next_move[1] == -1:
            return HandlerAction(commands=[f"play {next_move[0] + 1}"], memory_book=memory_book)
        if next_move[1] == PLAY_DISCARD:
            return HandlerAction(commands=get_discard_commands(path.plays), memory_book=memory_book)
        if next_move[1] == PLAY_EXHAUST:
            return HandlerAction(commands=get_exhaust_commands(path.plays), memory_book=memory_book)
        return HandlerAction(commands=[f"play {next_move[0] + 1} {next_move[1]}"], memory_book=memory_book)
    return None


def get_discard_commands(plays: List[Play]) -> List[str]:
    raw_indexes = []
    for (card_idx, play_type) in plays:
        if play_type == PLAY_DISCARD:
            raw_indexes.append(card_idx)
        else:
            break
    raw_indexes.reverse()
    adjusted_indexes = []
    for (i, idx) in enumerate(raw_indexes):
        for j in range(i + 1, len(raw_indexes)):
            if raw_indexes[j] <= idx:
                idx += 1
        adjusted_indexes.append(idx)
    adjusted_indexes.reverse()

    return [f"choose {idx}" for idx in adjusted_indexes] + ["confirm", "wait 30"]


def get_exhaust_commands(plays: List[Play]) -> List[str]:
    raw_indexes = []
    for (card_idx, play_type) in plays:
        if play_type == PLAY_EXHAUST:
            raw_indexes.append(card_idx)
        else:
            break
    raw_indexes.reverse()
    adjusted_indexes = []
    for (i, idx) in enumerate(raw_indexes):
        for j in range(i + 1, len(raw_indexes)):
            if raw_indexes[j] <= idx:
                idx += 1
        adjusted_indexes.append(idx)
    adjusted_indexes.reverse()

    return [f"choose {idx}" for idx in adjusted_indexes] + ["confirm", "wait 30"]
