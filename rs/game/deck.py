from typing import List

from rs.game.card import Card


class Deck:
    def __init__(self, json):
        self.cards: List[Card] = list(map(lambda card: Card(card), json))
