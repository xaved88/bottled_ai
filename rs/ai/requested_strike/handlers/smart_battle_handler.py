from typing import List

from rs.calculator.executor import get_best_battle_path, default_path_comparator, aggressive_path_comparator
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) and state.game_state()['room_type'] == "MonsterRoom"

    def handle(self, state: GameState) -> List[str]:
        report = get_best_battle_path(state, default_path_comparator)

        if report.path.plays:
            next_move = report.path.plays[0]
            if next_move[1] == -1:
                return [f"play {next_move[0] + 1}"]
            return [f"play {next_move[0] + 1} {next_move[1]}"]
        return []  # when optimized it should be end here, but for now let's just default back to the other battle handler
