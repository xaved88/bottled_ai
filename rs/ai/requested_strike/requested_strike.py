from typing import List

from rs.ai.requested_strike.config import CARD_REMOVAL_PRIORITY_LIST, DESIRED_CARDS_FOR_DECK, HIGH_PRIORITY_UPGRADES, \
    DESIRED_POTIONS
from rs.ai.requested_strike.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.requested_strike.handlers.event_handler import EventHandler
from rs.ai.requested_strike.handlers.neow_handler import NeowHandler
from rs.ai.requested_strike.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, \
    PotionsEliteHandler
from rs.ai.requested_strike.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.requested_strike.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.card_reward.common_card_reward_handler import CommonCardRewardHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler
from rs.common.handlers.common_grid_select_handler import CommonGridSelectHandler
from rs.common.handlers.common_mass_discard_handler import CommonMassDiscardHandler
from rs.common.handlers.common_map_handler import CommonMapHandler
from rs.common.handlers.common_purge_handler import CommonPurgeHandler
from rs.common.handlers.common_scry_handler import CommonScryHandler
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler
from rs.common.handlers.common_transform_handler import CommonTransformHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

requested_strike_custom_battle_handlers: List[Handler] = [
    # Potions Handlers First
    PotionsBossHandler(),
    PotionsEventFightHandler(),
    PotionsEliteHandler(),
]

REQUESTED_STRIKE: AiStrategy = AiStrategy(
    name='REQUESTED_STRIKE',
    character=Character.IRONCLAD,
    handlers=requested_strike_custom_battle_handlers + [
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonBattleHandler(),

        # General Stuff
        BossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonGridSelectHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonCombatRewardHandler(desired_potions=DESIRED_POTIONS),
        CommonCardRewardHandler(DESIRED_CARDS_FOR_DECK),
        NeowHandler(),
        EventHandler(removal_priority_list=CARD_REMOVAL_PRIORITY_LIST, cards_desired_for_deck=DESIRED_CARDS_FOR_DECK),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(HIGH_PRIORITY_UPGRADES, CARD_REMOVAL_PRIORITY_LIST),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonMassDiscardHandler(),
        CommonScryHandler(),
    ]
)
