from typing import List

from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class TransformHandler(Handler):

    def __init__(self):
        self.preferences: List[str] = [
            'defend',
            'strike',
            'defend+',
            'strike+',
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.game_state()["screen_type"] == "GRID" \
               and state.game_state()["screen_state"]["for_transform"]

    def handle(self, state: GameState) -> List[str]:
        choices = state.get_choice_list()
        choice = len(choices) - 1
        for pref in self.preferences:
            if pref in choices:
                choice = choices.index(pref)
                break
        return ["wait 30", "choose " + str(choice), "wait 30", "proceed", "wait 30"]

