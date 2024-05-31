import unittest

from ai.pwnder_my_orbs.pmo_test_handler_fixture import PmoTestHandlerFixture
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class BattleHandlerTestCase(PmoTestHandlerFixture):
    handler = CommonBattleHandler

    def test_plays_dualcast(self):
        self.execute_handler_tests('battles/with_orbs/defect_with_orb_and_dualcast.json', ['play 2'])

    def test_keep_calculating_even_if_multi_evoke_killed_everyone(self):
        self.execute_handler_tests('battles/with_orbs/multi_evoke_kills_last_enemy.json', ['play 1'])

    def test_hate_bias_early_in_big_fights(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/pmo_big_fight_do_not_allow_bias.json',
            ['end'])

    def test_hate_bias_if_unawakened_present(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/pmo_big_fight_hate_bias_because_unawakened_present.json',
            ['end'])

    def test_allow_bias_early_if_unawakened_not_present_and_is_awakened_one(self):
        self.execute_handler_tests(
            'battles/specific_comparator_cases/big_fight/pmo_big_fight_allow_bias_because_awakened_second_phase.json',
            ['play 1'])


if __name__ == '__main__':
    unittest.main()
