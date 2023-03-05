from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CardRewardHandler(Handler):

    def __init__(self):
        self.desired_cards: dict[str, int] = {
            'a thousand cuts': 1,
            'tools of the trade': 1,
            'accuracy': 2,
            'terror': 2,
            'adrenaline': 2,
            'storm of steel': 2,
            'die die die': 2,
            'blade dance': 4,
            'infinite blades': 2,
            'after image': 1,
            'leg sweep': 1,
            'cloak and dagger': 2,
            'poisoned stab': 2,
            'sucker punch': 1,
            'escape plan': 4,
            'heel hook': 2,
            'dagger spray': 2,
            'caltrops': 1,
            'unload': 1,
            'backstab': 1,
        }

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and (state.game_state()["room_phase"] == "COMPLETE" or state.game_state()["room_phase"] == "EVENT")

    def handle(self, state: GameState) -> List[str]:
        choice_list = state.game_state()["choice_list"]

        for idx, choice in enumerate(choice_list):
            choice_list[idx] = choice.replace("+", "")

        deck_card_list = state.get_deck_card_list()

        for desired_card in self.desired_cards.keys():
            if desired_card not in choice_list:
                continue
            if desired_card in deck_card_list and deck_card_list[desired_card] >= self.desired_cards[desired_card]:
                continue
            if presentation_mode:
                return [p_delay, "choose " + str(choice_list.index(desired_card)), "wait 30"]
            return ["wait 30", "choose " + str(choice_list.index(desired_card)), "wait 30"]

        if 'bowl' in choice_list:
            if presentation_mode:
                return [p_delay, "choose bowl", p_delay_s]
            return ["wait 30", "choose bowl"]

        if state.game_state()["room_phase"] == "EVENT":
            if presentation_mode:
                return [p_delay, "skip", p_delay_s]
            return ["skip"]  # There isn't a `proceed` available after skipping Neow's card obtain for example.

        if presentation_mode:
            return [p_delay, "skip", p_delay_s, "proceed"]
        return ["skip", "proceed"]  # This 'proceed' is for avoiding looking at the card rewards again.
