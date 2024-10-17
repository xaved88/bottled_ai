from typing import List

from rs.ai.pwnder_my_orbs.config import CARD_REMOVAL_PRIORITY_LIST, HIGH_PRIORITY_UPGRADES, DESIRED_POTIONS
from rs.ai.pwnder_my_orbs.handlers.battle_handler import get_pmo_battle_handler
from rs.ai.pwnder_my_orbs.handlers.boss_relic_handler import BossRelicHandler
from rs.ai.pwnder_my_orbs.handlers.card_reward_handler import CardRewardHandler
from rs.ai.pwnder_my_orbs.handlers.event_handler import EventHandler
from rs.ai.pwnder_my_orbs.handlers.potions_handler import PotionsBossHandler, PotionsEventFightHandler, \
    PotionsEliteHandler
from rs.ai.pwnder_my_orbs.handlers.shop_purchase_handler import ShopPurchaseHandler
from rs.ai.pwnder_my_orbs.handlers.upgrade_handler import UpgradeHandler
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler
from rs.common.handlers.common_chest_handler import CommonChestHandler
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler
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

orb_pondering_battle_potion_handlers: List[Handler] = [
    PotionsBossHandler(),
    PotionsEventFightHandler(),
    PotionsEliteHandler(),
]

PWNDER_MY_ORBS: AiStrategy = AiStrategy(
    name='PWNDER_MY_ORBS',
    character=Character.DEFECT,
    handlers=orb_pondering_battle_potion_handlers + [
        CommonAstrolabeHandler(CARD_REMOVAL_PRIORITY_LIST),
        get_pmo_battle_handler(),
        BossRelicHandler(),
        UpgradeHandler(),
        CommonTransformHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonPurgeHandler(CARD_REMOVAL_PRIORITY_LIST),
        CommonCombatRewardHandler(desired_potions=DESIRED_POTIONS),
        CardRewardHandler(),
        CommonNeowHandler(),
        EventHandler(removal_priority_list=CARD_REMOVAL_PRIORITY_LIST, cards_desired_for_deck=[]),
        CommonChestHandler(),
        CommonMapHandler(),
        CommonCampfireHandler(HIGH_PRIORITY_UPGRADES, CARD_REMOVAL_PRIORITY_LIST),
        CommonShopEntranceHandler(),
        ShopPurchaseHandler(),
        CommonMassDiscardHandler(),
        CommonScryHandler(),
    ]
)
