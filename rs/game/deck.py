from typing import List

from rs.calculator.enums.card_id import CardId
from rs.game.card import Card, CardType


class Deck:
    def __init__(self, json):
        self.cards: List[Card] = list(map(lambda card: Card(card), json))

    def contains_type(self, type: CardType) -> bool:
        for card in self.cards:
            if card.type == type:
                return True
        return False

    def contains_curses_of_any_kind(self) -> bool:
        for card in self.cards:
            if card.type == CardType.CURSE:
                return True
        return False

    def contains_curses_we_can_remove(self) -> bool:
        for card in self.cards:
            if card.type == CardType.CURSE and not \
                    card.id.lower() == "curseofthebell" and not \
                    card.id.lower() == "necronomicurse" and not \
                    card.id.lower() == "ascender\u0027sbane":
                return True
        return False

    def contains_cards(self, names: List[str]) -> bool:
        names = [element.lower() for element in names]
        for card in self.cards:
            if card.name.lower() in names:
                return True
        return False

    def contains_card_amount(self, card_name) -> int:
        # note that upgrades include "+" at the end of the name!
        amount = 0
        for c in self.cards:
            if c.name.lower() == card_name:
                amount += 1
        return amount

    def get_card_index(self, id: str) -> int:
        for i in range(len(self.cards)):
            if self.cards[i].id == id:
                return i
        return -1
