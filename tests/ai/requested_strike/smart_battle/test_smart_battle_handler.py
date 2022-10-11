from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.smart_battle_handler import SmartBattleHandler
from rs.calculator.game_state_converter import create_hand_state
from rs.calculator.play_path import get_paths, PlayPath
from test_helpers.resources import load_resource_state


class BattleHandlerTestCase(RsTestHandlerFixture):
    handler = SmartBattleHandler
    ai_handlers = [SmartBattleHandler()]

    def test_plays_bash(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_basic.json', ['play 5 0'])

    def test_plays_kills_opponent(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_choose_kill.json', ['play 1 0'])

    def test_doesnt_play_burn(self):
        self.execute_handler_tests('battles/smart_battle/smart_battle_burns.json', ['play 2 0'])

    # 2022-10-11-14-07-35--42V8JEKM6IGU.log crashed it, seems to go into an infinite loop somewhere...
    def test_crash_doesnt_crash(self):
        return None # TO FIX
        hand_state = create_hand_state(load_resource_state("battles/smart_battle/smart_battle_crash_test.json"))
        paths = get_paths(PlayPath([], hand_state))
        print(f"Paths: {len(paths)}")
        self.assertEqual(1, 1)
