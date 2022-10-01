from typing import List

from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class AstrolabeHandler(Handler):

    def __init__(self):
        self.preferences: List[str] = [
            'defend',
            'strike',
            'defend+',
            'strike+',
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.game_state()['room_type'] == "TreasureRoomBoss" \
               and state.has_command(Command.CHOOSE) \
               and 'screen_state' in state.game_state() \
               and 'num_cards' in state.game_state()['screen_state'] \
               and state.game_state()['screen_state']['num_cards'] == 3

    def handle(self, state: GameState) -> List[str]:
        # basically use remove but pick the best 3?
        choice_list = state.get_choice_list()
        choices = []
        for pref in self.preferences:
            for i in range(len(choice_list)):
                if pref == choice_list[i]:
                    choices.append(i)

        for i in range(len(choice_list)):
            if i not in choices:
                choices.append(i)

        commands = []
        for c in choices[0:3]:
            commands.append("choose " + str(c))
            commands.append("wait 30")
        return commands
