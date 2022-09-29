from typing import List

from rs.ai.requested_strike.handlers.battle_handler import BattleHandler
from rs.game.card import CardType
from rs.machine.state import GameState


class SentriesHandler(BattleHandler):

    def __init__(self):
        super().__init__()

    def can_handle(self, state: GameState) -> bool:
        return super().can_handle(state) \
               and state.has_monster("Sentry") \
               and len(list(filter(lambda m: not m['is_gone'], state.get_monsters()))) == 3

    def should_yolo(self) -> bool:
        return True

    def get_target(self, monsters: List[dict]) -> int:
        if monsters[0]['current_hp'] <= monsters[2]['current_hp']:
            return 0
        else:
            return 2
