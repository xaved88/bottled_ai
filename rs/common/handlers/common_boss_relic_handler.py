from typing import List

from config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState

default_preferences = [
    "sozu",
    "runic dome",
    "philosopher\u0027s stone",
    "ectoplasm",
    "velvet choker",
    "cursed key",
    "fusion hammer",
    "snecko eye",
    "mark of pain",
    "busted crown",
    "coffee dripper",
    "slaver\u0027s collar",
    "runic cube",
    "runic pyramid",
    "calling bell",
    "empty cage",
    "black star",
    "sacred bark",
]


class CommonBossRelicHandler(Handler):
    energy_relics = [
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
        "nuclear battery",
    ]

    def __init__(self, preferred_relic_list: List[str] = None):
        if preferred_relic_list is None:
            self.pref = default_preferences
        else:
            self.pref = preferred_relic_list

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.BOSS_REWARD.value and state.has_command(Command.CHOOSE)

    def adjust_preferences_based_on_game_state(self, prefs: List[str], state: GameState, has_energy_relic: bool):
        # can be implemented by the children
        pass

    def handle(self, state: GameState) -> List[str]:
        # we have to copy this, otherwise it will modify the prefs list until the bot is rerun
        prefs = self.pref.copy()

        has_energy_relic = bool(len(list(
            filter(lambda r: r['name'].lower() in self.energy_relics, state.get_relics()))))

        self.adjust_preferences_based_on_game_state(prefs, state, has_energy_relic)

        for p in prefs:
            if p in state.get_choice_list():
                if presentation_mode:
                    return [p_delay, "choose " + str(state.get_choice_list().index(p)), p_delay]
                return ["choose " + str(state.get_choice_list().index(p))]

        if presentation_mode:
            return [p_delay, "skip", p_delay, "proceed", p_delay]
        return ["skip", "proceed"]
