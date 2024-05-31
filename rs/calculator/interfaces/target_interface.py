import abc
from collections import namedtuple
from typing import List

from rs.calculator.enums.card_id import CardId
from rs.calculator.interfaces.powers import Powers
from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.relics import Relics

# hp_damage_dealt
InflictDamageSummary = int


class TargetInterface(metaclass=abc.ABCMeta):
    is_player: bool
    current_hp: int
    max_hp: int
    block: int
    powers: Powers
    relics: Relics

    def inflict_damage(self, source, base_damage: int, hits: int, blockable: bool = True,
                       vulnerable_modifier: float = 1.5, is_attack: bool = True,
                       min_hp_damage: int = 1, is_orbs: bool = False, card_id: CardId = None) -> InflictDamageSummary:
        # must be implemented by children
        pass

    def add_powers(self, powers: Powers, relics: Relics, source_powers: Powers) -> List[PowerId]:
        # must be implemented by children
        pass

    def get_state_string(self) -> str:
        # must be implemented by children
        pass

    def heal(self, amount: int, is_player: bool, relics: Relics):
        # must be implemented by children
        pass
