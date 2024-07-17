from typing import List

from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler
from rs.machine.state import GameState


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'neutralize',
            'accuracy',
            'footwork',
            'adrenaline',
            'tools of the trade',  # removed if we have snecko eye
            'blade dance',
            'prepared',
            'terror',  # removed if we have snecko eye
            'cloak and dagger',
            'storm of steel',
            'die die die',
            'eviscerate',
            'leg sweep',
            'master of strategy',
            'flash of steel',  # removed if we have snecko eye
            'finesse',  # removed if we have snecko eye
            'sneaky strike',
            'dagger spray',
            'sucker punch',
            'dash',
            'escape plan',  # removed if we have snecko eye
            'caltrops',
            'survivor',
            'backstab',
            'infinite blades',
            'after image',
        ]),

    def transform_priorities_based_on_game_state(self, priorities: List[str], state: GameState):
        remove_if_snecko = [
            'alchemize',
            'bullet time',
            'deflect',
            'distraction',
            'endless agony',
            'envenom',
            'escape plan',
            'flash of steel',
            'finesse',
            'nightmare',
            'phantasmal killer',
            'setup',
            'slice',
            'terror',
            'tools of the trade',
        ]
        safe_remove_if_snecko = []

        if state.has_relic("Snecko Eye"):
            for c in remove_if_snecko:
                if c in priorities:
                    safe_remove_if_snecko.append(c)
            for d in safe_remove_if_snecko:
                priorities.remove(d)
