from rs.common.comparators.common_general_comparator import CommonGeneralComparator, default_comparisons, \
    add_to_comparison_list
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
add_to_comparison_list(comparisons, comparison_to_add=least_awkward_shivs, after=most_enemy_weak)


class GeneralSilentComparator(CommonGeneralComparator):

    def __init__(self):
        super().__init__(comparisons)
