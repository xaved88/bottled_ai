from typing import List

from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class DefaultWaitHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.WAIT)

    def handle(self, state: GameState) -> str:
        return "wait 30"
