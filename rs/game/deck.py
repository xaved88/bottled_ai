from typing import List

from rs.game.card import Card, CardType


class Deck:
    def __init__(self, json):
        self.cards: List[Card] = list(map(lambda card: Card(card), json))

    def contains_type(self, type: CardType) -> bool:
        for card in self.cards:
            if card.type == type:
                return True
        return False

    def contains_cards(self, names: List[str]) -> bool:
        for card in self.cards:
            if card.name in names:
                return True
        return False

    def get_card_index(self, id: str) -> int:
        for i in range(len(self.cards)):
            if self.cards[i].id == id:
                return i
        return -1
