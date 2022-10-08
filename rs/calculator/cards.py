from enum import Enum

from rs.game.card import CardType


class CardId(Enum):
    STRIKE_R = 'strike_r'
    DEFEND_R = 'defend_r'
    BASH = 'bash'
    ANGER = 'anger'
    CLEAVE = 'cleave'
    CLOTHESLINE = 'clothesline'
    HEAVY_BLADE = 'heavy blade'
    IRON_WAVE = 'iron wave'
    PERFECTED_STRIKE = 'perfected strike'
    POMMEL_STRIKE = 'pommel strike'
    SHRUG_IT_OFF = 'shrug it off'
    THUNDERCLAP = 'thunderclap'
    TWIN_STRIKE = 'twin strike'


class Card:
    def __init__(self, id: CardId, upgrade: int, cost: int, needs_target: bool, card_type: CardType):
        self.id: CardId = id
        self.upgrade: int = upgrade
        self.cost: int = cost  # energy cost. Maybe -1 for no cost and not playable statuses?
        self.needs_target: bool = needs_target
        self.type: CardType = card_type  # todo -> maybe we want to extract that enum so this remains decoupled?


def get_card(card_id: CardId, cost: int = None, upgrade: int = 0) -> Card:
    if card_id == CardId.STRIKE_R:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.DEFEND_R:
        return Card(card_id, upgrade, 1 if cost is None else cost, False, CardType.SKILL)
    if card_id == CardId.BASH:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.ANGER:
        return Card(card_id, upgrade, 0 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CLEAVE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.CLOTHESLINE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.HEAVY_BLADE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.IRON_WAVE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.PERFECTED_STRIKE:
        return Card(card_id, upgrade, 2 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.POMMEL_STRIKE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.SHRUG_IT_OFF:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.SKILL)
    if card_id == CardId.THUNDERCLAP:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    if card_id == CardId.TWIN_STRIKE:
        return Card(card_id, upgrade, 1 if cost is None else cost, True, CardType.ATTACK)
    # TODO -> logging or throw error or something if it gets here?
