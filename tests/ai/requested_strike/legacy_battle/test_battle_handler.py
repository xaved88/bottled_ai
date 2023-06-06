import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.battle_handler import LegacyBattleHandler


class BattleHandlerTestCase(RsTestHandlerFixture):
    handler = LegacyBattleHandler

    ai_handlers = [LegacyBattleHandler()]
    def test_plays_bash(self):
        self.execute_handler_tests('battles/general/battle_should_play_bash.json', ['play 2 0'])

    def test_entangled(self):
        self.execute_handler_tests('battles/general/battle_entangled.json', ['play 4'])

    def test_defense_mode(self):
        self.execute_handler_tests('battles/general/battle_should_defend.json', ['play 3'])

    def test_kill_instead_of_defense_mode(self):
        self.execute_handler_tests('battles/general/battle_kill_instead_of_defend.json', ["play 1 0"])

    def test_unplayable_clash(self):
        self.execute_handler_tests('battles/general/battle_unplayable_clash.json', ["play 1 0"])

    def test_multi_counted_correctly_for_expected_damage(self):
        self.execute_handler_tests('battles/general/battle_multi_attack.json', ["play 3"])

    def test_runic_dome_doesnt_break_battle(self):
        self.execute_handler_tests('battles/general/battle_has_runic_dome.json', ["play 5"])

    def test_woke_blokes_transformation(self):
        self.execute_handler_tests('battles/general/battle_woke_bloke_transforming.json', ["end"])


if __name__ == '__main__':
    unittest.main()
