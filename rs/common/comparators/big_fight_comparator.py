from rs.common.comparators.common_general_comparator import default_comparisons, add_to_comparison_list, \
    move_in_comparison_list, CommonGeneralComparator
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers, after=most_dead_monsters)
move_in_comparison_list(comparisons, comparison_to_move=least_enemy_artifacts, after=most_enemy_vulnerable)
move_in_comparison_list(comparisons, comparison_to_move=least_bad_player_powers, after=most_less_good_player_powers)
move_in_comparison_list(comparisons, comparison_to_move=most_bad_cards_exhausted, after=least_incoming_damage)


class BigFightComparator(CommonGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
