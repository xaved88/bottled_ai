from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.common_astrolabe_handler import CommonAstrolabeHandler


class TestAstrolabeHandler(RsTestHandlerFixture):
    handler = CommonAstrolabeHandler

    def test_picks_three(self):
        self.execute_handler_tests('relics/boss_reward_astrolabe.json',
                                   ['choose 6', 'wait 30', 'choose 8', 'wait 30', 'choose 5', 'wait 30'])
