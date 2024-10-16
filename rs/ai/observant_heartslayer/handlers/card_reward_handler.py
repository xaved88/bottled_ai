from rs.ai.observant_heartslayer.config import DESIRED_CARDS_FOR_DECK, DESIRED_CARDS_FROM_POTIONS
from rs.common.handlers.card_reward.common_card_reward_handler import CommonCardRewardHandler
from rs.machine.state import GameState


class CardRewardHandler(CommonCardRewardHandler):

    def __init__(self):
        super().__init__(
            cards_desired_for_deck=DESIRED_CARDS_FOR_DECK,
            cards_desired_from_potions=DESIRED_CARDS_FROM_POTIONS)

    def transform_desired_cards_map_from_state(self, cards: dict[str, int], state: GameState):
        remove_if_snecko = [
            'consecrate',
            'halt',
            'just lucky',
            'scrawl',
        ]
        safe_remove_if_snecko = []

        if state.has_relic("Snecko Eye"):
            for c in remove_if_snecko:
                if c in cards:
                    safe_remove_if_snecko.append(c)
            for d in safe_remove_if_snecko:
                del cards[d]

        remove_if_pyramid = [
            'battle hymn',
        ]
        safe_remove_if_pyramid = []

        if state.has_relic("Runic Pyramid"):
            for c in remove_if_pyramid:
                if c in cards:
                    safe_remove_if_pyramid.append(c)
            for d in safe_remove_if_pyramid:
                del cards[d]
