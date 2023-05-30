from typing import List

from rs.common.handlers.common_boss_relic_handler import CommonBossRelicHandler
from rs.machine.state import GameState


class BossRelicHandler(CommonBossRelicHandler):

    def __init__(self):
        super().__init__(preferred_relic_list=[
            "nuclear battery",
            "sozu",
            # "runic dome", we will love this, but only once we make custom comparators for it.
            "velvet choker",
            "cursed key",
            "philosopher\u0027s stone",
            "fusion hammer",
            "ectoplasm",  # conditionally removed
            "runic pyramid",
            "busted crown",  # conditionally removed
            "coffee dripper",  # conditionally removed
            "slaver\u0027s collar",
            "inserter",
            "empty cage",
            "black star",
            "calling bell",
            "sacred bark",
            "frozen core",
        ])

    def adjust_preferences_based_on_game_state(self, prefs: List[str], state: GameState, has_energy_relic: bool):
        act = state.game_state()['act']

        if act == 1 or has_energy_relic:
            prefs.remove('busted crown')
            prefs.remove('coffee dripper')
            prefs.remove('ectoplasm')
