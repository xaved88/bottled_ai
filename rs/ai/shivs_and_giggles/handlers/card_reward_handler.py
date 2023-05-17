from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CardRewardHandler(Handler):

    def __init__(self):
        self.desired_cards: dict[str, int] = {
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
            'prepared': 1,              # removed if we have snecko eye
            'dagger throw': 1,
            'footwork': 1,
            'unload': 1,
            'backstab': 1,              # removed if we have snecko eye
            'master of strategy': 1,
            'flash of steel': 1,        # removed if we have snecko eye
            'finesse': 1,               # removed if we have snecko eye
        }

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT" or
                    state.game_state()["room_phase"] == "COMBAT")

    def handle(self, state: GameState) -> List[str]:
        choice_list = state.game_state()["choice_list"]

        for idx, choice in enumerate(choice_list):
            choice_list[idx] = choice.replace("+", "")

        deck_card_list = state.get_deck_card_list()

        # we have to copy this, otherwise it will modify the list until the bot is rerun
        desired_cards_working_copy = self.desired_cards.copy()

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
            return ["wait 30", "choose " + str(choice_list.index(desired_card)), "wait 30"]

        # exiting after not finding what we want

        if 'bowl' in choice_list:
            if presentation_mode:
                return [p_delay, "choose bowl", p_delay_s]
            return ["wait 30", "choose bowl"]

        if not state.has_command(Command.SKIP):  # Mainly relevant for the Colorless potion from what I've seen
            if presentation_mode:
                return [p_delay, "choose 0", p_delay_s]
            return ["wait 30", "choose 0", "wait 30"]

        if state.game_state()["room_phase"] == "EVENT" or state.game_state()["room_phase"] == "COMBAT":
            if presentation_mode:
                return [p_delay, "skip", p_delay_s]
            return ["skip"]  # There isn't a `proceed` available after skipping Neow's card obtain for example.

        if presentation_mode:
            return [p_delay, "skip", p_delay_s, "proceed"]
        return ["skip", "proceed"]  # This 'proceed' is for avoiding looking at the card rewards again.
