from typing import List

from rs.ai.requested_strike.handlers.card_reward_handler import CardRewardHandler
from rs.ai.requested_strike.handlers.temp_fight_handler import TempFightHandler
from rs.ai.requested_strike.handlers.temp_path_handler import TempPathHandler
from rs.ai.requested_strike.handlers.upgrade_handler import UpgradeHandler
from rs.machine.handlers.handler import Handler

REQUESTED_STRIKE: List[Handler] = [
    # CustomPathHandler(),
    TempFightHandler(),
    UpgradeHandler(),
    CardRewardHandler(),
]
