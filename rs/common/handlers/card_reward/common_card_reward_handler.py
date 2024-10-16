from typing import List

from presentation_config import presentation_mode, p_delay
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class CommonCardRewardHandler(Handler):

    def __init__(self, cards_desired_for_deck: dict[str, int], cards_desired_from_potions: dict[str, int] = None):
        self.cards_desired_for_deck: dict[str, int] = cards_desired_for_deck
        self.cards_desired_from_potions: dict[str, int] = \
            {} if cards_desired_from_potions is None else cards_desired_from_potions

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT" or
                    state.game_state()["room_phase"] == "COMBAT")

    def transform_desired_cards_map_from_state(self, cards: dict[str, int], state: GameState):
        # can be implemented by children
        pass

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        choice_list = state.get_choice_list_upgrade_stripped_from_choice()
        deck_card_list = state.get_deck_card_list_by_name_with_upgrade_stripped()

        # we have to copy this, otherwise it will modify the list until the bot is rerun
        transformed_desired_cards = self.cards_desired_for_deck.copy()

        # check if we're selecting from a potion
        if state.game_state()["room_phase"] == "COMBAT":
            transformed_desired_cards.update(self.cards_desired_from_potions)

        self.transform_desired_cards_map_from_state(transformed_desired_cards, state)

        for desired_card in transformed_desired_cards:
            if desired_card not in choice_list:
                continue
            if desired_card in deck_card_list \
                    and deck_card_list[desired_card] >= transformed_desired_cards[desired_card]:
                continue
            if presentation_mode:
                return HandlerAction(commands=[p_delay, "choose " + str(choice_list.index(desired_card)), "wait 30"])
            return HandlerAction(commands=["choose " + str(choice_list.index(desired_card)), "wait 30"])

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
