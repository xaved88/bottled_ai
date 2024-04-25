from rs.ai.pwnder_my_orbs.comparators.pmo_general_comparator import PmoGeneralComparator, default_comparisons
from rs.common.comparators.common_general_comparator import add_to_comparison_list, move_in_comparison_list
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
comparisons.remove(lowest_health_monster)
comparisons.remove(lowest_total_monster_health)
add_to_comparison_list(comparisons, comparison_to_add=highest_health_monster, after=most_lasting_intangible)
move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers, after=highest_health_monster)


# Differences to normal comparator:
# Do not cause damage, instead play powers and debuffs.
class PmoWaitingLagavulinComparator(PmoGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
