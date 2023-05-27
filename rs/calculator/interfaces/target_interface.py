import abc
from typing import List

from rs.calculator.powers import Powers, PowerId
from rs.calculator.relics import Relics

# hp_damage_dealt
InflictDamageSummary = int


class TargetInterface(metaclass=abc.ABCMeta):
    is_player: bool
    current_hp: int
    max_hp: int
    block: int
    powers: Powers
    relics: Relics

    def inflict_damage(self, source, base_damage: int, hits: int, blockable: bool, vulnerable_modifier: float,
                       is_attack: bool, min_hp_damage: int) -> InflictDamageSummary:
        # must be implemented by children
        pass

    def add_powers(self, powers: Powers, relics: Relics, source_powers: Powers) -> List[PowerId]:
        # must be implemented by children
        pass

    def get_state_string(self) -> str:
        # must be implemented by children
        pass

    def heal(self, amount: int):
        # must be implemented by children
        pass
