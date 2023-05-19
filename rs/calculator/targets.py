import math
from typing import List

from rs.calculator.powers import PowerId, Powers, DEBUFFS, DEBUFFS_WHEN_NEGATIVE
from rs.calculator.relics import Relics, RelicId

# hp_damage_dealt
InflictDamageSummary = (int)


class Target:
    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, relics=None):
        if relics is None:
            relics = {}
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.block: int = block
        self.powers: Powers = powers
        self.relics: Relics = relics

    def inflict_damage(self, source, base_damage: int, hits: int, blockable: bool = True,
                       vulnerable_modifier: float = 1.5,
                       is_attack: bool = True, min_hp_damage: int = 1) -> InflictDamageSummary:
        damage = base_damage
        if self.powers.get(PowerId.VULNERABLE):
            damage = math.floor(damage * vulnerable_modifier)

        health_damage_dealt = 0
        trigger_malleable_block = 0

        # inflict self damage from sharp_hide
        if is_attack and (self.powers.get(PowerId.SHARP_HIDE)):
            source.inflict_damage(
                source=self,
                base_damage=self.powers.get(PowerId.SHARP_HIDE),
                hits=1,
                vulnerable_modifier=1,
                is_attack=False,
            )

        for hit_damage in [damage for i in range(hits)]:
            if is_attack and (self.powers.get(PowerId.FLAME_BARRIER) or self.powers.get(PowerId.THORNS)):
                source.inflict_damage(
                    source=self,
                    base_damage=self.powers.get(PowerId.FLAME_BARRIER, 0) + self.powers.get(PowerId.THORNS, 0),
                    hits=1,
                    vulnerable_modifier=1,
                    is_attack=False,
                )

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
                        self.add_powers({PowerId.VULNERABLE: 2}, source.relics)

            if hit_damage > 0:
                if self.relics.get(RelicId.TORII) and hit_damage < 6:
                    hit_damage = 1
                if self.powers.get(PowerId.INTANGIBLE_PLAYER):
                    hit_damage = 1
                if self.powers.get(PowerId.INTANGIBLE_ENEMY):
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
                    self.current_hp -= hit_damage
                    health_damage_dealt += hit_damage
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
                        self.add_powers({PowerId.POISON: 1}, source.relics)
                    if self.current_hp < 0:
                        health_damage_dealt += self.current_hp
                        self.current_hp = 0
                        break  # target is dead, stop attacking

            if source.current_hp <= 0:
                source.current_hp = 0
                break  # source is dead, stop attacking

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
            self.add_powers({PowerId.STRENGTH: -health_damage_dealt}, source.relics)
        return (health_damage_dealt)

    # returns a list of powerIds that were applied and not blocked by artifacts
    def add_powers(self, powers: Powers, relics: Relics) -> List[PowerId]:
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

            if relics:
                if relics.get(RelicId.SNECKO_SKULL) and power == PowerId.POISON:
                    self.powers[PowerId.POISON] += 1
                if relics.get(RelicId.CHAMPION_BELT) and power == PowerId.VULNERABLE:
                    if PowerId.WEAKENED in self.powers:
                        self.powers[PowerId.WEAKENED] += 1
                    else:
                        self.powers[PowerId.WEAKENED] = 1

        return applied_powers

    def get_state_string(self) -> str:
        state: str = f"{self.current_hp},{self.max_hp},{self.block}"
        power_keys = sorted([k.value for k in self.powers.keys()])
        for k in power_keys:
            state += k + str(self.powers[PowerId(k)]) + ","
        return state

    def heal(self, amount: int):
        self.current_hp += amount
        if self.current_hp > self.max_hp:
            self.current_hp = self.max_hp


class Player(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, energy: int, relics: Relics):
        super().__init__(current_hp, max_hp, block, powers, relics)
        self.energy: int = energy

    def get_state_string(self) -> str:
        return super().get_state_string() + str(self.energy) + ","


class Monster(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, damage: int = 0, hits: int = 0, is_gone: bool = False):
        super().__init__(current_hp, max_hp, block, powers)
        self.damage: int = damage
        self.hits: int = hits
        self.is_gone: bool = is_gone

    def get_state_string(self) -> str:
        return super().get_state_string() + f"{self.damage},{self.hits},"
