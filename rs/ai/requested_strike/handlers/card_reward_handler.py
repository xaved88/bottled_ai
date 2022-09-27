from typing import List

from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CardRewardHandler(Handler):

    def __init__(self):
        self.desired_cards: dict[str, int] = {
            'perfected strike': 5,
            'offering': 2,
            'battle trance': 2,
            'reaper': 2,
            'twin strike': 2,
            'shockwave': 2,
            'thunderclap': 2,
            'pommel strike': 2,
        }

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.CHOOSE) \
               and state.screen_type() == ScreenType.CARD_REWARD.value \
               and state.game_state()["room_phase"] == "COMPLETE"

    def handle(self, state: GameState) -> List[str]:
        choice_list = state.game_state()["choice_list"]
        deck_card_list = state.get_deck_card_list()

        for desired_card in self.desired_cards.keys():
            if desired_card not in choice_list:
                continue
            if desired_card in deck_card_list and deck_card_list[desired_card] >= self.desired_cards[desired_card]:
                continue
            return ["choose " + str(choice_list.index(desired_card))]
        return ["skip", "proceed"]
