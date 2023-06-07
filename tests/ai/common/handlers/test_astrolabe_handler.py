from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler


class TestAstrolabeHandler(CoTestHandlerFixture):
    handler = CommonAstrolabeHandler

    def test_picks_three(self):
        self.execute_handler_tests('relics/boss_reward_astrolabe.json',
                                   ['choose 5', 'wait 30', 'choose 2', 'wait 30', 'choose 3', 'wait 30'])
