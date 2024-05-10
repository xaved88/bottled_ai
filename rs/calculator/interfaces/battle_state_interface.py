import abc
from typing import List, Tuple

from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.interfaces.memory_items import ResetSchedule, MemoryItem, StanceType
from rs.calculator.interfaces.monster_interface import MonsterInterface
from rs.calculator.interfaces.player import PlayerInterface
from rs.calculator.interfaces.relics import Relics


class BattleStateInterface(metaclass=abc.ABCMeta):
    player: PlayerInterface
    hand: List[CardInterface]
    discard_pile: List[CardInterface]
    exhaust_pile: List[CardInterface]
    draw_pile: List[CardInterface]
    monsters: List[MonsterInterface]
    relics: Relics
    cards_discarded_this_turn: int
    orbs: List[Tuple[OrbId, int]]
    orb_slots: int
    memory_by_card: dict[CardId, dict[ResetSchedule, dict[str, int]]]
    memory_general: dict

    @abc.abstractmethod
    def draw_cards(self, amount: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def spawn_in_hand(self, card: CardInterface, amount: int = 1):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def spawn_in_draw(self, card_to_spawn: CardInterface, amount: int = 1):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def spawn_in_discard(self, card_to_spawn: CardInterface, amount: int = 1):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def discard_card(self, card: CardInterface):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def exhaust_card(self, card: CardInterface, handle_remove: bool = True):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def inflict_non_card_random_target_damage(self, base_damage: int, hits: int, is_orbs: bool = False):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def add_random_poison(self, poison_amount: int, hits: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def add_player_block(self, amount: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def evoke_orbs(self, amount: int = 1, times: int = 1):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def channel_orb(self, orb_id: OrbId, triggered_by_darkness_upgraded: bool = False):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def repeat_card(self, card: CardInterface, target_index: int, repeating_power, power_lost_if_incomplete: bool = True):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def add_memory_by_card(self, card_id: CardId, uuid: str, value_to_add: int):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def get_memory_by_card(self, card_id: CardId, uuid: str) -> int:
        # must be implemented by children
        pass

    @abc.abstractmethod
    def add_memory_value(self, item: MemoryItem, value):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def get_memory_value(self, item: MemoryItem):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def change_stance(self, stance: StanceType):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def get_stance(self) -> StanceType:
        # must be implemented by children
        pass

    @abc.abstractmethod
    def retrieve_from_discard(self, retrieval_target: CardId, just_one=True):
        # must be implemented by children
        pass

    @abc.abstractmethod
    def is_new_turn(self) -> bool:
        # must be implemented by children
        pass

    @abc.abstractmethod
    def is_turn_forced_to_be_over(self) -> bool:
        # must be implemented by children
        pass

    @abc.abstractmethod
    def end_turn(self):
        # must be implemented by children
        pass
