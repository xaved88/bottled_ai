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

    if best.incoming_damage() != challenger.incoming_damage():
        return challenger.incoming_damage() < best.incoming_damage()

    if best.pen_nib_counter() != challenger.pen_nib_counter():
        return challenger.pen_nib_counter() > best.pen_nib_counter()

    if best.nunchaku_counter() != challenger.nunchaku_counter():
        return challenger.nunchaku_counter() > best.nunchaku_counter()

    if best.energy() != challenger.energy():
        return challenger.energy() > best.energy()
    return False


def most_free_early_draw(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_free_early() == challenger.draw_free_early() \
        else challenger.draw_free_early() > best.draw_free_early()


def most_free_draw(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_free() == challenger.draw_free() else challenger.draw_free() > best.draw_free()


def most_lasting_intangible(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(1, best.intangible()) == max(1, challenger.intangible()) \
        else challenger.intangible() > best.intangible()


def least_incoming_damage_over_1(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(2, best.incoming_damage()) == max(2, challenger.incoming_damage()) \
        else challenger.incoming_damage() < best.incoming_damage()


def most_dead_monsters(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.dead_monsters() == challenger.dead_monsters() \
        else challenger.dead_monsters() > best.dead_monsters()


def most_enemy_vulnerable(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(1, best.enemy_vulnerable()) == max(1, challenger.enemy_vulnerable()) \
        else challenger.enemy_vulnerable() > best.enemy_vulnerable()


def most_enemy_weak(best: CA, challenger: CA) -> Optional[bool]:
    return None if max(1, best.enemy_weak()) == max(1, challenger.enemy_weak()) \
        else challenger.enemy_weak() > best.enemy_weak()


def lowest_health_monster(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.lowest_health_monster() == challenger.lowest_health_monster() \
        else challenger.lowest_health_monster() < best.lowest_health_monster()


def lowest_total_monster_health(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.total_monster_health() == challenger.total_monster_health() \
        else challenger.total_monster_health() < best.total_monster_health()


def most_draw_pay_early(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_pay_early() == challenger.draw_pay_early() \
        else challenger.draw_pay_early() > best.draw_pay_early()


def most_draw_pay(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.draw_pay() == challenger.draw_pay() else challenger.draw_pay() > best.draw_pay()


def most_energy(best: CA, challenger: CA) -> Optional[bool]:
    return None if best.energy() == challenger.energy() else challenger.energy() > best.energy()
