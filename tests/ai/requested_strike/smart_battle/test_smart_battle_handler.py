import time

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.smart_battle_handler import SmartBattleHandler


class BattleHandlerTestCase(RsTestHandlerFixture):
    handler = SmartBattleHandler
    ai_handlers = [SmartBattleHandler()]

    def test_plays_bash(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_basic.json', ['play 5 0'])

    def test_plays_kills_opponent(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_choose_kill.json', ['play 1 0'])

    def test_doesnt_play_burn(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_burns.json', ['play 2 0'])

    def test_complex_case_does_not_timeout(self):
        start = time.perf_counter()
        self.execute_handler_tests('battles/smart_battle/smart_battle_complex_case.json', ['play 1'])
        end = time.perf_counter()
        if end > start + 40:
            self.fail("Process took too long!")
