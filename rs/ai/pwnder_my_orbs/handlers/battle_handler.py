from rs.ai.pwnder_my_orbs.comparators.pmo_big_fight_comparator import PmoBigFightComparator
from rs.ai.pwnder_my_orbs.comparators.pmo_general_comparator import PmoGeneralComparator
from rs.ai.pwnder_my_orbs.comparators.pmo_gremlin_nob_comparator import PmoGremlinNobComparator
from rs.ai.pwnder_my_orbs.comparators.pmo_three_sentry_comparator import PmoThreeSentriesComparator
from rs.ai.pwnder_my_orbs.comparators.pmo_waiting_lagavulin_comparator import PmoWaitingLagavulinComparator
from rs.common.handlers.common_battle_handler import BattleHandlerConfig, CommonBattleHandler
from rs.machine.handlers.handler import Handler


def get_pmo_battle_handler() -> Handler:
    config = BattleHandlerConfig()
    config.big_fight_floors = [16, 33, 50]
    config.big_fight_comparator = PmoBigFightComparator
    config.gremlin_nob_comparator = PmoGremlinNobComparator
    config.three_sentries_comparator = PmoThreeSentriesComparator
    config.waiting_lagavulin_comparator = PmoWaitingLagavulinComparator
    config.general_comparator = PmoGeneralComparator

    return CommonBattleHandler(config=config)
