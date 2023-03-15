from typing import List

from rs.ai.requested_strike.comparators.general_comparator import GeneralComparator
from rs.calculator.executor import get_best_battle_action
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.has_action("DiscardAction")

    def handle(self, state: GameState) -> List[str]:
        return get_best_battle_action(state, GeneralComparator())
