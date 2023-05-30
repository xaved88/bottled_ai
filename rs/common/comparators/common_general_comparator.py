from typing import Callable, List

from rs.calculator.battle_state import BattleState
from rs.calculator.comparator import SbcComparator
from rs.common.comparators.core.comparisons import *

Comparison = Callable[[CA, CA], Optional[bool]]

default_comparisons = [
    battle_not_lost,
    battle_is_won,
    most_optimal_winning_battle,
    most_free_early_draw,
    most_free_draw,
    most_lasting_intangible,
    least_incoming_damage_over_1,
    most_dead_monsters,
    most_enemy_vulnerable,
    most_enemy_weak,
    lowest_health_monster,
    lowest_total_monster_health,
    most_draw_pay_early,
    most_draw_pay,
    most_energy,
]


class CommonGeneralComparator(SbcComparator):

    def __init__(self, comparisons: List[Comparison] = None):
        self.comparisons: List[Comparison] = default_comparisons if comparisons is None else comparisons

    def does_challenger_defeat_the_best(self, best_state: BattleState, challenger_state: BattleState,
                                        original: BattleState) -> bool:
        best = CA(best_state, original)
        challenger = CA(challenger_state, original)

        for c in self.comparisons:
            v = c(best, challenger)
            if v is not None:
                return v
        return False
