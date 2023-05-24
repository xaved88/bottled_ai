from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CardRewardHandler(Handler):

    def __init__(self):
        self.cards_desired_for_deck: dict[str, int] = {
            'accuracy': 4,
            'after image': 2,
            'tools of the trade': 1,    # removed if we have snecko eye
            'terror': 2,
            'adrenaline': 2,
            'storm of steel': 2,
            'die die die': 2,
            'blade dance': 4,
            'infinite blades': 2,
            'eviscerate': 1,
            'leg sweep': 1,
            'cloak and dagger': 3,
            'sneaky strike': 2,
            'sucker punch': 1,
            'dagger spray': 2,
            'dash': 1,
            'escape plan': 2,           # removed if we have snecko eye
            'dagger throw': 1,
            'footwork': 1,
            'prepared': 1,              # removed if we have snecko eye
            'unload': 1,
            'backstab': 1,              # removed if we have snecko eye
            'master of strategy': 1,
            'flash of steel': 1,        # removed if we have snecko eye
            'finesse': 1,               # removed if we have snecko eye
        }

        self.additional_cards_desired_if_from_a_potion: dict[str, int] = {
            'envenom': 3,
            'a thousand cuts': 3,
            'noxious fumes': 3,
            'caltrops': 3,
            'corpse explosion': 3,
            'crippling cloud': 3,
            'apotheosis': 1,
            'panache': 3,
            'sadistic nature': 3,
            'panacea': 3,
            'bandage up': 3,
            'dramatic entrance': 3,
            'blind': 1,
            'deep breath': 1,
            'enlightenment': 1,
        }

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT" or
                    state.game_state()["room_phase"] == "COMBAT")

    def handle(self, state: GameState) -> List[str]:
        choice_list = state.get_choice_list_upgrade_stripped_from_choice()
        deck_card_list = state.get_deck_card_list_upgrade_stripped_from_name()

        # we have to copy this, otherwise it will modify the list until the bot is rerun
        desired_cards_working_copy = self.cards_desired_for_deck.copy()

        # check if we're selecting from a potion
        if state.game_state()["room_phase"] == "COMBAT":
            desired_cards_working_copy.update(self.additional_cards_desired_if_from_a_potion)

        if state.has_relic("Snecko Eye"):
            del desired_cards_working_copy['tools of the trade']
            del desired_cards_working_copy['escape plan']
            del desired_cards_working_copy['prepared']
            del desired_cards_working_copy['backstab']
            del desired_cards_working_copy['flash of steel']
            del desired_cards_working_copy['finesse']

        for desired_card in desired_cards_working_copy:
            if desired_card not in choice_list:
                continue
            if desired_card in deck_card_list and deck_card_list[desired_card] >= desired_cards_working_copy[
                desired_card]:
                continue
            if presentation_mode:
                return [p_delay, "choose " + str(choice_list.index(desired_card)), "wait 30"]
            return ["choose " + str(choice_list.index(desired_card)), "wait 30"]

        # exiting after not finding what we want
        exit_choice = "undecided"

        if 'bowl' in choice_list:
            exit_choice = "choose bowl"
        elif not state.has_command(Command.SKIP):  # Mainly (only?) relevant for the Colorless potion
            exit_choice = "choose 0"
        elif state.game_state()["room_phase"] == "COMBAT":  # E.g. potions
            exit_choice = "skip"
        elif state.game_state()["room_phase"] == "EVENT" and not state.floor() == '0' and not state.has_relic("Tiny House"):
            exit_choice = "skip"  # There isn't a `proceed` available after skipping Neow's card obtain for example.

        if exit_choice != "undecided":
            if presentation_mode:
                return [p_delay, exit_choice, "wait 30"]
            return [exit_choice, "wait 30"]

        # Very specific case for being with Neow and getting a Tiny House, which unfortunately requires different exiting.
        if state.floor() == "0" and state.has_relic("Tiny House"):
            return ["skip", "proceed"]

        if presentation_mode:
            return [p_delay, "skip", "proceed"]
        return ["skip", "proceed"]  # This 'proceed' is for avoiding looking at the card rewards again.
