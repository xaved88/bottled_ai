from rs.ai.pwnder_my_orbs.comparators.pmo_general_comparator import default_comparisons, PmoGeneralComparator
from rs.common.comparators.common_general_comparator import move_in_comparison_list, add_to_comparison_list
from rs.common.comparators.core.comparisons import *


def hate_bias(best: CA, challenger: CA) -> Optional[bool]:
    if challenger.total_monster_health_percent() < 0.60:
        return None  # when they've lost more than 60% we don't hate bias anymore
    return None if best.player_bias() == challenger.player_bias() \
        else challenger.player_bias() < best.player_bias()


comparisons = default_comparisons.copy()
move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers, after=most_dead_monsters)
move_in_comparison_list(comparisons, comparison_to_move=least_enemy_artifacts, after=most_enemy_vulnerable)
move_in_comparison_list(comparisons, comparison_to_move=least_bad_player_powers, after=most_less_good_player_powers)
move_in_comparison_list(comparisons, comparison_to_move=most_bad_cards_exhausted, after=least_incoming_damage)
add_to_comparison_list(comparisons, comparison_to_add=hate_bias, after=most_optimal_winning_battle)


class PmoBigFightComparator(PmoGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
