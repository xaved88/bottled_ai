from ai.peaceful_pummeling.pp_test_handler_fixture import PpTestHandlerFixture
from rs.ai.peaceful_pummeling.handlers.boss_relic_handler import BossRelicHandler


class BossRelicHandlerTestCase(PpTestHandlerFixture):
    handler = BossRelicHandler

    def test_select_violet_lotus(self):
        self.execute_handler_tests('relics/boss_reward_take_violet_lotus.json', ['choose 1'])
