from rs.ai.requested_strike.handlers.battle_handler import BattleHandler
from rs.machine.state import GameState


class TransientHandler(BattleHandler):

    def __init__(self):
        super().__init__()

    def can_handle(self, state: GameState) -> bool:
        return super().can_handle(state) \
               and state.has_monster("Transient") \
               and len(list(filter(lambda m: not m['is_gone'], state.get_monsters()))) == 1

    def should_yolo(self) -> bool:
        return True
