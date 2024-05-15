from rs.common.comparators.common_general_comparator import default_comparisons, add_to_comparison_list, \
    CommonGeneralComparator
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
comparisons.remove(lowest_health_monster)
comparisons.remove(lowest_total_monster_health)


# Differences to normal comparator:
# * Encourage bot to not bother attacking if Transient is already not dealing damage to not waste cards and time.
class TransientComparator(CommonGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
