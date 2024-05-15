from typing import List

from rs.common.handlers.common_upgrade_handler import CommonUpgradeHandler
from rs.machine.state import GameState


class UpgradeHandler(CommonUpgradeHandler):

    def __init__(self):
        super().__init__(priorities=[
            'apotheosis',
            'eruption',
            'blasphemy',
            'tantrum',
            'talk to the hand',
            'rushdown',  # removed if snecko
            'flurry of blows',
            'cut_through_fate',
            'wallop',
            'mental fortress',
            'reach heaven',
            'carve reality',
            'crush joints',
            'vigilance',
            'ragnarok',
            'fear no evil',
            'reach heaven',
            'inner peace',
            'lesson learned',
            'halt',  # removed if snecko
            'indignation',
            'empty body',
            'empty fist',
            'battle hymn',
            'spirit shield',
            'deceive reality',
            'crescendo',  # removed if snecko
            'tranquility',  # removed if snecko
            'sands of time',
            'perseverance',
            'wheel kick',
            'like water',
            'follow-up',
        ])

    def transform_priorities_based_on_game_state(self, priorities: List[str], state: GameState):
        if state.has_relic("Snecko Eye"):
            priorities.remove('crescendo')
            priorities.remove('tranquility')
            priorities.remove('halt')
            priorities.remove('rushdown')
