from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class UpgradeHandler(Handler):

    def __init__(self):
        self.upgrade_priorities: List[str] = [
            'neutralize',           # removed if we have snecko eye
            'a thousand cuts',
            'tools of the trade',   # removed if we have snecko eye
            'accuracy',
            'adrenaline',
            'storm of steel',
            'blade dance',
            'prepared',
            'terror',               # removed if we have snecko eye
            'infinite blades',
            'cloak and dagger',
            'die die die',
            'after image',
            'eviscerate',
            'leg sweep',
            'master of strategy',
            'flash of steel',       # removed if we have snecko eye
            'finesse',              # removed if we have snecko eye
            'poisoned stab',
            'sneaky strike',
            'sucker punch',
            'escape plan',          # removed if we have snecko eye
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
        upgrade_priorities_working_copy = self.upgrade_priorities.copy()

        if state.has_relic("Snecko Eye"):
            upgrade_priorities_working_copy.remove('neutralize')
            upgrade_priorities_working_copy.remove('tools of the trade')
            upgrade_priorities_working_copy.remove('terror')
            upgrade_priorities_working_copy.remove('escape plan')
            upgrade_priorities_working_copy.remove('flash of steel')
            upgrade_priorities_working_copy.remove('finesse')

        for priority in upgrade_priorities_working_copy:
            if priority in choice_list:
                if presentation_mode:
                    return [p_delay, "choose " + priority, p_delay_s]
                return ["choose " + priority]
        if presentation_mode:
            return [p_delay, "choose " + choice_list[0], p_delay_s]
        return ["choose " + choice_list[0]]
