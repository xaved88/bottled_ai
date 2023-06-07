import time
import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.common_battle_handler import CommonBattleHandler
from test_helpers.resources import load_resource_state


class BattleHandlerTestCase(RsTestHandlerFixture):
    handler = CommonBattleHandler

    def test_plays_bash(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_basic.json', ['play 5 0'])

    def test_plays_kills_opponent(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_choose_kill.json', ['play 1 0'])

    def test_doesnt_play_burn(self):
        state = load_resource_state('battles/smart_battle/smart_battle_burns.json')
        self.assertEqual(['play 2 0'], CommonBattleHandler().handle(state))

    @unittest.skip("we only want to run this test occasionally")
    def test_complex_case_does_not_timeout(self):
        start = time.perf_counter()
        state = load_resource_state('battles/smart_battle/smart_battle_complex_case.json')
        self.assertEqual(['play 5'], CommonBattleHandler().handle(state))
        end = time.perf_counter()
        if end > start + 40:
            self.fail("Process took too long!")

    def test_another_simple_case(self):
        state = load_resource_state('battles/smart_battle/smart_battle_another_simple.json')
        self.assertEqual(['play 5'], CommonBattleHandler().handle(state))
