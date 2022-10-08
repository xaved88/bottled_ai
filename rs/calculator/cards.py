from enum import Enum

from rs.game.card import CardType


class CardId(Enum):
    STRIKE_R = 'strike_r'
    BASH = 'bash'


class Card:
    id: CardId
    upgrade: int
    cost: int  # energy cost. Maybe -1 for no cost and not playable statuses?
    needs_target: bool  # normally matches to targetType:Enemy, but some do both (iron wave, dash, etc)
    type: CardType  # todo -> maybe we want to extract that enum so this remains decoupled?
