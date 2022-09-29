from typing import List

from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class PurgeHandler(Handler):

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
               and state.game_state()["screen_state"]["for_purge"] \
               and self.get_choice(state.game_state()) > -1

    def handle(self, state: GameState) -> List[str]:
        return ["wait 30", "choose " + str(self.get_choice(state)), "wait 30", "proceed", "wait 30"]

    def get_choice(self, state: GameState) -> int:
        choices = state.get_choice_list()
        for pref in self.preferences:
            if pref in choices:
                return choices.index(pref)
        return -1
