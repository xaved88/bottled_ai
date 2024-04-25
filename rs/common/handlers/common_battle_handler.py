from dataclasses import dataclass, field

from rs.calculator.executor import get_best_battle_action
from rs.calculator.interfaces.comparator_interface import ComparatorInterface
from rs.common.comparators.big_fight_comparator import BigFightComparator
from rs.common.comparators.common_general_comparator import CommonGeneralComparator
from rs.common.comparators.gremlin_nob_comparator import GremlinNobComparator
from rs.common.comparators.three_sentry_comparator import ThreeSentriesComparator
from rs.common.comparators.waiting_lagavulin_comparator import WaitingLagavulinComparator
from rs.game.card import CardType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


@dataclass
class BattleHandlerConfig:
    big_fight_floors: list[int] = field(default_factory=lambda: [33, 50])
    big_fight_comparator: ComparatorInterface = BigFightComparator
    gremlin_nob_comparator: ComparatorInterface = GremlinNobComparator
    three_sentries_comparator: ComparatorInterface = ThreeSentriesComparator
    waiting_lagavulin_comparator: ComparatorInterface = WaitingLagavulinComparator
    general_comparator: ComparatorInterface = CommonGeneralComparator


class CommonBattleHandler(Handler):

    def __init__(self, config: BattleHandlerConfig = BattleHandlerConfig(), max_path_count: int = 11_000):
        self.config: BattleHandlerConfig = config
        self.max_path_count: int = max_path_count

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.current_action() == "DiscardAction"

    def select_comparator(self, state: GameState) -> ComparatorInterface:
        big_fight = state.floor() in self.config.big_fight_floors

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
            return self.config.big_fight_comparator()
        elif gremlin_nob_is_present:
            return self.config.gremlin_nob_comparator()
        elif three_sentries_are_alive:
            return self.config.three_sentries_comparator()
        elif lagavulin_is_sleeping and lagavulin_is_worth_delaying:
            return self.config.waiting_lagavulin_comparator()
        return self.config.general_comparator()

    def handle(self, state: GameState) -> HandlerAction:
        actions = get_best_battle_action(state, self.select_comparator(state), self.max_path_count)
        if actions:
            return actions
        if state.has_command(Command.END):
            return HandlerAction(commands=["end"], memory_book=None)
        return HandlerAction(commands=[], memory_book=None)
