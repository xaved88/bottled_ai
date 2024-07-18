from rs.ai.shivs_and_giggles.config import DESIRED_CARDS_FOR_DECK, DESIRED_CARDS_FROM_POTIONS
from rs.common.handlers.card_reward.common_card_reward_handler import CommonCardRewardHandler
from rs.machine.state import GameState


class CardRewardHandler(CommonCardRewardHandler):

    def __init__(self):
        super().__init__(
            cards_desired_for_deck=DESIRED_CARDS_FOR_DECK,
            cards_desired_from_potions=DESIRED_CARDS_FROM_POTIONS
        )

    def transform_desired_cards_map_from_state(self, cards: dict[str, int], state: GameState):
        if state.has_relic("Snecko Eye"):
            del cards['tools of the trade']
            del cards['escape plan']
            del cards['prepared']
            del cards['backstab']
            del cards['flash of steel']
            del cards['finesse']
