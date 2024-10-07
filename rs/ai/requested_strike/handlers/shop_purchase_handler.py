from typing import List

from presentation_config import presentation_mode, p_delay, p_delay_s
from rs.ai.requested_strike.config import CARD_REMOVAL_PRIORITY_LIST
from rs.game.card import CardType
from rs.game.screen_type import ScreenType
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class ShopPurchaseHandler(Handler):

    def __init__(self):
        self.relics = [
            'Bag of Marbles',
            'Pen Nib',
            'Strike Dummy',
            'Paper Phrog',
            'Preserved Insect',
            'Red Skull',
            'Meat on the Bone',
            'Eternal Feather',
            'Regal Pillow',
            'Lee’s Waffle',
            'Meal Ticket',
            'Strawberry',
            'Toy Ornithopter',
            'Pantograph',
            'Pear',
            'Orichalcum',
            'Anchor',
            'Horn Cleat',
            'Self-Forming Clay',
            'Thread and Needle',
            'Lantern',
            'Happy Flower',
            'Bag of Preparation',
            'Centennial Puzzle',
        ]

        self.cards = [
            "Offering",
            "Battle Trance",
            "Shockwave"
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.screen_type() == ScreenType.SHOP_SCREEN.value

    def handle(self, state: GameState, slay_heart: bool) -> HandlerAction:
        choice = self.find_choice(state)
        if choice:
            idx = state.get_choice_list().index(choice)
            if presentation_mode:
                return HandlerAction(commands=[p_delay, "choose " + str(idx), p_delay_s, "wait 30"])
            return HandlerAction(commands=["choose " + str(idx), "wait 30"])
        if presentation_mode:
            return HandlerAction(commands=["wait " + p_delay, "return", "proceed"])
        return HandlerAction(commands=["return", "proceed"])

    def find_choice(self, state: GameState) -> str:
        gold = state.game_state()['gold']
        screen_state = state.game_state()['screen_state']
        can_purge = screen_state['purge_available'] and gold >= screen_state['purge_cost']

        # 1. Purge curses
        if can_purge and state.deck.contains_curses_we_can_remove():
            return "purge"

        # 2. Perfected strike
        for card in screen_state['cards']:
            if card['id'] == 'Perfected Strike' and gold >= card['price']:
                return card['name'].lower()

        # 3. Membership Card
        for relic in screen_state['relics']:
            if relic['name'] == 'Membership Card' and gold >= relic['price']:
                return "membership card"

        # 4. Purge in general
        if can_purge and state.deck.contains_cards(CARD_REMOVAL_PRIORITY_LIST):
            return "purge"

        # 5. Relics based on list
        for p in self.relics:
            for relic in screen_state['relics']:
                if relic['name'] == p and gold >= relic['price']:
                    return relic['name'].lower()

        # 6. Cards based on list
        deck_card_list = state.get_deck_card_list_by_id()
        for p in self.cards:
            for card in screen_state['cards']:
                if card['id'] == p and gold >= card['price']:
                    if p.lower not in deck_card_list:
                        return card['name'].lower()

        # Nothing we want / can afford, leave.
        return ''
