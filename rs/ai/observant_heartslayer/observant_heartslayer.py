from typing import List

from rs.ai.observant_heartslayer.config import CARD_REMOVAL_PRIORITY_LIST, HIGH_PRIORITY_UPGRADES, DESIRED_POTIONS
from rs.ai.observant_heartslayer.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.observant_heartslayer.handlers.card_reward_handler import CardRewardHandler
from rs.ai.observant_heartslayer.handlers.event_handler import EventHandler
from rs.ai.observant_heartslayer.handlers.neow_handler import NeowHandler
from rs.ai.observant_heartslayer.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, PotionsEliteHandler
from rs.ai.observant_heartslayer.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.observant_heartslayer.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler
from rs.common.handlers.common_mass_discard_handler import CommonMassDiscardHandler
from rs.common.handlers.common_map_handler import CommonMapHandler
from rs.common.handlers.common_purge_handler import CommonPurgeHandler
from rs.common.handlers.common_scry_handler import CommonScryHandler
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler
from rs.common.handlers.common_transform_handler import CommonTransformHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

peaceful_pummeling_potion_handlers: List[Handler] = [
    PotionsBossHandler(),
    # PotionsEventFightHandler(),  # Watcher doesn't really need this one - better to save our potions for the boss.
    PotionsEliteHandler(),
]

OBSERVANT_HEARTSLAYER: AiStrategy = AiStrategy(
    name='OBSERVANT_HEARTSLAYER',
    character=Character.WATCHER,
    slay_heart=True,
    handlers=peaceful_pummeling_potion_handlers + [
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonBattleHandler(),
        BossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonCombatRewardHandler(desired_potions=DESIRED_POTIONS),
        CardRewardHandler(),
        NeowHandler(),
        EventHandler(),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(HIGH_PRIORITY_UPGRADES, CARD_REMOVAL_PRIORITY_LIST),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonMassDiscardHandler(),
        CommonScryHandler(),
    ],
)
