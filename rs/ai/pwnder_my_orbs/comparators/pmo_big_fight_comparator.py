from rs.ai.pwnder_my_orbs.comparators.pmo_general_comparator import PmoGeneralComparator
from rs.calculator.enums.power_id import PowerId
from rs.common.comparators.common_general_comparator import move_in_comparison_list, add_to_comparison_list, \
    default_comparisons
from rs.common.comparators.core.comparisons import *


def hate_bias(best: CA, challenger: CA) -> Optional[bool]:
    unawakened_present = False
    awakened_one = False

    for mon in challenger.state.monsters:
        if mon.powers.get(PowerId.UNAWAKENED, 0):
            unawakened_present = True
        if mon.name == 'Awakened One':
            awakened_one = True

    if not unawakened_present:
        if challenger.total_monster_health_percent() < 0.60 or awakened_one:
            return None  # when they've lost more than 40% we don't hate bias anymore

    return None if best.player_bias() == challenger.player_bias() \
        else challenger.player_bias() < best.player_bias()


comparisons = default_comparisons.copy()
move_in_comparison_list(comparisons, comparison_to_move=most_good_player_powers, after=most_dead_monsters)
move_in_comparison_list(comparisons, comparison_to_move=most_orb_slots, after=most_good_player_powers)
move_in_comparison_list(comparisons, comparison_to_move=least_enemy_artifacts, after=most_enemy_vulnerable)
add_to_comparison_list(comparisons, comparison_to_add=hate_bias, after=most_optimal_winning_battle)
add_to_comparison_list(comparisons, comparison_to_add=avoid_inconvenient_time_warp, after=least_incoming_damage_over_1)
comparisons.remove(most_powered_up_ritual_dagger)


class PmoBigFightComparator(PmoGeneralComparator):
    def __init__(self):
        super().__init__(comparisons)
