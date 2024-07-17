from typing import List

from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler
from rs.machine.state import GameState


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'fission',
            'defragment',
            'biased cognition',
            'capacitor',
            'loop',
            'buffer',
            'electrodynamics',
            'zap',
            'genetic algorithm',
            'doom and gloom',
            'sunder',
            'coolheaded',
            'reinforced body',
            'equilibrium',
            'charge battery',
            'hologram',
            'dualcast',
            'bullseye',
            'core surge',
            'skim',
            'streamline',
            'ftl',
            'sweeping beam',
            'compile driver',
            'ball lightning',
            'cold snap',
            'glacier',
            'chill',
            'autoshields',
            'glacier',
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
