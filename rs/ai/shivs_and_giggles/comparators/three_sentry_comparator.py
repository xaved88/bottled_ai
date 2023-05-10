from typing import List

from rs.calculator.cards import CardId, CardType
from rs.calculator.comparator import SbcComparator
from rs.calculator.hand_state import HandState
from rs.calculator.powers import PowerId, get_power_count
from rs.calculator.relics import RelicId


class GCValues:
    def __init__(
            self,
            battle_lost: bool,
            battle_won: bool,
            incoming_damage: int,
            dead_monsters: int,
            lowest_health_preferred_sentry: int,
            total_monster_health: int,
            barricaded_block: int,
            draw_free_early: int,
            draw_free: int,
            draw_pay_early: int,
            draw_pay: int,
            energy: int,
            intangible: int,
            enemy_vulnerable: int,
            enemy_weak: int,
            player_powers_good: int,
            player_powers_less_good: int,
            player_powers_bad: int,
            bad_cards_exhausted: int,
            saved_for_later: int,
            awkward_shivs: int,
    ):
        self.battle_lost: bool = battle_lost
        self.battle_won: bool = battle_won
        self.incoming_damage: int = incoming_damage
        self.dead_monsters: int = dead_monsters
        self.lowest_health_preferred_sentry: int = lowest_health_preferred_sentry
        self.total_monster_health: int = total_monster_health
        self.barricaded_block: int = barricaded_block
        self.draw_free_early: int = draw_free_early
        self.draw_free: int = draw_free
        self.draw_pay_early: int = draw_pay_early
        self.draw_pay: int = draw_pay
        self.energy: int = energy
        self.intangible: int = intangible
        self.enemy_vulnerable: int = enemy_vulnerable
        self.enemy_weak: int = enemy_weak
        self.player_powers_good: int = player_powers_good
        self.player_powers_less_good: int = player_powers_less_good
        self.player_powers_bad: int = player_powers_bad
        self.bad_cards_exhausted: int = bad_cards_exhausted
        self.saved_for_later: int = saved_for_later
        self.awkward_shivs: int = awkward_shivs


powers_we_like: List[PowerId] = [
    PowerId.ACCURACY,
    PowerId.AFTER_IMAGE,
    PowerId.ARTIFACT,
    PowerId.BUFFER,
    PowerId.DEXTERITY,
    PowerId.FLAME_BARRIER,
    PowerId.INFINITE_BLADES,
    PowerId.INTANGIBLE,
    PowerId.METALLICIZE,
    PowerId.PLATED_ARMOR,
    PowerId.STRENGTH,
    PowerId.THORNS,
    PowerId.THOUSAND_CUTS,
    PowerId.TOOLS_OF_THE_TRADE,
]

powers_we_like_less: List[PowerId] = [
    PowerId.DRAW_CARD,
    PowerId.ENERGIZED,
    PowerId.NEXT_TURN_BLOCK,
]

powers_we_dislike: List[PowerId] = [
    PowerId.FRAIL,
    PowerId.WEAKENED,
]

# Difference to normal comparator:
# Go very aggressive on killing either the front or back sentry for as long as there are 3 sentries alive.


