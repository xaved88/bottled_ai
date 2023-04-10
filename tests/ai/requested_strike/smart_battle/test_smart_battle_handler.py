import time

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.smart_battle_handler import SmartBattleHandler
from test_helpers.resources import load_resource_state


class BattleHandlerTestCase(RsTestHandlerFixture):
    handler = SmartBattleHandler

    def test_plays_bash(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_basic.json', ['play 5 0'])

    def test_plays_kills_opponent(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_choose_kill.json', ['play 1 0'])

    def test_doesnt_play_burn(self):
        state = load_resource_state('battles/smart_battle/smart_battle_burns.json')
        self.assertEqual(['play 2 0'], SmartBattleHandler().handle(state))

    def test_complex_case_does_not_timeout(self):
        start = time.perf_counter()
        state = load_resource_state('battles/smart_battle/smart_battle_complex_case.json')
        self.assertEqual(['play 5'], SmartBattleHandler().handle(state))
        end = time.perf_counter()
        if end > start + 40:
            self.fail("Process took too long!")

    def test_another_simple_case(self):
        state = load_resource_state('battles/smart_battle/smart_battle_another_simple.json')
        self.assertEqual(['play 5'], SmartBattleHandler().handle(state))
