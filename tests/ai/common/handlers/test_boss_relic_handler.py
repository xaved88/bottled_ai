from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_boss_relic_handler import CommonBossRelicHandler


class BossRelicHandlerTestCase(CoTestHandlerFixture):
    handler = CommonBossRelicHandler

    def test_select_first(self):
        self.execute_handler_tests('relics/boss_reward_first_is_best.json', ['choose 0'])

    def test_select_best(self):
        self.execute_handler_tests('relics/boss_reward_last_is_best.json', ['choose 2'])

    def test_take_mark_of_pain(self):
        self.execute_handler_tests('relics/boss_reward_mark_of_pain.json', ['choose 1'])

    def test_take_coffee_dripper(self):
        self.execute_handler_tests('relics/boss_reward_coffee_dripper.json', ['choose 1'])

    def test_take_busted_crown(self):
        self.execute_handler_tests('relics/boss_reward_busted_crown.json', ['choose 1'])

    def test_calling_boss_relic_handler_multiple_games_in_a_row_does_not_break(self):
        self.execute_handler_tests('relics/boss_reward_double_run_bug_check.json', ['choose 2'])
        self.execute_handler_tests('relics/boss_reward_double_run_bug_check.json', ['choose 2'])

    def test_do_not_take_runic_pyramid_because_we_have_snecko_eye(self):
        self.execute_handler_tests('relics/boss_reward_skip_runic_pyramid_because_snecko_eye.json', ['choose 2'])
