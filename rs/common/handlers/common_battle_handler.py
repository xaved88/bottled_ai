from typing import List

from rs.calculator.interfaces.comparator_interface import ComparatorInterface
from rs.calculator.executor import get_best_battle_action
from rs.common.comparators.common_general_comparator import CommonGeneralComparator
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CommonBattleHandler(Handler):

    def __init__(self, max_path_count: int = 11_000):
        self.max_path_count: int = max_path_count

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.current_action() == "DiscardAction"

    def select_comparator(self, state: GameState) -> ComparatorInterface:
        # can be overridden by children for extra logic.
        return CommonGeneralComparator()

    def handle(self, state: GameState) -> List[str]:
        actions = get_best_battle_action(state, self.select_comparator(state), self.max_path_count)
        if actions:
            return actions
        if state.has_command(Command.PLAY):
            return ["end"]
        return []
