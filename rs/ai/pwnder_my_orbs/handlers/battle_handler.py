from rs.ai.pwnder_my_orbs.comparators.pmo_big_fight_comparator import PmoBigFightComparator
from rs.ai.pwnder_my_orbs.comparators.pmo_general_comparator import PmoGeneralComparator
from rs.common.handlers.common_battle_handler import BattleHandlerConfig, CommonBattleHandler
from rs.machine.handlers.handler import Handler


def get_pmo_battle_handler() -> Handler:
    config = BattleHandlerConfig()
    config.big_fight_floors = [16, 33, 50]
    config.big_fight_comparator = PmoBigFightComparator
    config.general_comparator = PmoGeneralComparator

    return CommonBattleHandler(config=config)
