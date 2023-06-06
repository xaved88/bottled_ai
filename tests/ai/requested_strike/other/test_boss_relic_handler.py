from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.boss_relic_handler import BossRelicHandler


class BossRelicHandlerTestCase(RsTestHandlerFixture):
    handler = BossRelicHandler

    def test_skip_bad_energy_relics_when_applicable(self):
        self.execute_handler_tests('relics/boss_reward_nothing_to_take.json', ['skip', 'proceed'])

