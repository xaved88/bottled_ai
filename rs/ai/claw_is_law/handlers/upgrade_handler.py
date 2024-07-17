from typing import List

from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler
from rs.machine.state import GameState


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'reprogram',
            'fission',
            'streamline',
            'hyperbeam',
            'all for one',
            'go for the eyes',
            'beam cell',
            'reinforced body',
            'scrape',
            'reboot',
            'steam barrier',
            'equilibrium'
            'ftl',
            'ball lightning',
            'claw',
            'zap',
            'boot sequence',
        ])

    def transform_priorities_based_on_game_state(self, priorities: List[str], state: GameState):
        remove_if_snecko = [
            'creative ai',
            'dualcast',
            'double energy',
            'fusion',
            'recursion',
            'recycle',
            'white noise',
            'zap',
        ]
        safe_remove_if_snecko = []

        if state.has_relic("Snecko Eye"):
            for c in remove_if_snecko:
                if c in priorities:
                    safe_remove_if_snecko.append(c)
            for d in safe_remove_if_snecko:
                priorities.remove(d)
