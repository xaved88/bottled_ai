from typing import List

from rs.ai.shivs_and_giggles.comparators.general_comparator import GeneralSilentComparator
from rs.ai.shivs_and_giggles.comparators.gremlin_nob_comparator import GremlinNobSilentComparator
from rs.ai.shivs_and_giggles.comparators.big_fight_comparator import BigFightSilentComparator
from rs.ai.shivs_and_giggles.comparators.three_sentry_comparator import ThreeSentriesSilentComparator
from rs.calculator.executor import get_best_battle_action
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.current_action() == "DiscardAction"

    def handle(self, state: GameState) -> List[str]:
        comparator = GeneralSilentComparator()

        if state.has_monster("Gremlin Nob"):
            comparator = GremlinNobSilentComparator()
        if state.has_monster("Sentry") and len(list(filter(lambda m: not m['is_gone'], state.get_monsters()))) == 3:
            comparator = ThreeSentriesSilentComparator()
        if state.floor() == 33 or state.floor() == 50:
            comparator = BigFightSilentComparator()

        actions = get_best_battle_action(state, comparator, 10_000)
        if actions:
            return actions
        if state.has_command(Command.PLAY):
            return ["end"]
        return []
