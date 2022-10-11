from typing import List, Tuple, Callable

from rs.calculator.game_state_converter import create_hand_state
from rs.calculator.hand_state import Play
from rs.calculator.play_path_report import PathPlayReport
from rs.calculator.play_path import PlayPath, get_paths, get_paths_performant
from rs.machine.state import GameState

# (best:PathPlayReport, challenger:PathPlayReport) -> is_challenger_better: bool
ReportComparator = Callable[[PathPlayReport, PathPlayReport], bool]


def default_path_comparator(best: PathPlayReport, challenger: PathPlayReport) -> bool:
    if best.battle_lost != challenger.battle_lost:
        return not challenger.battle_lost
    if best.battle_won != challenger.battle_won:
        return challenger.battle_won
    if max(2, best.incoming_damage) != max(2, challenger.incoming_damage):
        return challenger.incoming_damage < best.incoming_damage
    if best.dead_monsters != challenger.dead_monsters:
        return challenger.dead_monsters > best.dead_monsters
    if best.lowest_health_monster != challenger.lowest_health_monster:
        return challenger.lowest_health_monster < best.lowest_health_monster
    if best.total_monster_health != challenger.total_monster_health:
        return challenger.total_monster_health < best.total_monster_health
    return False


def get_best_battle_path(game_state: GameState, comparator: ReportComparator) -> PathPlayReport:
    original_hp = game_state.combat_state()['player']['current_hp']
    hand_state = create_hand_state(game_state)
    paths = {}
    get_paths_performant(PlayPath([], hand_state), paths)
    print(f"Number of paths found: {len(paths.keys())}")
    for path in paths.values():
        path.state.end_turn()

    best_report = None
    reports = [PathPlayReport(path.state, original_hp, path) for path in paths.values()]
    for report in reports:
        if best_report is None:
            best_report = report
        else:
            if comparator(best_report, report):
                best_report = report

    return best_report
