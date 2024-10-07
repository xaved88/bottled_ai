from typing import List

from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonTransformHandler(Handler):

    def __init__(self, preferences: List[str]):
        self.preferences: List[str] = preferences

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.game_state()["screen_type"] == "GRID" \
               and state.game_state()["screen_state"]["for_transform"]

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        choices = state.get_choice_list()
        choice = len(choices) - 1
        for pref in self.preferences:
            if pref in choices:
                choice = choices.index(pref)
                break
        return HandlerAction(commands=["wait 30", "choose " + str(choice), "wait 30", "proceed", "wait 30"])
