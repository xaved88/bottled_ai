from typing import List

from config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class BossRelicHandler(Handler):

    # maybe configure some preferences here
    def __init__(self):
        self.pref = [
            "sozu",
            "philosopher\u0027s stone",
            "ectoplasm",
            "fusion hammer",
            "mark of pain",
            "velvet choker",
            "cursed key",
            "busted crown",  # removed if already have another energy relic or it's act 1
            "coffee dripper",  # removed if already have another energy relic or it's act 1
            "slaver\u0027s collar",
            "runic cube",
            "black blood",
            "calling bell",
            "empty cage",
            "black star",
            "sacred bark",
            "snecko eye"
        ]
        self.energy_relics = [
            "sozu",
            "philosopher\u0027s stone",
            "ectoplasm",
            "velvet choker",
            "cursed key",
            "fusion hammer",
            "mark of pain",
            "runic dome",
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

        if has_energy_relic:
            prefs.remove('mark of pain')

        for p in prefs:
            if p in state.get_choice_list():
                if presentation_mode:
                    return [p_delay, "choose " + str(state.get_choice_list().index(p)), p_delay]
                return ["choose " + str(state.get_choice_list().index(p))]

        if presentation_mode:
            return [p_delay, "skip", p_delay, "proceed", p_delay]
        return ["skip", "proceed"]
