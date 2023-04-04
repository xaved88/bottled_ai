from typing import List

from rs.ai.shivs_and_giggles.comparators.general_comparator import GeneralSilentComparator
from rs.calculator.executor import get_best_battle_action
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.current_action() == "DiscardAction"

    def handle(self, state: GameState) -> List[str]:
        actions = get_best_battle_action(state, GeneralSilentComparator(), 10_000)
        if actions:
            return actions
        if state.has_command(Command.PLAY):
            return ["end"]
        return []
