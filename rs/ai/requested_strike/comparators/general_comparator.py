from rs.calculator.cards import CardId
from rs.calculator.comparator import SbcComparator
from rs.calculator.hand_state import HandState
from rs.calculator.powers import PowerId
from rs.calculator.relics import RelicId


class GCValues:
    def __init__(
            self,
            battle_lost: bool,
            battle_won: bool,
            incoming_damage: int,
            dead_monsters: int,
            lowest_health_monster: int,
            total_monster_health: int,
            draw_free_early: int,
            draw_free: int,
            draw_pay_early: int,
            draw_pay: int,
            energy: int,
            intangible: int,
            enemy_vulnerable: int,
            enemy_weak: int,
    ):
        self.battle_lost: bool = battle_lost
        self.battle_won: bool = battle_won
        self.incoming_damage: int = incoming_damage
        self.dead_monsters: int = dead_monsters
        self.lowest_health_monster: int = lowest_health_monster
        self.total_monster_health: int = total_monster_health
        self.draw_free_early: int = draw_free_early
        self.draw_free: int = draw_free
        self.draw_pay_early: int = draw_pay_early
        self.draw_pay: int = draw_pay
        self.energy: int = energy
        self.intangible: int = intangible
        self.enemy_vulnerable: int = enemy_vulnerable
        self.enemy_weak: int = enemy_weak


class GeneralComparator(SbcComparator):

    def get_values(self, state: HandState, original: HandState) -> GCValues:
        battle_won = not [True for m in state.monsters if m.current_hp > 0]
        monsters_vulnerable_hp = [monster.current_hp - min(monster.powers.get(PowerId.VULNERABLE, 0) * 5, 3)
                                  for monster in state.monsters if monster.current_hp > 0]
        return GCValues(
            battle_lost=state.player.current_hp <= 0,
            battle_won=battle_won,
            incoming_damage=original.player.current_hp - state.player.current_hp,
            dead_monsters=len([True for monster in state.monsters if monster.current_hp <= 0]),
            lowest_health_monster=0 if battle_won else min(monsters_vulnerable_hp),
            total_monster_health=0 if battle_won else sum(monsters_vulnerable_hp),
            draw_free_early=len([True for c in state.hand if c.id == CardId.DRAW_FREE_EARLY]),
            draw_free=len([True for c in state.hand if c.id == CardId.DRAW_FREE or c.id == CardId.DRAW_FREE_EARLY]),
            draw_pay_early=len([True for c in state.hand if c.id == CardId.DRAW_PAY_EARLY]),
            draw_pay=len([True for c in state.hand if c.id == CardId.DRAW_PAY or c.id == CardId.DRAW_PAY_EARLY]),
            energy=state.player.energy,
            intangible=state.player.powers.get(PowerId.INTANGIBLE, 0),
            enemy_vulnerable=min(max([m.powers.get(PowerId.VULNERABLE, 0) for m in state.monsters]), 4),
            enemy_weak=min(max([m.powers.get(PowerId.WEAKENED, 0) for m in state.monsters]), 4),
        )

    def optimize_battle_won(self, best: GCValues, challenger: GCValues, best_state: HandState,
                            challenger_state: HandState, original: HandState) -> bool:
        if best_state.player.max_hp != challenger_state.player.max_hp:
            return challenger_state.player.max_hp > best_state.player.max_hp
        if best.incoming_damage != challenger.incoming_damage:
            return challenger.incoming_damage < best.incoming_damage
        if RelicId.PEN_NIB in best_state.player.relics and \
                best_state.player.relics[RelicId.PEN_NIB] != challenger_state.player.relics[RelicId.PEN_NIB]:
            return challenger_state.player.relics[RelicId.PEN_NIB] > best_state.player.relics[RelicId.PEN_NIB]
        if RelicId.NUNCHAKU in best_state.player.relics and \
                best_state.player.relics[RelicId.NUNCHAKU] != challenger_state.player.relics[RelicId.NUNCHAKU]:
            return challenger_state.player.relics[RelicId.NUNCHAKU] > best_state.player.relics[RelicId.NUNCHAKU]
        return False

    def does_best_remain_the_best(self, best_state: HandState, challenger_state: HandState,
                                  original: HandState) -> bool:
        """
        - split
        """
        best = self.get_values(best_state, original)
        challenger = self.get_values(challenger_state, original)

        # battle end conditions
        if best.battle_lost != challenger.battle_lost:
            return not challenger.battle_lost
        if best.battle_won != challenger.battle_won:
            return challenger.battle_won
        if best.battle_won:
            return self.optimize_battle_won(best, challenger, best_state, challenger_state, original)

        # normal conditions
        if best.draw_free_early != challenger.draw_free_early:
            return challenger.draw_free_early > best.draw_free_early
        if best.draw_free != challenger.draw_free:
            return challenger.draw_free > best.draw_free
        if max(1, best.intangible) != max(1, challenger.intangible):
            return challenger.intangible > best.intangible
        if max(2, best.incoming_damage) != max(2, challenger.incoming_damage):
            return challenger.incoming_damage < best.incoming_damage
        if best.dead_monsters != challenger.dead_monsters:
            return challenger.dead_monsters > best.dead_monsters
        if max(1, best.enemy_vulnerable) != max(1, challenger.enemy_vulnerable):
            return challenger.enemy_vulnerable > best.enemy_vulnerable
        if max(1, best.enemy_weak) != max(1, challenger.enemy_weak):
            return challenger.enemy_weak > best.enemy_weak
        if best.lowest_health_monster != challenger.lowest_health_monster:
            return challenger.lowest_health_monster < best.lowest_health_monster
        if best.total_monster_health != challenger.total_monster_health:
            return challenger.total_monster_health < best.total_monster_health
        if best.draw_pay_early != challenger.draw_pay_early:
            return challenger.draw_pay_early > best.draw_pay_early
        if best.draw_pay != challenger.draw_pay:
            return challenger.draw_pay > best.draw_pay
        if best.energy != challenger.energy:
            return challenger.energy > best.energy
        return False