class ThreeSentriesSilentComparator(SbcComparator):

    def get_values(self, state: HandState, original: HandState) -> GCValues:
        battle_won = not [True for m in state.monsters if m.current_hp > 0]
        monsters_vulnerable_hp = [monster.current_hp - min(monster.powers.get(PowerId.VULNERABLE, 0) * 5, 3)
                                  for monster in state.monsters if monster.current_hp > 0]
        front_sentry_vulnerable_hp = state.monsters[0].current_hp - min(state.monsters[0].powers.get(PowerId.VULNERABLE, 0) * 5, 3)
        back_sentry_vulnerable_hp = state.monsters[2].current_hp - min(state.monsters[2].powers.get(PowerId.VULNERABLE, 0) * 5, 3)

        return GCValues(
            battle_lost=state.player.current_hp <= 0,
            battle_won=battle_won,
            incoming_damage=original.player.current_hp - state.player.current_hp,
            dead_monsters=len([True for monster in state.monsters if monster.current_hp <= 0]),
            lowest_health_preferred_sentry=0 if battle_won else min(front_sentry_vulnerable_hp, back_sentry_vulnerable_hp),
            total_monster_health=0 if battle_won else sum(monsters_vulnerable_hp),
            barricaded_block=sum([m.block for m in state.monsters if m.powers.get(PowerId.BARRICADE, 0) != 0]),
            draw_free_early=len([True for c in state.hand if c.id == CardId.DRAW_FREE_EARLY]),
            draw_free=len([True for c in state.hand if c.id == CardId.DRAW_FREE or c.id == CardId.DRAW_FREE_EARLY]),
            draw_pay_early=len([True for c in state.hand if c.id == CardId.DRAW_PAY_EARLY]),
            draw_pay=len([True for c in state.hand if c.id == CardId.DRAW_PAY or c.id == CardId.DRAW_PAY_EARLY]),
            energy=state.player.energy,
            intangible=state.player.powers.get(PowerId.INTANGIBLE, 0),
            enemy_vulnerable=min(max([m.powers.get(PowerId.VULNERABLE, 0) for m in state.monsters]), 4),
            enemy_weak=min(max([m.powers.get(PowerId.WEAKENED, 0) for m in state.monsters]), 4),
            player_powers_good=get_power_count(state.player.powers, powers_we_like),
            player_powers_less_good=get_power_count(state.player.powers, powers_we_like_less),
            player_powers_bad=get_power_count(state.player.powers, powers_we_dislike),
            bad_cards_exhausted=len([True for c in state.exhaust_pile if c.type == CardType.CURSE or c.type == CardType.STATUS]),  # We mostly don't exhaust cards yet though.
            saved_for_later=len([True for c in state.discard_pile if c.ethereal and c.type != CardType.CURSE and c.type != CardType.STATUS]),
            awkward_shivs=len([True for c in state.hand or state.discard_pile if c.id == CardId.SHIV]),
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
        if best.energy != challenger.energy:
            return challenger.energy > best.energy
        return False

    def does_challenger_defeat_the_best(self, best_state: HandState, challenger_state: HandState,
                                        original: HandState) -> bool:
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
        if best.dead_monsters != challenger.dead_monsters:
            return challenger.dead_monsters > best.dead_monsters
        if best.lowest_health_preferred_sentry != challenger.lowest_health_preferred_sentry:
            return challenger.lowest_health_preferred_sentry < best.lowest_health_preferred_sentry
        if max(2, best.incoming_damage) != max(2, challenger.incoming_damage):
            return challenger.incoming_damage < best.incoming_damage
        if max(1, best.enemy_vulnerable) != max(1, challenger.enemy_vulnerable):
            return challenger.enemy_vulnerable > best.enemy_vulnerable
        if max(1, best.enemy_weak) != max(1, challenger.enemy_weak):
            return challenger.enemy_weak > best.enemy_weak
        if best.total_monster_health != challenger.total_monster_health:
            return challenger.total_monster_health < best.total_monster_health
        if best.barricaded_block != challenger.barricaded_block:
            return challenger.barricaded_block < best.barricaded_block
        if best.draw_pay_early != challenger.draw_pay_early:
            return challenger.draw_pay_early > best.draw_pay_early
        if best.draw_pay != challenger.draw_pay:
            return challenger.draw_pay > best.draw_pay
        if best.player_powers_good != challenger.player_powers_good:
            return challenger.player_powers_good > best.player_powers_good
        if best.player_powers_bad != challenger.player_powers_bad:
            return challenger.player_powers_bad < best.player_powers_bad
        if best.player_powers_less_good != challenger.player_powers_less_good:
            return challenger.player_powers_less_good > best.player_powers_less_good
        if best.bad_cards_exhausted != challenger.bad_cards_exhausted:
            return challenger.bad_cards_exhausted > best.bad_cards_exhausted
        if best.incoming_damage != challenger.incoming_damage:
            return challenger.incoming_damage < best.incoming_damage
        if best.saved_for_later != challenger.saved_for_later:
            return challenger.saved_for_later > best.saved_for_later
        if best.awkward_shivs != challenger.awkward_shivs:
            return challenger.awkward_shivs < best.awkward_shivs
        if best.energy != challenger.energy:
            return challenger.energy > best.energy
        return False
