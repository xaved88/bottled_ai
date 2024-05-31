from rs.ai.pwnder_my_orbs.comparators.pmo_general_comparator import default_comparisons, PmoGeneralComparator
from rs.calculator.enums.power_id import PowerId
from rs.common.comparators.common_general_comparator import move_in_comparison_list, add_to_comparison_list
from rs.common.comparators.core.comparisons import *


def hate_bias(best: CA, challenger: CA) -> Optional[bool]:
    unawakened_present = False
    for mon in challenger.state.monsters:
        if mon.powers.get(PowerId.UNAWAKENED, 0):
            unawakened_present = True
    if challenger.total_monster_health_percent() < 0.60 and (not unawakened_present or challenger.total_monster_health_percent() < 0.20):
        return None  # when they've lost more than 60% we don't hate bias anymore
    return None if best.player_bias() == challenger.player_bias() \
        else challenger.player_bias() < best.player_bias()


comparisons = default_comparisons.copy()
move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers, after=most_dead_monsters)
move_in_comparison_list(comparisons, comparison_to_move=least_enemy_artifacts, after=most_enemy_vulnerable)
move_in_comparison_list(comparisons, comparison_to_move=least_bad_player_powers, after=most_less_good_player_powers)
move_in_comparison_list(comparisons, comparison_to_move=most_bad_cards_exhausted, after=least_incoming_damage)
add_to_comparison_list(comparisons, comparison_to_add=hate_bias, after=most_optimal_winning_battle)
add_to_comparison_list(comparisons, comparison_to_add=avoid_inconvenient_time_warp, after=least_incoming_damage_over_1)
move_in_comparison_list(comparisons, comparison_to_move=most_powered_up_ritual_dagger,
                        after=most_powered_up_genetic_algorithm)


class PmoBigFightComparator(PmoGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
