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
            "wrist blade",
            "sozu",
            "hovering kite",
            "snecko eye",
            "busted crown",                         # removed if act 1 or already have energy
            "cursed key",
            "philosopher\u0027s stone",
            "calling bell",
            "runic cube",
            "slaver\u0027s collar",
            "fusion hammer",
            "ectoplasm",
            "ring of the serpent",
            "runic pyramid",
            "black star",
            "tiny house",
            "mark of pain",
            "empty cage",
            "sacred bark",
            "coffee dripper",
            # "pandora\u0027s box",
            # "runic dome",
            # "velvet choker",
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

        for p in prefs:
            if p in state.get_choice_list():
                if presentation_mode:
                    return [p_delay, "choose " + str(state.get_choice_list().index(p)), p_delay]
                return ["choose " + str(state.get_choice_list().index(p))]

        if presentation_mode:
            return [p_delay, "skip", p_delay, "proceed", p_delay]
        return ["skip", "proceed"]
