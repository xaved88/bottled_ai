from enum import Enum
from typing import List

from rs.calculator.enums.orb_id import OrbId
from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.interfaces.memory_items import StanceType
from rs.calculator.interfaces.powers import Powers
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from rs.calculator.interfaces.card_effect_hooks_interface import CardEffectCustomHook, CardEffectCustomHookWithCard


class TargetType(Enum):
    NONE = 0
    SELF = 1
    MONSTER = 2
    ALL_MONSTERS = 3
    RANDOM = 4


class CardEffectsInterface:
    damage: int
    hits: int
    blockable: bool
    block: int
    block_times: int
    applies_powers: Powers
    target: TargetType
    energy_gain: int
    draw: int
    pre_hooks: List['CardEffectCustomHook']
    post_hooks: List['CardEffectCustomHook']
    post_others_discarded_hooks: List['CardEffectCustomHookWithCard']
    post_self_discarded_hooks: List['CardEffectCustomHook']
    end_turn_hooks: List['CardEffectCustomHook']
    heal: int
    amount_to_discard: int
    amount_to_exhaust: int
    spawn_cards_in_hand: [CardInterface, int]
    spawn_cards_in_draw: [CardInterface, int]
    spawn_cards_in_discard: [CardInterface, int]
    channel_orbs: List[OrbId]
    retains: bool
    sets_stance: StanceType
    amount_to_scry: int
