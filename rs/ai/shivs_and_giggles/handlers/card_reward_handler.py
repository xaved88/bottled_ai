from rs.common.handlers.common_card_reward_handler import CommonCardRewardHandler
from rs.machine.state import GameState


class CardRewardHandler(CommonCardRewardHandler):

    def __init__(self):
        super().__init__(
            cards_desired_for_deck={
                'accuracy': 4,
                'after image': 2,
                'tools of the trade': 1,  # removed if we have snecko eye
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
                'escape plan': 2,  # removed if we have snecko eye
                'dagger throw': 1,
                'footwork': 1,
                'prepared': 1,  # removed if we have snecko eye
                'unload': 1,
                'backstab': 1,  # removed if we have snecko eye
                'master of strategy': 1,
                'flash of steel': 1,  # removed if we have snecko eye
                'finesse': 1,  # removed if we have snecko eye
            }, cards_desired_from_potions={
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
        )

    def transform_desired_cards_map_from_state(self, cards: dict[str, int], state: GameState):
        if state.has_relic("Snecko Eye"):
            del cards['tools of the trade']
            del cards['escape plan']
            del cards['prepared']
            del cards['backstab']
            del cards['flash of steel']
            del cards['finesse']
