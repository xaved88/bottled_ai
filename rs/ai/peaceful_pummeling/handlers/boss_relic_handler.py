from typing import List

from rs.common.handlers.common_boss_relic_handler import CommonBossRelicHandler
from rs.machine.state import GameState


class BossRelicHandler(CommonBossRelicHandler):

    def __init__(self):
        super().__init__(preferred_relic_list=[
            "violet lotus",
            "philosopher\u0027s stone",
            "sozu",
            "ectoplasm",
            "cursed key",
            "snecko eye",
            "fusion hammer",
            "busted crown",  # removed if already have another energy relic or it's act 1
            "coffee dripper",  # removed if already have another energy relic or it's act 1
            "slaver\u0027s collar",
            "runic pyramid",
            "holy water",
            "calling bell",
            "astrolabe",
            "empty cage",
            "black star",
            "tiny house",
            "pandora\u0027s box",
            "sacred bark",
            # "velvet choker", scary
            # "runic dome", scary
        ])

    def adjust_preferences_based_on_game_state(self, prefs: List[str], state: GameState, has_energy_relic: bool):
        act = state.game_state()['act']

        if act == 1 or has_energy_relic:
            prefs.remove('busted crown')
            prefs.remove('coffee dripper')
