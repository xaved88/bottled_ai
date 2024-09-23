from typing import List

from rs.calculator.enums.power_id import PowerId
from rs.common.comparators.common_general_comparator import CommonGeneralComparator, powers_we_like, \
    powers_we_like_less, powers_we_dislike, default_comparisons, Comparison
from rs.common.comparators.core.assessment import ComparatorAssessmentConfig
from rs.common.comparators.core.comparisons import *


class PmoGeneralComparator(CommonGeneralComparator):

    def __init__(self, comparisons: List[Comparison] = None):
        if comparisons is None:
            comparisons = default_comparisons.copy()
            move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers,
                                    after=lowest_health_monster)
            move_in_comparison_list(comparisons, comparison_to_move=most_orb_slots, after=most_good_player_powers)

        powers_we_love = [
            PowerId.ECHO_FORM,
            PowerId.ELECTRO,
        ]
        config = ComparatorAssessmentConfig(powers_we_like, powers_we_like_less, powers_we_dislike, powers_we_love)
        super().__init__(comparisons, config)

    def __init__(self, comparisons: List[Comparison] = None):
        powers_we_love = [
            PowerId.ECHO_FORM,
            PowerId.ELECTRO,
        ]
        config = ComparatorAssessmentConfig(powers_we_like, powers_we_like_less, powers_we_dislike, powers_we_love)
        super().__init__(default_comparisons if comparisons is None else comparisons, config)
