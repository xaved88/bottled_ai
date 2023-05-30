from typing import List

from rs.calculator.interfaces.comparator_interface import ComparatorInterface
from rs.calculator.executor import get_best_battle_action
from rs.common.comparators.big_fight_comparator import BigFightComparator
from rs.common.comparators.common_general_comparator import CommonGeneralComparator
from rs.common.comparators.gremlin_nob_comparator import GremlinNobComparator
from rs.common.comparators.three_sentry_comparator import ThreeSentriesComparator
from rs.common.comparators.waiting_lagavulin_comparator import WaitingLagavulinComparator
from rs.game.card import CardType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CommonBattleHandler(Handler):

    def __init__(self, max_path_count: int = 11_000):
        self.max_path_count: int = max_path_count

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.current_action() == "DiscardAction"

    def select_comparator(self, state: GameState) -> ComparatorInterface:
        big_fight = state.floor() == 33 or state.floor() == 50

        gremlin_nob_is_present = state.has_monster("Gremlin Nob")

        three_sentries_are_alive = state.has_monster("Sentry") \
                                   and len(list(filter(lambda m: not m['is_gone'], state.get_monsters()))) == 3

        lagavulin_is_sleeping = state.has_monster("Lagavulin") \
                                and state.combat_state()['turn'] <= 2 \
                                and not state.game_state()['room_type'] == "EventRoom"

        lagavulin_is_worth_delaying = state.deck.contains_type(CardType.POWER) \
                                      or state.deck.contains_cards(["Terror", "Terror+"]) \
                                      or state.has_relic("Warped Tongs") \
                                      or state.has_relic("Ice Cream")

        if big_fight:
            return BigFightComparator()
        elif gremlin_nob_is_present:
            return GremlinNobComparator()
        elif three_sentries_are_alive:
            return ThreeSentriesComparator()
        elif lagavulin_is_sleeping and lagavulin_is_worth_delaying:
            return WaitingLagavulinComparator()
        return CommonGeneralComparator()

    def handle(self, state: GameState) -> List[str]:
        actions = get_best_battle_action(state, self.select_comparator(state), self.max_path_count)
        if actions:
            return actions
        if state.has_command(Command.PLAY):
            return ["end"]
        return []
