from presentation_config import presentation_mode, p_delay, p_delay_s
from rs.ai.observant_heartslayer.config import CARD_REMOVAL_PRIORITY_LIST
from rs.game.screen_type import ScreenType
from rs.machine.handlers.handler import Handler
from rs.machine.handlers.handler_action import HandlerAction
from rs.machine.state import GameState


class ShopPurchaseHandler(Handler):

    def __init__(self):
        self.relics = [
            'Pen Nib',
            'Bag of Marbles',
            'Shuriken',
            'Meat on the Bone',
            'Vajra',
            'Bag of Preparation',
            'Kunai',
            'Eternal Feather',
            'Regal Pillow',
            'Lee’s Waffle',
            'Meal Ticket',
            'Strawberry',
            'Pear',
            'Pantograph',
            'Anchor',
            'Horn Cleat',
            'Lantern',
            'Centennial Puzzle',
            'Damaru',
        ]

        self.cards = [
            # 'Blasphemy',  # We have a specific line for purchasing Blasphemy with higher priority than Relics
            'Adaptation',  # Rushdown
            'Mentalfortress',
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

        # 2. Membership Card
        for relic in screen_state['relics']:
            if relic['name'] == 'Membership Card' and gold >= relic['price']:
                return "membership card"

        # 3. Blasphemy
        for card in screen_state['cards']:
            if card['id'] == 'Blasphemy' and gold >= card['price']:
                return card['name'].lower()

        # 4. Relics based on list
        for p in self.relics:
            for relic in screen_state['relics']:
                if relic['name'] == p and gold >= relic['price']:
                    return relic['name'].lower()

        # 5. Cards based on list
        deck_card_list = state.get_deck_card_list_by_id()
        for p in self.cards:
            for card in screen_state['cards']:
                if card['id'] == p and gold >= card['price']:
                    if p.lower not in deck_card_list:
                        return card['name'].lower()

        # 6. Purge in general
        if can_purge and state.deck.contains_cards(CARD_REMOVAL_PRIORITY_LIST):
            return "purge"

        # Nothing we want / can afford, leave.
        return ''
