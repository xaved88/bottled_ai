from config import presentation_mode, p_delay
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonScryHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.current_action() == 'ScryAction'

    def handle(self, state: GameState) -> HandlerAction:
        if presentation_mode:
            return HandlerAction(commands=[p_delay, 'confirm'])
        return HandlerAction(commands=[p_delay, 'confirm'])
