from typing import List

from config import presentation_mode, p_delay, p_delay_s
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class CardRewardHandler(Handler):

    def __init__(self):
        self.desired_cards: dict[str, int] = {
            'limit break': 2,
            'inflame': 2,
            'spot weakness': 1,
            'hemokinesis': 1,
            'immolate': 1,
            'offering': 1,
            'disarm': 2,
            'burning pact': 1,
            'feel no pain': 2,
            'evolve': 1,
            'power through': 1,
            'battle trance': 1,
            'reaper': 2,
            'twin strike': 2,
            'pommel strike': 2,
            'shockwave': 1,
            'thunderclap': 1,
            'dropkick': 2,
            'flex': 1,
            'shrug it off': 3,
            'impervious': 2,
            'ghostly armor': 1,
            'flame barrier': 1,
            'blind': 1,
            'dark embrace': 1,
            'apotheosis': 1,
            'handofgreed': 1,
            'master of strategy': 1,
            'flash of steel': 1,
            'trip': 1,
            'dark shackles': 1,
            'swift strike': 1,
            'dramatic entrance': 1,
            'heavy blade': 1,
            'finesse': 1,
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
