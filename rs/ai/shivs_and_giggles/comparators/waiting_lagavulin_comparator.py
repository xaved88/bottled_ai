from rs.common.comparators.common_general_comparator import default_comparisons, add_to_comparison_list, \
    move_in_comparison_list, CommonGeneralComparator
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
comparisons.remove(lowest_health_monster)
comparisons.remove(lowest_total_monster_health)
add_to_comparison_list(comparisons, comparison_to_add=least_awkward_shivs, after=most_enemy_weak)
add_to_comparison_list(comparisons, comparison_to_add=highest_health_monster, after=most_lasting_intangible)
move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers, after=highest_health_monster)


# Differences to normal comparator:
# Do not cause damage, instead play powers and debuffs.
# See battle_handler.py for the special criteria to get here.
class WaitingLagavulinSilentComparator(CommonGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
