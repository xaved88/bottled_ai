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
               and len(self.get_choices(state)) > -1

    def handle(self, state: GameState) -> List[str]:
        commands = []
        amount = 1
        if 'screen_state' in state.game_state() and 'num_cards' in state.game_state()['screen_state']:
            amount = state.game_state()['screen_state']['num_cards']
        for c in self.get_choices(state)[0:amount]:
            commands.append("choose " + str(c))
            commands.append("wait 30")
        return commands

    def get_choices(self, state: GameState) -> List[int]:
        choice_list = state.get_choice_list()
        choices = []
        for pref in self.preferences:
            for i in range(len(choice_list)):
                if pref == choice_list[i]:
                    choices.append(i)

        for i in range(len(choice_list)):
            if i not in choices:
                choices.append(i)

        return choices
