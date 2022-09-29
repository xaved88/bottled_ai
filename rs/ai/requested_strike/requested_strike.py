from typing import List

from rs.ai.requested_strike.handlers.battle_handler import BattleHandler
from rs.ai.requested_strike.handlers.card_reward_handler import CardRewardHandler
from rs.ai.requested_strike.handlers.custom_battle.gremlin_nob_handler import GremlinNobHandler
from rs.ai.requested_strike.handlers.path_handler import PathHandler
from rs.ai.requested_strike.handlers.upgrade_handler import UpgradeHandler
from rs.machine.handlers.handler import Handler

requested_strike_custom_battle_handlers: List[Handler] = [
    GremlinNobHandler()
]

REQUESTED_STRIKE: List[Handler] = requested_strike_custom_battle_handlers + [
    BattleHandler(),
    UpgradeHandler(),
    CardRewardHandler(),
    PathHandler(),
]
