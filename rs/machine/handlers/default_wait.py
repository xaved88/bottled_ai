from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class DefaultWaitHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.WAIT)

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        return HandlerAction(commands=["wait 30"])
