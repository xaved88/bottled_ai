from typing import List

from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler
from rs.machine.state import GameState


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'eruption',
            'blasphemy',
            'vigilance',
            'talk to the hand',
            'rushdown', # removed if snecko
            'tantrum',
            'crescendo',  # removed if snecko
            'tranquility',  # removed if snecko
            'reach heaven',
            'mental fortress',
            'fear no evil',
            'reach heaven',
            'empty body',
            'empty fist',
            'inner peace',
            'flurry of blows',
            'lesson learned',
            'halt',  # removed if snecko
            'carve reality',
            'wallop',
            'battle hymn',
            'spirit shield',
            'sands of time',
            'perseverance',
            'wheel kick',
            'like water',
            'crush joints',
            'deceive reality',
            'follow-up',
        ])

    def transform_priorities_based_on_game_state(self, priorities: List[str], state: GameState):
        if state.has_relic("Snecko Eye"):
            priorities.remove('crescendo')
            priorities.remove('tranquility')
            priorities.remove('halt')
            priorities.remove('rushdown')
