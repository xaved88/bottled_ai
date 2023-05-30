from rs.common.comparators.common_general_comparator import default_comparisons, add_to_comparison_list, \
    CommonGeneralComparator
from rs.common.comparators.core.comparisons import *

comparisons = default_comparisons.copy()
comparisons.remove(most_free_early_draw)
comparisons.remove(most_free_draw)
comparisons.remove(least_incoming_damage_over_1)
add_to_comparison_list(comparisons, comparison_to_add=least_nob_adjusted_scaling_damage, after=most_lasting_intangible)


# Differences to normal comparator:
# * Penalize ourselves with nob_adjusted_incoming_damage for playing skills based on how long the fight will still go.
# * Mostly ignore draw_free_early and draw_acceptable_against_nob possibilities
# * (because e.g. Prepared is not a good card here).
class GremlinNobComparator(CommonGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
