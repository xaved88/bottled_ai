from typing import List

from rs.ai.requested_strike.handlers.battle_handler import LegacyBattleHandler
from rs.game.card import CardType
from rs.machine.state import GameState


class GremlinNobHandler(LegacyBattleHandler):

    def __init__(self):
        super().__init__()
        self.allowed_skills = self.always  # the card draw / energy stuff is pretty good, so let's allow it

    def can_handle(self, state: GameState) -> bool:
        return super().can_handle(state) and state.has_monster("Gremlin Nob")

    def handle(self, state: GameState) -> List[str]:
        for card in state.hand.cards:
            if card.type == CardType.SKILL and not self.allowed_skills.count(card.id.lower()):
                card.is_playable = False

        return super().handle(state)
