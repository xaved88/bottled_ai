from typing import List

from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler
from rs.machine.state import GameState


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'perfected strike',
            'bash',
            'shockwave',
            'uppercut',  # Not in pickup list at time of writing
            'battle trance',
            'offering',
            'blind',
            'seeing red',  # Not in pickup list at time of writing
            'dropkick',
            'flame barrier',
            'twin strike',
            'pommel strike',
            'handofgreed',
            'thunderclap',
            'shrug it off',
            'impervious',
            'ghostly armor',
            'master of strategy',
            'flash of steel',
            'trip',
            'dark shackles',
            'swift strike',
            'dramatic entrance',
            'finesse',
        ])

    def transform_priorities_based_on_game_state(self, priorities: List[str], state: GameState):
        remove_if_snecko = [
            'barricade',
            'blood for blood',
            'body slam',
            'corruption',
            'dark embrace',
            'entrench',
            'exhume',
            'havoc',
            'infernal blade',
            'seeing red',
        ]
        safe_remove_if_snecko = []

        if state.has_relic("Snecko Eye"):
            for c in remove_if_snecko:
                if c in priorities:
                    safe_remove_if_snecko.append(c)
            for d in safe_remove_if_snecko:
                priorities.remove(d)