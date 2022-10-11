import math

from rs.calculator.powers import PowerId, Powers, DEBUFFS


class Target:
    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers):
        self.current_hp: int = current_hp
        self.max_hp: int = max_hp
        self.block: int = block
        self.powers: Powers = powers

    def inflict_damage(self, base_damage: int, hits: int, blockable: bool = True, vulnerable_modifier: float = 1.5):
        damage = base_damage
        if self.powers.get(PowerId.VULNERABLE):
            damage = math.floor(damage * vulnerable_modifier)
        if self.powers.get(PowerId.PLATED_ARMOR):
            temp_block = self.block
            reduction = 0
            for i in range(hits):
                temp_block -= damage
                if temp_block < 0:
                    reduction += 1
            if reduction:
                new_value = self.powers.get(PowerId.PLATED_ARMOR) - reduction
                if new_value:
                    self.powers[PowerId.PLATED_ARMOR] = new_value
                else:
                    del self.powers[PowerId.PLATED_ARMOR]
        damage *= hits
        if blockable:
            self.block -= damage
            if self.block < 0:
                self.current_hp += self.block
                if self.powers.get(PowerId.CURL_UP):
                    self.block = self.powers.get(PowerId.CURL_UP)
                    del self.powers[PowerId.CURL_UP]
                else:
                    self.block = 0
        else:
            self.current_hp -= damage

        self.current_hp = max(0, self.current_hp)

    def add_powers(self, powers: Powers):
        for power in powers:
            if power in DEBUFFS and self.powers.get(PowerId.ARTIFACT):
                if self.powers[PowerId.ARTIFACT] == 1:
                    del self.powers[PowerId.ARTIFACT]
                else:
                    self.powers[PowerId.ARTIFACT] -= 1
                continue
            if power in self.powers:
                self.powers[power] += powers[power]
            else:
                self.powers[power] = powers[power]

    def get_state_string(self) -> str:
        state: str = f"{self.current_hp},{self.max_hp},{self.block}"
        power_keys = sorted([k.value for k in self.powers.keys()])
        for k in power_keys:
            state += k + str(self.powers[PowerId(k)]) + ","
        return state


class Player(Target):

    def __init__(self, current_hp: int, max_hp: int, block: int, powers: Powers, energy: int):
        super().__init__(current_hp, max_hp, block, powers)
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
