from typing import List

from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class DefaultEndHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.END)

    def handle(self, state: GameState) -> List[str]:
        return ["end"]
