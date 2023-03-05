from typing import List

from rs.ai.shivs_and_giggles.handlers.chest_handler import ChestHandler
from rs.ai.shivs_and_giggles.handlers.astrolabe_handler import AstrolabeHandler
from rs.ai.shivs_and_giggles.handlers.battle_handler import BattleHandler
from rs.ai.shivs_and_giggles.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.shivs_and_giggles.handlers.campfire_handler import CampfireHandler
from rs.ai.shivs_and_giggles.handlers.card_reward_handler import CardRewardHandler
from rs.ai.shivs_and_giggles.handlers.combat_reward_handler import CombatRewardHandler
from rs.ai.shivs_and_giggles.handlers.custom_battle.gremlin_nob_handler import GremlinNobHandler
from rs.ai.shivs_and_giggles.handlers.custom_battle.lagavulin_handler import LagavulinHandler
from rs.ai.shivs_and_giggles.handlers.custom_battle.sentries_handler import SentriesHandler
from rs.ai.shivs_and_giggles.handlers.custom_battle.transient_handler import TransientHandler
from rs.ai.shivs_and_giggles.handlers.discard_handler import DiscardHandler
from rs.ai.shivs_and_giggles.handlers.event_handler import EventHandler
from rs.ai.shivs_and_giggles.handlers.neow_handler import NeowHandler
from rs.ai.shivs_and_giggles.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, \
    PotionsEliteHandler
from rs.ai.shivs_and_giggles.handlers.purge_handler import PurgeHandler
from rs.ai.shivs_and_giggles.handlers.shop_entrance_handler import ShopEntranceHandler
from rs.ai.shivs_and_giggles.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.shivs_and_giggles.handlers.smart_battle_handler import SmartBattleHandler
from rs.ai.shivs_and_giggles.handlers.smart_path_handler import SmartPathHandler
from rs.ai.shivs_and_giggles.handlers.transform_handler import TransformHandler
from rs.ai.shivs_and_giggles.handlers.upgrade_handler import UpgradeHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

shivs_and_giggles_custom_battle_handlers: List[Handler] = [
    # Potions Handlers First
    PotionsBossHandler(),
    PotionsEventFightHandler(),
    PotionsEliteHandler(),

    # Enemies After
    GremlinNobHandler(),
    LagavulinHandler(),
    SentriesHandler(),
    TransientHandler(),
]

SHIVS_AND_GIGGLES: AiStrategy = AiStrategy(
    character=Character.SILENT,
    handlers=shivs_and_giggles_custom_battle_handlers + [
        # Some edge cases
        AstrolabeHandler(),

        # Temp for testing
        SmartBattleHandler(),

        # General Stuff
        BossRelicHandler(),
        BattleHandler(),
        UpgradeHandler(),
        TransformHandler(),
        PurgeHandler(),
        CombatRewardHandler(),
        CardRewardHandler(),
        NeowHandler(),
        EventHandler(),
        ChestHandler(),
        SmartPathHandler(),
        CampfireHandler(),
        ShopEntranceHandler(),
        ShopPurchaseHandler(),
        DiscardHandler(),
    ]
)
