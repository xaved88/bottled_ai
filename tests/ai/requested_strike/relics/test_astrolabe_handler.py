from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.astrolabe_handler import AstrolabeHandler


class TestAstrolabeHandler(RsTestHandlerFixture):
    handler = AstrolabeHandler

    def test_picks_three(self):
        self.execute_handler_tests('relics/boss_reward_astrolabe.json',
                                   ['choose 6', 'wait 30', 'choose 8', 'wait 30', 'choose 5', 'wait 30'])
