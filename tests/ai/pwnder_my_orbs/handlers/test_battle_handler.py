import unittest

from ai.pwnder_my_orbs.pmo_test_handler_fixture import PmoTestHandlerFixture
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class BattleHandlerTestCase(PmoTestHandlerFixture):
    handler = CommonBattleHandler

    def test_plays_dualcast(self):
        self.execute_handler_tests('battles/with_orbs/defect_with_orb_and_dualcast.json', ['play 2'])

    def test_keep_calculating_even_if_multi_evoke_killed_everyone(self):
        self.execute_handler_tests('battles/with_orbs/multi_evoke_kills_last_enemy.json', ['play 1'])

    def test_hate_bias_if_unawakened_present(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/pmo_big_fight_hate_bias_because_unawakened_present.json',
            ['end'])

    def test_allow_bias_if_unawakened_present_and_really_low(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/pmo_big_fight_allow_bias_because_unawakened_really_low.json',
            ['play 1'])


if __name__ == '__main__':
    unittest.main()
