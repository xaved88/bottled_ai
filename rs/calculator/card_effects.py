from enum import Enum
from typing import List

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
            applies_powers=None
    ):
        if applies_powers is None:
            applies_powers = dict()
        self.damage = damage
        self.hits = hits
        self.blockable = blockable
        self.block = block
        self.target = target
        # applies to the targets? Are there ever things that do _more_ than that?
        self.applies_powers: Powers = applies_powers
        # special effect lambdas maybe we can add in here at some point but not for now.


def strike_ce(card: Card) -> List[CardEffects]:
    damage = 6 if not card.upgrade else 9
    return [CardEffects(damage=damage, hits=1, target=TargetType.MONSTER)]


def bash_ce(card: Card) -> List[CardEffects]:
    damage = 8 if not card.upgrade else 10
    powers = {PowerId.VULNERABLE: 2} if not card.upgrade else {PowerId.VULNERABLE: 3}
    return [CardEffects(damage=damage, hits=1, target=TargetType.MONSTER, applies_powers=powers)]


def get_card_effects(card: Card) -> List[CardEffects]:
    if card.id == CardId.STRIKE_R:
        return strike_ce(card)
    if card.id == CardId.BASH:
        return bash_ce(card)
    # default case, todo maybe some logging or?
    return [CardEffects()]
