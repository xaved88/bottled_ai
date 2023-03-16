from typing import List

from rs.ai.requested_strike.comparators.general_comparator import GeneralComparator
from rs.calculator.executor import get_best_battle_path
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY)

    def handle(self, state: GameState) -> List[str]:
        path = get_best_battle_path(state, GeneralComparator())

        if path.plays:
            next_move = path.plays[0]
            if next_move[1] == -1:
                return [f"play {next_move[0] + 1}"]
            return [f"play {next_move[0] + 1} {next_move[1]}"]
        return []  # when optimized it should be end here, but for now let's just default back to the other battle handler
