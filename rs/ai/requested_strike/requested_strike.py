from typing import List

from rs.ai.requested_strike.handlers.astrolabe_handler import AstrolabeHandler
from rs.ai.requested_strike.handlers.battle_handler import BattleHandler
from rs.ai.requested_strike.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.requested_strike.handlers.campfire_handler import CampfireHandler
from rs.ai.requested_strike.handlers.card_reward_handler import CardRewardHandler
from rs.ai.requested_strike.handlers.custom_battle.gremlin_nob_handler import GremlinNobHandler
from rs.ai.requested_strike.handlers.custom_battle.lagavulin_handler import LagavulinHandler
from rs.ai.requested_strike.handlers.custom_battle.sentries_handler import SentriesHandler
from rs.ai.requested_strike.handlers.custom_battle.transient_handler import TransientHandler
from rs.ai.requested_strike.handlers.event_handler import EventHandler
from rs.ai.requested_strike.handlers.path_handler import PathHandler
from rs.ai.requested_strike.handlers.potions_handler import PotionsBossHandler, PotionsEliteHandler
from rs.ai.requested_strike.handlers.purge_handler import PurgeHandler
from rs.ai.requested_strike.handlers.shop_entrance_handler import ShopEntranceHandler
from rs.ai.requested_strike.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.requested_strike.handlers.smart_path_handler import SmartPathHandler
from rs.ai.requested_strike.handlers.transform_handler import TransformHandler
from rs.ai.requested_strike.handlers.upgrade_handler import UpgradeHandler
from rs.machine.handlers.handler import Handler

requested_strike_custom_battle_handlers: List[Handler] = [
    # Potions Handlers First
    PotionsBossHandler(),
    PotionsEliteHandler(),

    # Enemies After
    GremlinNobHandler(),
    LagavulinHandler(),
    SentriesHandler(),
    TransientHandler(),
]

REQUESTED_STRIKE: List[Handler] = requested_strike_custom_battle_handlers + [
    # Some edge cases
    AstrolabeHandler(),

    # General Stuff
    BossRelicHandler(),
    BattleHandler(),
    EventHandler(),
    UpgradeHandler(),
    TransformHandler(),
    PurgeHandler(),
    CardRewardHandler(),
    PathHandler(),
    #SmartPathHandler(),
    CampfireHandler(),
    ShopEntranceHandler(),
    ShopPurchaseHandler(),
]
