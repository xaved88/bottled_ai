from typing import List

from rs.ai.shivs_and_giggles.comparators.general_comparator import GeneralSilentComparator
from rs.ai.shivs_and_giggles.comparators.gremlin_nob_comparator import GremlinNobSilentComparator
from rs.ai.shivs_and_giggles.comparators.big_fight_comparator import BigFightSilentComparator
from rs.ai.shivs_and_giggles.comparators.waiting_lagavulin_comparator import WaitingLagavulinSilentComparator
from rs.ai.shivs_and_giggles.comparators.three_sentry_comparator import ThreeSentriesSilentComparator
from rs.calculator.executor import get_best_battle_action
from rs.game.card import CardType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class SmartBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY) or state.current_action() == "DiscardAction"

    def handle(self, state: GameState) -> List[str]:

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
            comparator = BigFightSilentComparator()
        elif gremlin_nob_is_present:
            comparator = GremlinNobSilentComparator()
        elif three_sentries_are_alive:
            comparator = ThreeSentriesSilentComparator()
        elif lagavulin_is_sleeping and lagavulin_is_worth_delaying:
            comparator = WaitingLagavulinSilentComparator()
        else:
            comparator = GeneralSilentComparator()

        actions = get_best_battle_action(state, comparator, 11_000)
        if actions:
            return actions
        if state.has_command(Command.PLAY):
            return ["end"]
        return []
