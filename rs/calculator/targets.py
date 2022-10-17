import math
from typing import List

from rs.calculator.powers import PowerId, Powers, DEBUFFS
from rs.calculator.relics import Relics, RelicId


class Target:
    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, relics=None):
        if relics is None:
            relics = {}
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.block: int = block
        self.powers: Powers = powers
        self.relics: Relics = relics

    def inflict_damage(self, base_damage: int, hits: int, blockable: bool = True, vulnerable_modifier: float = 1.5,
                       is_attack: bool = True, min_hp_damage: int = 1) -> int: # returns health damage dealt
        damage = base_damage
        if self.powers.get(PowerId.VULNERABLE):
            damage = math.floor(damage * vulnerable_modifier)

        health_damage_dealt = 0
        for hit_damage in [damage for i in range(hits)]:
            if blockable and self.block:
                if self.block > hit_damage:
                    self.block -= hit_damage
                    hit_damage = 0
                else:
                    hit_damage -= self.block
                    self.block = 0

            if hit_damage:
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
                    self.current_hp -= hit_damage
                    health_damage_dealt += hit_damage
                    if is_attack and self.powers.get(PowerId.PLATED_ARMOR):
                        self.powers[PowerId.PLATED_ARMOR] -= 1
                    if self.powers.get(PowerId.CURL_UP):
                        self.block = self.powers.get(PowerId.CURL_UP)
                        del self.powers[PowerId.CURL_UP]

            pa = self.powers.get(PowerId.PLATED_ARMOR,None)
            if pa is not None and pa < 1:
                del self.powers[PowerId.PLATED_ARMOR]

        if self.current_hp < 0:
            health_damage_dealt += self.current_hp
            self.current_hp = 0
        return health_damage_dealt

    # returns a list of powerIds that were applied and not blocked by artifacts
    def add_powers(self, powers: Powers) -> List[PowerId]:
        applied_powers = []
        for power in powers:
            if power in DEBUFFS and self.powers.get(PowerId.ARTIFACT):
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
        return applied_powers

    def get_state_string(self) -> str:
        state: str = f"{self.current_hp},{self.max_hp},{self.block}"
        power_keys = sorted([k.value for k in self.powers.keys()])
        for k in power_keys:
            state += k + str(self.powers[PowerId(k)]) + ","
        return state


class Player(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, energy: int, relics: Relics):
        super().__init__(current_hp, max_hp, block, powers, relics)
        self.energy: int = energy

    def get_state_string(self) -> str:
        return super().get_state_string() + str(self.energy) + ","


class Monster(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, damage: int = 0, hits: int = 0):
        super().__init__(current_hp, max_hp, block, powers)
        self.damage: int = damage
        self.hits: int = hits

    def get_state_string(self) -> str:
        return super().get_state_string() + f"{self.damage},{self.hits},"
