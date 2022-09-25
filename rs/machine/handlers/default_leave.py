from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class DefaultLeaveHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.LEAVE)

    def handle(self, state: GameState) -> str:
        return "return"
