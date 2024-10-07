from typing import List, Tuple, Optional

from presentation_config import presentation_mode, p_delay
from rs.calculator.helper import pickle_deepcopy
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState

CardDesiredAmount = Tuple[str, int]


class CardPriorityGroup:

    def __init__(self, cards: List[CardDesiredAmount], total_amount: int = 0):
        self.cards: List[CardDesiredAmount] = cards
        # total amount:  0 makes the group never full, only the individual cards are considered.
        self.total_amount: int = total_amount

    def get_priority(self, cards: List[str], pile: dict[str, int]) -> Optional[str]:
        if not self.has_card(cards) or self.is_full(pile):
            return None
        # at this point we know it has a relevant card AND the group isn't full. So find the highest prio card not full.
        for (card, amount) in self.cards:
            if card in cards and pile.get(card, 0) < amount:
                return card
        return None

    def has_card(self, cards: List[str]) -> bool:
        for (card, amount) in self.cards:
            if card in cards:
                return True
        return False

    def is_full(self, pile: dict[str, int]) -> bool:
        if self.total_amount == 0:
            return False
        count = 0
        for (card, amount) in self.cards:
            count += pile.get(card, 0)
        return count >= self.total_amount

    def remove(self, card: str):
        self.cards = [(c, a) for (c, a) in self.cards if card != c]


class CommonGroupedCardRewardHandler(Handler):

    def __init__(self, card_reward_priorities: List[CardPriorityGroup],
                 in_battle_priorities: List[CardPriorityGroup] = None):

        self.card_reward_priorities: List[CardPriorityGroup] = card_reward_priorities
        self.in_battle_priorities: List[
            CardPriorityGroup] = [] if in_battle_priorities is None else in_battle_priorities

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT" or
                    state.game_state()["room_phase"] == "COMBAT")

    def transform_priorities_by_state(self, groups: List[CardPriorityGroup], state: GameState):
        # can be implemented by children
        pass

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        choice_list = state.get_choice_list_upgrade_stripped_from_choice()
        deck_card_list = state.get_deck_card_list_by_name_with_upgrade_stripped()

        priorities = self.in_battle_priorities \
            if state.game_state()["room_phase"] == "COMBAT" else self.card_reward_priorities
        priorities_copy = pickle_deepcopy(priorities)
        self.transform_priorities_by_state(priorities_copy, state)

        for group in priorities_copy:
            choice = group.get_priority(choice_list, deck_card_list)
            if choice is not None:
                if presentation_mode:
                    return HandlerAction(commands=[p_delay, "choose " + str(choice_list.index(choice)), "wait 30"])
                return HandlerAction(commands=["choose " + str(choice_list.index(choice)), "wait 30"])

        # exiting after not finding what we want
        exit_choice = "undecided"

        if 'bowl' in choice_list:
            exit_choice = "choose bowl"
        elif not state.has_command(Command.SKIP):  # Mainly (only?) relevant for the Colorless potion
            exit_choice = "choose 0"
        elif state.game_state()["room_phase"] == "COMBAT":  # E.g. potions
            exit_choice = "skip"
        elif state.game_state()["room_phase"] == "EVENT" and not state.floor() == '0' and not state.has_relic(
                "Tiny House"):
            exit_choice = "skip"  # There isn't a `proceed` available after skipping Neow's card obtain for example.

        if exit_choice != "undecided":
            if presentation_mode:
                return HandlerAction(commands=[p_delay, exit_choice, "wait 30"])
            return HandlerAction(commands=[exit_choice, "wait 30"])

        # Specific case for being with Neow and getting a Tiny House, which unfortunately requires different exiting.
        if state.floor() == "0" and state.has_relic("Tiny House"):
            return HandlerAction(commands=["skip", "proceed"])

        if presentation_mode:
            return HandlerAction(commands=[p_delay, "skip", "proceed"])
        return HandlerAction(commands=["skip", "proceed"])  # So we don't look at the card rewards again.
