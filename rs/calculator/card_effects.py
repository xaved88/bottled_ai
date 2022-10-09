from enum import Enum
from typing import List, Callable

from rs.calculator.card_effect_custom_hooks import CardEffectCustomHook, dropkick_custom_hook
from rs.calculator.cards import Card, CardId
from rs.calculator.powers import Powers, PowerId


class TargetType(Enum):
    NONE = 0
    SELF = 1
    MONSTER = 2
    ALL_MONSTERS = 3


class CardEffects:
    def __init__(
            self,
            damage: int = 0,
            hits: int = 0,
            blockable: bool = True,
            block: int = 0,
            target: TargetType = TargetType.SELF,
            applies_powers=None,
            energy_gain: int = 0,
            custom_hooks: List[CardEffectCustomHook] = None
    ):
        self.damage: int = damage
        self.hits: int = hits
        self.blockable: bool = blockable
        self.block: int = block
        self.target: TargetType = target
        self.applies_powers: Powers = dict() if applies_powers is None else applies_powers
        self.energy_gain: int = energy_gain
        self.custom_hooks: List[CardEffectCustomHook] = [] if custom_hooks is None else custom_hooks


def get_card_effects(card: Card, player_powers: Powers, draw_pile: List[Card], discard_pile: List[Card],
                     hand: List[Card]) -> List[CardEffects]:
    if card.id == CardId.STRIKE_R:
        return [CardEffects(damage=6 if not card.upgrade else 9, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.DEFEND_R:
        return [CardEffects(block=5 if not card.upgrade else 8, target=TargetType.SELF)]
    if card.id == CardId.BASH:
        return [CardEffects(damage=8 if not card.upgrade else 10, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.VULNERABLE: 2} if not card.upgrade else {PowerId.VULNERABLE: 3})]
    if card.id == CardId.ANGER:
        return [CardEffects(damage=6 if not card.upgrade else 8, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.CLEAVE:
        return [CardEffects(damage=8 if not card.upgrade else 11, hits=1, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.CLOTHESLINE:
        return [CardEffects(damage=12 if not card.upgrade else 14, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.WEAK: 2} if not card.upgrade else {PowerId.WEAK: 3})]
    if card.id == CardId.HEAVY_BLADE:
        str_bonus = player_powers.get(PowerId.STRENGTH, 0)
        damage = 12 + (str_bonus * 2 if not card.upgrade else str_bonus * 4)
        return [CardEffects(damage=damage, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.IRON_WAVE:
        amount = 5 if not card.upgrade else 7
        return [CardEffects(damage=amount, hits=1, block=amount, target=TargetType.MONSTER)]
    if card.id == CardId.PERFECTED_STRIKE:
        strike_amount = len([1 for c in discard_pile + draw_pile + hand if "strike" in c.id.value])
        damage = 6 + strike_amount * (2 if not card.upgrade else 3)
        return [CardEffects(damage=damage, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.POMMEL_STRIKE:
        return [CardEffects(damage=9 if not card.upgrade else 10, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.SHRUG_IT_OFF:
        return [CardEffects(block=8 if not card.upgrade else 11, target=TargetType.SELF)]
    if card.id == CardId.THUNDERCLAP:
        return [CardEffects(damage=4 if not card.upgrade else 6, hits=1, target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.VULNERABLE: 1})]
    if card.id == CardId.TWIN_STRIKE:
        return [CardEffects(damage=5 if not card.upgrade else 7, hits=2, target=TargetType.MONSTER)]
    if card.id == CardId.BLOOD_FOR_BLOOD:
        return [CardEffects(damage=18 if not card.upgrade else 22, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.BLOODLETTING:
        return [CardEffects(energy_gain=2 if not card.upgrade else 3, damage=3, hits=1, blockable=False,
                            target=TargetType.SELF)]
    if card.id == CardId.CARNAGE:
        return [CardEffects(damage=20 if not card.upgrade else 28, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.UPPERCUT:
        powers = {PowerId.WEAK: 1, PowerId.VULNERABLE: 1} if not card.upgrade \
            else {PowerId.WEAK: 2, PowerId.VULNERABLE: 2}
        return [CardEffects(damage=13, hits=1, target=TargetType.MONSTER, applies_powers=powers)]
    if card.id == CardId.DISARM:
        return [CardEffects(target=TargetType.MONSTER,
                            applies_powers={PowerId.STRENGTH: -2 if not card.upgrade else 3})]
    if card.id == CardId.DROPKICK:
        return [CardEffects(damage=5 if not card.upgrade else 8, hits=1, target=TargetType.MONSTER,
                            custom_hooks=[dropkick_custom_hook])]
    if card.id == CardId.ENTRENCH:
        return [CardEffects(target=TargetType.SELF, custom_hooks=[dropkick_custom_hook])]
    if card.id == CardId.FLAME_BARRIER:
        return [CardEffects(target=TargetType.SELF, block=12 if not card.upgrade else 16,
                            applies_powers={PowerId.FLAME_BARRIER: 4 if not card.upgrade else 6})]
    if card.id == CardId.GHOSTLY_ARMOR:
        return [CardEffects(target=TargetType.SELF, block=10 if not card.upgrade else 13)]
    if card.id == CardId.HEMOKINESIS:
        return [CardEffects(damage=15 if not card.upgrade else 20, hits=1, target=TargetType.MONSTER),
                CardEffects(damage=2, hits=1, blockable=False, target=TargetType.SELF)]
    if card.id == CardId.INFLAME:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STRENGTH: 2 if not card.upgrade else 3})]
    if card.id == CardId.INTIMIDATE:
        return [CardEffects(target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.WEAK: 1 if not card.upgrade else 2})]
    if card.id == CardId.PUMMEL:
        return [CardEffects(damage=2, hits=4 if not card.upgrade else 5, target=TargetType.MONSTER)]
    if card.id == CardId.SEEING_RED:
        return [CardEffects(energy_gain=2, target=TargetType.SELF)]
    if card.id == CardId.SHOCKWAVE:
        amount = 3 if not card.upgrade else 5
        return [CardEffects(target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.WEAK: amount, PowerId.VULNERABLE: amount})]

    # default case, todo maybe some logging or?
    return [CardEffects()]
