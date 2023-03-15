from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class UpgradeHandler(Handler):

    def __init__(self):
        self.priorities: List[str] = [
            'neutralize',
            'a thousand cuts',
            'accuracy',
            'adrenaline',
            'storm of steel',
            'blade dance',
            'terror',
            'infinite blades',
            'cloak and dagger',
            'die die die',
            'after image',
            'leg sweep',
            'master of strategy',
            'flash of steel',
            'finesse',
            'poisoned stab',
            'sucker punch',
            'escape plan',
            'dagger spray',
            'caltrops',
            'heel hook',
            'survivor',
            'backstab',
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.game_state()["screen_type"] == "GRID" \
               and state.game_state()["screen_state"]["for_upgrade"]

    def handle(self, state: GameState) -> List[str]:
        choice_list = state.game_state()["choice_list"]

        # we have to copy this, otherwise it will modify the list until the bot is rerun
        priorities_working_copy = self.priorities.copy()

        if state.has_relic("Snecko Eye"):
            priorities_working_copy.remove('terror')
            priorities_working_copy.remove('escape plan')
            priorities_working_copy.remove('flash of steel')
            priorities_working_copy.remove('finesse')

        for priority in priorities_working_copy:
            if priority in choice_list:
                if presentation_mode:
                    return [p_delay, "choose " + priority, p_delay_s]
                return ["choose " + priority]
        if presentation_mode:
            return [p_delay, "choose " + choice_list[0], p_delay_s]
        return ["choose " + choice_list[0]]
