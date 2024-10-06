from typing import Optional

from rs.common.comparators.core.assessment import ComparatorAssessment as CA


def battle_not_lost(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.battle_lost() == challenger.battle_lost() else not challenger.battle_lost()


def battle_is_won(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.battle_won() == challenger.battle_won() else challenger.battle_won()


def most_optimal_winning_battle(best: CA, challenger: CA) -> Optional[bool]:
    if not best.battle_won() or not challenger.battle_won():
        return None

    if best.player_max_hp() != challenger.player_max_hp():
        return challenger.player_max_hp() > best.player_max_hp()

    if best.most_kills_with_lesson_learned() != challenger.most_kills_with_lesson_learned():
        return challenger.most_kills_with_lesson_learned() > best.most_kills_with_lesson_learned()

    if best.power_up_ritual_dagger() != challenger.power_up_ritual_dagger():
        return challenger.power_up_ritual_dagger() > best.power_up_ritual_dagger()

    if best.power_up_genetic_algorithm() != challenger.power_up_genetic_algorithm():
        return challenger.power_up_genetic_algorithm() > best.power_up_genetic_algorithm()

    if best.incoming_damage() != challenger.incoming_damage():
        return challenger.incoming_damage() < best.incoming_damage()

    if best.repair_count() != challenger.repair_count():
        return challenger.repair_count() > best.repair_count()

    if best.pen_nib_counter() != challenger.pen_nib_counter():
        return challenger.pen_nib_counter() > best.pen_nib_counter()

    if best.nunchaku_counter() != challenger.nunchaku_counter():
        return challenger.nunchaku_counter() > best.nunchaku_counter()

    if best.ink_bottle_counter() != challenger.ink_bottle_counter():
        return challenger.ink_bottle_counter() > best.ink_bottle_counter()

    if best.cards_left_in_hand() != challenger.cards_left_in_hand():
        return challenger.cards_left_in_hand() > best.cards_left_in_hand()

    if best.energy() != challenger.energy():
        return challenger.energy() > best.energy()

    return False


def most_free_early_draw(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_free_early() == challenger.draw_free_early() \
        else challenger.draw_free_early() > best.draw_free_early()


def most_free_draw(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_free() == challenger.draw_free() \
        else challenger.draw_free() > best.draw_free()


def most_lasting_intangible(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(1, best.intangible()) == max(1, challenger.intangible()) \
        else challenger.intangible() > best.intangible()


def least_incoming_damage_over_1(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(2, best.incoming_damage()) == max(2, challenger.incoming_damage()) \
        else challenger.incoming_damage() < best.incoming_damage()


def most_dead_monsters(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.dead_monsters() == challenger.dead_monsters() \
        else challenger.dead_monsters() > best.dead_monsters()


def most_dead_edge_monsters(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.dead_edge_monsters() == challenger.dead_edge_monsters() \
        else challenger.dead_edge_monsters() > best.dead_edge_monsters()


def most_enemy_vulnerable(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(1, best.enemy_vulnerable()) == max(1, challenger.enemy_vulnerable()) \
        else challenger.enemy_vulnerable() > best.enemy_vulnerable()


def most_enemy_weak(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(1, best.enemy_weak()) == max(1, challenger.enemy_weak()) \
        else challenger.enemy_weak() > best.enemy_weak()


def most_enemy_talking_to_hand(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.enemy_talking_to_hand() == challenger.enemy_talking_to_hand() \
        else challenger.enemy_talking_to_hand() > best.enemy_talking_to_hand()


def lowest_health_monster(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.lowest_health_monster() == challenger.lowest_health_monster() \
        else challenger.lowest_health_monster() < best.lowest_health_monster()


# mainly only useful for lagavulin or intentional waiting
def highest_health_monster(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.lowest_true_health_monster() == challenger.lowest_true_health_monster() \
        else challenger.lowest_true_health_monster() > best.lowest_true_health_monster()


def lowest_health_edge_monster(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.lowest_health_edge_monster() == challenger.lowest_health_edge_monster() \
        else challenger.lowest_health_edge_monster() < best.lowest_health_edge_monster()


def lowest_total_monster_health(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.total_monster_health() == challenger.total_monster_health() \
        else challenger.total_monster_health() < best.total_monster_health()


def lowest_barricaded_block(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.barricaded_block() == challenger.barricaded_block() \
        else challenger.barricaded_block() < best.barricaded_block()


def most_draw_pay_early(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_pay_early() == challenger.draw_pay_early() \
        else challenger.draw_pay_early() > best.draw_pay_early()


def most_draw_pay(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_pay() == challenger.draw_pay() else challenger.draw_pay() > best.draw_pay()


def most_good_player_powers(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.player_powers_good() == challenger.player_powers_good() \
        else challenger.player_powers_good() > best.player_powers_good()


def most_great_player_powers(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.player_powers_great() == challenger.player_powers_great() \
        else challenger.player_powers_great() > best.player_powers_great()


def most_less_good_player_powers(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.player_powers_less_good() == challenger.player_powers_less_good() \
        else challenger.player_powers_less_good() > best.player_powers_less_good()


def least_bad_player_powers(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.player_powers_bad() == challenger.player_powers_bad() \
        else challenger.player_powers_bad() < best.player_powers_bad()


def most_bad_cards_exhausted(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.bad_cards_exhausted() == challenger.bad_cards_exhausted() \
        else challenger.bad_cards_exhausted() > best.bad_cards_exhausted()


def most_energy(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.energy() == challenger.energy() else challenger.energy() > best.energy()


def least_incoming_damage(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.incoming_damage() == challenger.incoming_damage() \
        else challenger.incoming_damage() < best.incoming_damage()


def most_ethereal_cards_saved_for_later(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.ethereal_saved_for_later() == challenger.ethereal_saved_for_later() \
        else challenger.ethereal_saved_for_later() > best.ethereal_saved_for_later()


def least_awkward_shivs(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.awkward_shivs() == challenger.awkward_shivs() \
        else challenger.awkward_shivs() < best.awkward_shivs()


def least_enemy_artifacts(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.enemy_artifacts() == challenger.enemy_artifacts() \
        else challenger.enemy_artifacts() < best.enemy_artifacts()


def least_nob_adjusted_scaling_damage(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.nob_adjusted_scaling_damage() == challenger.nob_adjusted_scaling_damage() \
        else challenger.nob_adjusted_scaling_damage() < best.nob_adjusted_scaling_damage()


def most_orb_slots(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.orb_slot_count() == challenger.orb_slot_count() \
        else challenger.orb_slot_count() > best.orb_slot_count()


def most_channeled_orbs(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.channeled_orb_count() == challenger.channeled_orb_count() \
        else challenger.channeled_orb_count() > best.channeled_orb_count()


def most_cards_left_in_hand(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.cards_left_in_hand() == challenger.cards_left_in_hand() \
        else challenger.cards_left_in_hand() > best.cards_left_in_hand()


def most_powered_up_ritual_dagger(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.power_up_ritual_dagger() == challenger.power_up_ritual_dagger() \
        else challenger.power_up_ritual_dagger() > best.power_up_ritual_dagger()


def most_powered_up_genetic_algorithm(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.power_up_genetic_algorithm() == challenger.power_up_genetic_algorithm() \
        else challenger.power_up_genetic_algorithm() > best.power_up_genetic_algorithm()


def least_powered_down_steam_barrier(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.power_down_steam_barrier() == challenger.power_down_steam_barrier() \
        else challenger.power_down_steam_barrier() < best.power_down_steam_barrier()


def most_powered_up_claws(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.powered_up_claws() == challenger.powered_up_claws() \
        else challenger.powered_up_claws() > best.powered_up_claws()


def lowest_enemy_plated_armor(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.enemy_plated_armor() == challenger.enemy_plated_armor() \
        else challenger.enemy_plated_armor() < best.enemy_plated_armor()


def stance_is_not_wrath(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.stance_is_not_wrath() == challenger.stance_is_not_wrath() \
        else challenger.stance_is_not_wrath() < best.stance_is_not_wrath()


def stance_is_calm(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.stance_is_calm() == challenger.stance_is_calm() \
        else challenger.stance_is_calm() > best.stance_is_calm()


def no_blasphemy(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.played_blasphemy() == challenger.played_blasphemy() \
        else challenger.played_blasphemy() < best.played_blasphemy()


def killed_with_lesson_learned(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.most_kills_with_lesson_learned() == challenger.most_kills_with_lesson_learned() \
        else challenger.most_kills_with_lesson_learned() > best.most_kills_with_lesson_learned()


def most_tranquility(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.count_tranquility() == challenger.count_tranquility() \
        else challenger.count_tranquility() > best.count_tranquility()


def most_crescendo(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.count_crescendo() == challenger.count_crescendo() \
        else challenger.count_crescendo() > best.count_crescendo()


def most_block_saved_for_next_turn(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.block_for_next_turn() == challenger.block_for_next_turn() \
        else challenger.block_for_next_turn() > best.block_for_next_turn()


def kept_expensive_decreasing_cost_retain_cards(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.count_expensive_cheapening_retain_cards() == challenger.count_expensive_cheapening_retain_cards() \
        else challenger.count_expensive_cheapening_retain_cards() > best.count_expensive_cheapening_retain_cards()


def avoid_inconvenient_time_warp(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.inconvenient_time_warp_count() == challenger.inconvenient_time_warp_count() \
        else challenger.inconvenient_time_warp_count() < best.inconvenient_time_warp_count()


def preserve_revive_options(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.revive_option_count() == challenger.revive_option_count() \
        else challenger.revive_option_count() > best.revive_option_count()


def spear_lowest_health(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.spear_lowest_health() == challenger.spear_lowest_health() \
        else challenger.spear_lowest_health() < best.spear_lowest_health()


def excessive_amount_of_cards_played_this_turn(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.excessive_amount_of_cards_played_this_turn() == challenger.excessive_amount_of_cards_played_this_turn() \
        else challenger.excessive_amount_of_cards_played_this_turn() < best.excessive_amount_of_cards_played_this_turn()
