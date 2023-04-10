from typing import List

from rs.calculator.comparator import SbcComparator
from rs.calculator.game_state_converter import create_hand_state
from rs.calculator.hand_state import PLAY_DISCARD, Play
from rs.calculator.play_path import PlayPath, get_paths_bfs
from rs.machine.state import GameState


def get_best_battle_path(game_state: GameState, comparator: SbcComparator, max_path_count) -> PlayPath:
    original_state = create_hand_state(game_state)
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


def get_best_battle_action(game_state: GameState, comparator: SbcComparator, max_path_count: int = 40_000) -> List[str]:
    path = get_best_battle_path(game_state, comparator, max_path_count)

    if path.plays:
        next_move = path.plays[0]
        if next_move[1] == -1:
            return [f"play {next_move[0] + 1}"]
        if next_move[1] == PLAY_DISCARD:
            return get_discard_commands(path.plays)
        return [f"play {next_move[0] + 1} {next_move[1]}"]
    return []


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
