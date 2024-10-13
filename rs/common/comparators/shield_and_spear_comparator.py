from rs.common.comparators.common_general_comparator import default_comparisons, add_to_comparison_list, \
    CommonGeneralComparator
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
comparisons.remove(lowest_health_monster)
add_to_comparison_list(comparisons, comparison_to_add=spear_lowest_health, after=most_dead_monsters)


# Difference to normal comparator:
# Prefer dealing damage to the Spear over the Shield
class ShieldAndSpearComparator(CommonGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
