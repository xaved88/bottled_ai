from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class BossRelicHandler(Handler):

    # maybe configure some preferences here
    def __init__(self):
        self.pref = [
            "sozu",
            "runic dome",
            "philosopher\u0027s stone",
            "ectoplasm",
            "velvet choker",
            "cursed key",
            "fusion hammer",
            "snecko eye",
            "mark of pain",  ## removed if already have another energy relic
            "busted crown",  ## removed if already have another energy relic or it's act 1
            "coffee dripper",  ## removed if already have another energy relic or it's act 1
            "slaver\u0027s collar",
            "runic cube",
            "runic pyramid",
            "black blood",
            "calling bell",
            "empty cage",
            "black star",
            "sacred bark",
        ]
        self.energy_relics = [
            "sozu",
            "runic dome",
            "philosopher\u0027s stone",
            "ectoplasm",
            "velvet choker",
            "cursed key",
            "fusion hammer",
            "mark of pain",
            "busted crown",
            "coffee dripper",
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.BOSS_REWARD.value and state.has_command(Command.CHOOSE)

    def handle(self, state: GameState) -> List[str]:
        # we have to copy this, otherwise it will modify the prefs list until the bot is rerun
        prefs = self.pref.copy()

        has_energy_relic = bool(len(list(
            filter(lambda r: r['name'].lower() in self.energy_relics, state.get_relics()))))
        act = state.game_state()['act']

        if act == 1 or has_energy_relic:
            prefs.remove('busted crown')
            prefs.remove('coffee dripper')

        if has_energy_relic:
            prefs.remove('mark of pain')

        for p in prefs:
            if p in state.get_choice_list():
                return ["choose " + str(state.get_choice_list().index(p))]
        return ["skip", "proceed"]
