import math
from typing import List

from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.potion_id import PotionId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.potions import Potions
from rs.calculator.interfaces.powers import Powers
from rs.calculator.interfaces.relics import Relics
from rs.calculator.interfaces.target_interface import InflictDamageSummary, TargetInterface
from rs.calculator.powers import DEBUFFS, DEBUFFS_WHEN_NEGATIVE


class Target(TargetInterface):
    def __init__(self, is_player: bool, current_hp: int, max_hp: int, block: int, powers: Powers, relics=None,
                 potions=None):
        if relics is None:
            relics = {}
        if potions is None:
            potions = []
        self.is_player: bool = is_player
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.block: int = block
        self.powers: Powers = powers
        self.relics: Relics = relics
        self.potions: Potions = potions

    def inflict_damage(self, source, base_damage: int, hits: int, blockable: bool = True,
                       vulnerable_modifier: float = 1.5,
                       is_attack: bool = True, min_hp_damage: int = 1, is_orbs: bool = False,
                       card_id: CardId = None) -> InflictDamageSummary:
        damage = base_damage
        if self.powers.get(PowerId.VULNERABLE):
            damage = math.floor(damage * vulnerable_modifier)
        if source.powers.get(PowerId.BACK_ATTACK):
            damage = math.floor(damage * 1.5)
        if is_orbs and self.powers.get(PowerId.LOCK_ON):
            damage = math.floor(damage * 1.5)

        health_damage_dealt = 0
        times_block_triggered = 0
        sharp_hide_done = False
        trigger_malleable_block = 0

        for hit_damage in [damage for i in range(hits)]:
            if is_attack and self.powers.get(PowerId.BLOCK_RETURN):
                source.block += self.powers.get(PowerId.BLOCK_RETURN)
                times_block_triggered += 1

            # pre-block checks
            if self.powers.get(PowerId.INTANGIBLE_PLAYER):
                hit_damage = 1
            if self.powers.get(PowerId.INTANGIBLE_ENEMY):
                hit_damage = 1

            if self.powers.get(PowerId.FLIGHT):
                hit_damage = math.floor(hit_damage * .5)  # this may not be entirely accurate, pay attention

            if blockable and self.block:
                if self.block > hit_damage:
                    self.block -= hit_damage
                    hit_damage = 0
                else:
                    hit_damage -= self.block
                    self.block = 0
                    if source.relics.get(RelicId.HAND_DRILL):
                        self.add_powers({PowerId.VULNERABLE: 2}, source.relics, source.powers)

            # post-block checks
            if hit_damage > 0:
                if self.relics.get(RelicId.TORII) and hit_damage < 6:
                    hit_damage = 1
                if self.relics.get(RelicId.TUNGSTEN_ROD):
                    hit_damage -= 1

                if hit_damage > 0:
                    hit_damage = max(hit_damage, min_hp_damage)
                    if self.powers.get(PowerId.BUFFER):
                        self.powers[PowerId.BUFFER] -= 1
                        if not self.powers[PowerId.BUFFER]:
                            del self.powers[PowerId.BUFFER]
                        continue
                    if PowerId.INVINCIBLE in self.powers:
                        hit_damage = min(self.powers[PowerId.INVINCIBLE], hit_damage)
                    self.current_hp -= hit_damage
                    health_damage_dealt += hit_damage
                    if self.powers.get(PowerId.INVINCIBLE):
                        self.powers[PowerId.INVINCIBLE] -= hit_damage
                        if self.powers[PowerId.INVINCIBLE] < 0:
                            self.powers[PowerId.INVINCIBLE] = 0
                    if is_attack and self.powers.get(PowerId.PLATED_ARMOR):
                        self.powers[PowerId.PLATED_ARMOR] -= 1
                    if is_attack and self.powers.get(PowerId.FLIGHT):
                        self.powers[PowerId.FLIGHT] -= 1
                    if is_attack and self.powers.get(PowerId.ANGRY):
                        if not self.powers.get(PowerId.STRENGTH):
                            self.powers[PowerId.STRENGTH] = 0
                        self.powers[PowerId.STRENGTH] += self.powers.get(PowerId.ANGRY)
                    if is_attack and self.powers.get(PowerId.MODE_SHIFT):
                        self.powers[PowerId.MODE_SHIFT] -= hit_damage
                    if is_attack and self.powers.get(PowerId.CURL_UP):
                        self.block = self.powers.get(PowerId.CURL_UP)
                        del self.powers[PowerId.CURL_UP]
                    if is_attack and self.powers.get(PowerId.MALLEABLE):
                        self.powers[PowerId.MALLEABLE] += 1
                        trigger_malleable_block += 1
                    if is_attack and source.powers.get(PowerId.ENVENOM):
                        self.add_powers({PowerId.POISON: 1}, source.relics, source.powers)

            plated_armor = self.powers.get(PowerId.PLATED_ARMOR, None)
            if plated_armor is not None and plated_armor < 1:
                del self.powers[PowerId.PLATED_ARMOR]

            flight = self.powers.get(PowerId.FLIGHT, None)
            if flight is not None and flight < 1:
                self.damage = 0
                self.hits = 0
                del self.powers[PowerId.FLIGHT]
            ms = self.powers.get(PowerId.MODE_SHIFT)
            if ms is not None and ms < 1:
                self.damage = 0
                self.hits = 0
                self.block = 20
                del self.powers[PowerId.MODE_SHIFT]

            if card_id:
                if card_id == CardId.WALLOP:
                    source.block += health_damage_dealt

                if card_id == CardId.REAPER:
                    source.heal(health_damage_dealt, True, self.relics)

            if is_attack and (self.powers.get(PowerId.FLAME_BARRIER) or self.powers.get(PowerId.THORNS)):
                source.inflict_damage(
                    source=self,
                    base_damage=self.powers.get(PowerId.FLAME_BARRIER, 0) + self.powers.get(PowerId.THORNS, 0),
                    hits=1,
                    vulnerable_modifier=1,
                    is_attack=False,
                )

            if is_attack and (self.powers.get(PowerId.SHARP_HIDE)) and not sharp_hide_done:
                source.inflict_damage(
                    source=self,
                    base_damage=self.powers.get(PowerId.SHARP_HIDE),
                    hits=1,
                    vulnerable_modifier=1,
                    is_attack=False,
                )
                sharp_hide_done = True

            if self.current_hp < 0:
                health_damage_dealt += self.current_hp
                self.current_hp = 0
                if self.relics.get(RelicId.LIZARD_TAIL):
                    if self.relics[RelicId.LIZARD_TAIL] != -2:
                        self.heal(math.floor(self.max_hp * .5), True, self.relics, is_revive=True)
                        self.relics[RelicId.LIZARD_TAIL] = -2
                    continue

                if PotionId.FAIRY_IN_A_BOTTLE in self.potions:
                    self.heal(math.floor(self.max_hp * .3), True, self.relics, is_revive=True)
                    self.potions.remove(PotionId.FAIRY_IN_A_BOTTLE)
                    continue
                break  # target is dead, stop attacking

            if source.current_hp <= 0:
                source.current_hp = 0
                break  # source is dead, stop attacking

        if trigger_malleable_block:
            block_to_add = self.powers.get(PowerId.MALLEABLE)
            for i in range(trigger_malleable_block):
                self.block += block_to_add
                block_to_add -= 1

        if self.powers.get(PowerId.SPLIT) and self.current_hp <= self.max_hp / 2:
            self.damage = 0
            self.hits = 0
            del self.powers[PowerId.SPLIT]
        if self.powers.get(PowerId.SHIFTING):
            self.add_powers({PowerId.STRENGTH: -health_damage_dealt}, source.relics, source.powers)
        return times_block_triggered

    # returns a list of powerIds that were applied and not blocked by artifacts
    def add_powers(self, powers: Powers, relics: Relics, source_powers: Powers) -> List[PowerId]:
        applied_powers = []
        for power in powers:
            if self.powers.get(PowerId.ARTIFACT) and \
                    (power in DEBUFFS or (powers[power] < 0 and power in DEBUFFS_WHEN_NEGATIVE)):
                if self.powers[PowerId.ARTIFACT] == 1:
                    del self.powers[PowerId.ARTIFACT]
                else:
                    self.powers[PowerId.ARTIFACT] -= 1
                continue
            applied_powers.append(power)

            if power in self.powers:
                self.powers[power] += powers[power]
            else:
                self.powers[power] = powers[power]

            if source_powers and not self.is_player:
                if source_powers.get(PowerId.SADISTIC):
                    self.inflict_damage(self, source_powers.get(PowerId.SADISTIC), 1, vulnerable_modifier=1,
                                        is_attack=False)
                    #  'Self' as source is technically incorrect here, but I don't want to pass even more things into this function and it shouldn't break anything.

            if relics:
                if relics.get(RelicId.CHAMPION_BELT) and power == PowerId.VULNERABLE:
                    self.add_powers({PowerId.WEAKENED: 1}, relics, source_powers)
                if relics.get(RelicId.SNECKO_SKULL) and power == PowerId.POISON:
                    # Adding this manually, so we don't get into an infinite loop
                    self.powers[PowerId.POISON] += 1

        return applied_powers

    def get_state_string(self) -> str:
        state: str = f"{self.current_hp},{self.max_hp},{self.block}"
        power_keys = sorted([k.value for k in self.powers.keys()])
        for k in power_keys:
            state += k + str(self.powers[PowerId(k)]) + ","
        return state

    def heal(self, amount: int, is_player: bool, relics: Relics, is_revive: bool = False):
        if is_player and relics.get(RelicId.MARK_OF_THE_BLOOM):
            return
        if self.current_hp <= 0 and not is_revive:
            return
        else:
            if is_player and relics.get(RelicId.MAGIC_FLOWER):
                self.current_hp += round(amount * 1.5)
            else:
                self.current_hp += amount
            if self.current_hp > self.max_hp:
                self.current_hp = self.max_hp

