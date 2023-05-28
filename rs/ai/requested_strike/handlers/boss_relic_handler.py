from typing import List

from rs.common.handlers.common_boss_relic_handler import CommonBossRelicHandler
from rs.machine.state import GameState


class BossRelicHandler(CommonBossRelicHandler):

    def __init__(self):
        super().__init__(preferred_relic_list=[
            "sozu",
            "runic dome",
            "philosopher\u0027s stone",
            "ectoplasm",
            "velvet choker",
            "cursed key",
            "fusion hammer",
            "snecko eye",
            "mark of pain",  # removed if already have another energy relic
            "busted crown",  # removed if already have another energy relic or it's act 1
            "coffee dripper",  # removed if already have another energy relic or it's act 1
            "slaver\u0027s collar",
            "runic cube",
            "runic pyramid",
            "black blood",
            "calling bell",
            "empty cage",
            "black star",
            "sacred bark",
        ])

    def adjust_preferences_based_on_game_state(self, prefs: List[str], state: GameState, has_energy_relic: bool):
        act = state.game_state()['act']

        if act == 1 or has_energy_relic:
            prefs.remove('busted crown')
            prefs.remove('coffee dripper')

        if has_energy_relic:
            prefs.remove('mark of pain')
