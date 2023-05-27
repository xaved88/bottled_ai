import abc
from typing import List

from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.relics import Relics
from rs.calculator.targets import Player, Monster


class BattleStateInterface(metaclass=abc.ABCMeta):
    player: Player
    hand: List[CardInterface]
    discard_pile: List[CardInterface]
    exhaust_pile: List[CardInterface]
    draw_pile: List[CardInterface]
    monsters: List[Monster]
    relics: Relics
    cards_discarded_this_turn: int

    @abc.abstractmethod
    def draw_cards(self, amount: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def add_cards_to_hand(self, card: CardInterface, amount: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def discard_card(self, card: CardInterface):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def inflict_random_target_damage(self, base_damage: int, hits: int, blockable: bool, vulnerable_modifier: float,
                                     is_attack: bool, min_hp_damage: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def add_random_poison(self, poison_amount: int, hits: int):
        # must be implemented by children
        pass
