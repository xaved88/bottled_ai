from typing import List

from rs.common.handlers.common_boss_relic_handler import CommonBossRelicHandler
from rs.machine.state import GameState


class BossRelicHandler(CommonBossRelicHandler):

    def __init__(self):
        super().__init__(preferred_relic_list=[
            "wrist blade",
            "sozu",
            "hovering kite",
            "busted crown",  # removed if act 1 or already have energy
            "cursed key",
            "philosopher\u0027s stone",
            "snecko eye",
            "calling bell",
            "slaver\u0027s collar",
            "runic pyramid",
            "fusion hammer",
            "astrolabe"
            "ectoplasm",
            "runic cube",
            "ring of the serpent",
            "black star",
            "tiny house",
            "mark of pain",
            "empty cage",
            "sacred bark",
            "coffee dripper",
            # "pandora\u0027s box",
            # "runic dome",
            # "velvet choker",
        ])

    def adjust_preferences_based_on_game_state(self, prefs: List[str], state: GameState, has_energy_relic: bool):
        if state.game_state()['act'] == 1 or has_energy_relic:
            prefs.remove('busted crown')
