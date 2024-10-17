from typing import List

from rs.ai.shivs_and_giggles.config import CARD_REMOVAL_PRIORITY_LIST, HIGH_PRIORITY_UPGRADES, DESIRED_POTIONS, \
    DESIRED_CARDS_FOR_DECK
from rs.ai.shivs_and_giggles.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.shivs_and_giggles.handlers.card_reward_handler import CardRewardHandler
from rs.ai.shivs_and_giggles.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, \
    PotionsEliteHandler
from rs.ai.shivs_and_giggles.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.shivs_and_giggles.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler
from rs.common.handlers.common_event_handler import CommonEventHandler
from rs.common.handlers.common_mass_discard_handler import CommonMassDiscardHandler
from rs.common.handlers.common_map_handler import CommonMapHandler
from rs.common.handlers.common_neow_handler import CommonNeowHandler
from rs.common.handlers.common_purge_handler import CommonPurgeHandler
from rs.common.handlers.common_scry_handler import CommonScryHandler
from rs.common.handlers.common_shop_entrance_handler import CommonShopEntranceHandler
from rs.common.handlers.common_transform_handler import CommonTransformHandler
from rs.machine.ai_strategy import AiStrategy
from rs.machine.character import Character
from rs.machine.handlers.handler import Handler

shivs_and_giggles_battle_potion_handlers: List[Handler] = [
    # Potions Handlers First
    PotionsBossHandler(),
    PotionsEventFightHandler(),
    PotionsEliteHandler(),
]

SHIVS_AND_GIGGLES: AiStrategy = AiStrategy(
    name='SHIVS_AND_GIGGLES',
    character=Character.SILENT,
    handlers=shivs_and_giggles_battle_potion_handlers + [
        # Some edge cases
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),

        # Battle Handler
        CommonBattleHandler(),

        # General Stuff
        BossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonCombatRewardHandler(desired_potions=DESIRED_POTIONS),
        CardRewardHandler(),
        CommonNeowHandler(),
        CommonEventHandler(removal_priority_list=CARD_REMOVAL_PRIORITY_LIST, cards_desired_for_deck=DESIRED_CARDS_FOR_DECK),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(HIGH_PRIORITY_UPGRADES, CARD_REMOVAL_PRIORITY_LIST),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonMassDiscardHandler(),
        CommonScryHandler(),
    ]
)
