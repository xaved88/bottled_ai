from typing import List

from rs.ai.requested_scaling.handlers.general_handlers.chest_handler import ChestHandler
from rs.ai.requested_scaling.handlers.general_handlers.astrolabe_handler import AstrolabeHandler
from rs.ai.requested_scaling.handlers.general_handlers.battle_handler import BattleHandler
from rs.ai.requested_scaling.handlers.general_handlers.boss_relic_handler import BossRelicHandler
from rs.ai.requested_scaling.handlers.general_handlers.campfire_handler import CampfireHandler
from rs.ai.requested_scaling.handlers.general_handlers.card_reward_handler import CardRewardHandler
from rs.ai.requested_scaling.handlers.general_handlers.combat_reward_handler import CombatRewardHandler
from rs.ai.requested_scaling.handlers.custom_battle.gremlin_nob_handler import GremlinNobHandler
from rs.ai.requested_scaling.handlers.custom_battle.lagavulin_handler import LagavulinHandler
from rs.ai.requested_scaling.handlers.custom_battle.sentries_handler import SentriesHandler
from rs.ai.requested_scaling.handlers.custom_battle.transient_handler import TransientHandler
from rs.ai.requested_scaling.handlers.general_handlers.discard_handler import DiscardHandler
from rs.ai.requested_scaling.handlers.general_handlers.event_handler import EventHandler
from rs.ai.requested_scaling.handlers.general_handlers.neow_handler import NeowHandler
from rs.ai.requested_scaling.handlers.general_handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, \
    PotionsEliteHandler
from rs.ai.requested_scaling.handlers.general_handlers.purge_handler import PurgeHandler
from rs.ai.requested_scaling.handlers.general_handlers.shop_entrance_handler import ShopEntranceHandler
from rs.ai.requested_scaling.handlers.general_handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.requested_scaling.handlers.general_handlers.smart_battle_handler import SmartBattleHandler
from rs.ai.requested_scaling.handlers.general_handlers.smart_path_handler import SmartPathHandler
from rs.ai.requested_scaling.handlers.synergy_handlers.exhaust_action.exhaust_handler import ExhaustHandler
from rs.ai.requested_scaling.handlers.synergy_handlers.scaling_battle_handler import ScalingBattleHandler
from rs.ai.requested_scaling.handlers.synergy_handlers.synergy_card_reward_handler import SynergyCardRewardHandler
from rs.ai.requested_scaling.handlers.general_handlers.transform_handler import TransformHandler
from rs.ai.requested_scaling.handlers.general_handlers.upgrade_handler import UpgradeHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

requested_scaling_custom_battle_handlers: List[Handler] = [
    # Potions Handlers First
    PotionsBossHandler(),
    PotionsEventFightHandler(),
    PotionsEliteHandler(),

    #Inserting Scaling Handler as high as possible:
    ExhaustHandler(),
    ScalingBattleHandler(),

    # Enemies After
    GremlinNobHandler(),
    LagavulinHandler(),
    SentriesHandler(),
    TransientHandler(),
]

REQUESTED_SCALING: AiStrategy = AiStrategy(
    character=Character.IRONCLAD,
    handlers=requested_scaling_custom_battle_handlers + [
        # Some edge cases
        AstrolabeHandler(),

        # Temp for testing
        ScalingBattleHandler(),
        ExhaustHandler(),
        SmartBattleHandler(),

        # General Stuff
        BossRelicHandler(),
        BattleHandler(),
        UpgradeHandler(),
        TransformHandler(),
        PurgeHandler(),
        CombatRewardHandler(),
        SynergyCardRewardHandler(),
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
