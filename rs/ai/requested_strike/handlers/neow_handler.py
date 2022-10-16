from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class NeowHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.EVENT.value \
               and state.has_command(Command.CHOOSE) \
               and state.game_state()['screen_state']['event_id'] == "Neow Event"

    def handle(self, state: GameState) -> List[str]:
        if "leave" in state.get_choice_list():
            return ["choose 0"]
        # choose 3 here for relic swap
        return ["choose 0"]
