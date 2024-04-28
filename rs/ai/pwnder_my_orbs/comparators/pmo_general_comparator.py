from typing import List

from rs.calculator.enums.power_id import PowerId
from rs.common.comparators.common_general_comparator import Comparison, CommonGeneralComparator, powers_we_like, \
    powers_we_like_less, powers_we_dislike
from rs.common.comparators.core.assessment import ComparatorAssessmentConfig
from rs.common.comparators.core.comparisons import *

default_comparisons = [
    battle_not_lost,
    battle_is_won,
    most_optimal_winning_battle,
    most_free_early_draw,
    most_free_draw,
    most_lasting_intangible,
    least_incoming_damage_over_1,
    most_great_player_powers,
    most_dead_monsters,
    most_enemy_vulnerable,
    most_enemy_weak,
    least_awkward_shivs,
    lowest_health_monster,
    most_good_player_powers,
    most_orb_slots,
    lowest_total_monster_health,
    lowest_barricaded_block,
    lowest_enemy_plated_armor,
    most_channeled_orbs,
    most_draw_pay_early,
    most_draw_pay,
    least_bad_player_powers,
    most_less_good_player_powers,
    least_enemy_artifacts,
    most_bad_cards_exhausted,
    most_powered_up_ritual_dagger,
    most_powered_up_genetic_algorithm,
    least_incoming_damage,
    most_ethereal_cards_saved_for_later,
    most_powered_up_claws,
    most_retained_cards,
    least_powered_down_steam_barrier,
    most_energy,
]


class PmoGeneralComparator(CommonGeneralComparator):

    def __init__(self, comparisons: List[Comparison] = None):
        powers_we_love = [
            PowerId.ECHO_FORM,
            PowerId.ELECTRO,
        ]
        config = ComparatorAssessmentConfig(powers_we_like, powers_we_like_less, powers_we_dislike, powers_we_love)
        super().__init__(default_comparisons if comparisons is None else comparisons, config)
