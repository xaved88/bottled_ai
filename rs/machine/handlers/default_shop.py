from rs.game.screen_type import ScreenType
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class DefaultShopHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.SHOP_ROOM.value

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        return HandlerAction(commands=["proceed"])
