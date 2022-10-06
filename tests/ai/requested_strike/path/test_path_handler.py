from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.path_handler import PathHandler


class PathHandlerTestCase(RsTestHandlerFixture):
    handler = PathHandler
    # Path handler is not in RS default handlers anymore, but we still want to keep it around
    ai_handlers = [PathHandler()]

    def test_no_errors_on_basic(self):
        self.execute_handler_tests('/path/path_basic.json', ['choose 0'])

    def test_choose_different_path_based_on_elites(self):
        self.execute_handler_tests('/path/path_elites.json', ['choose 1'])

    def test_initial_state(self):
        self.execute_handler_tests('/path/path_initial_state.json', ['choose 1'])

    def test_act_two_start(self):
        self.execute_handler_tests('/path/path_act_two_start.json', ['choose 3'])

    def test_no_zero_x(self):
        # we had bugs for a while reading paths when there was no node in the farthest left x column
        self.execute_handler_tests('/path/path_no_zero_x.json', ['choose 1'])

    def test_many_options(self):
        self.execute_handler_tests('/path/path_many_options.json', ['choose 3'])

    def test_act_three_start_with_bad_coord_bug(self):
        # This one is funky, it's giving "-1_15" as the current coord, only time I've ever seen a -x... :shrug:
        self.execute_handler_tests('/path/path_bad_coord_bug.json', ['choose 1'])
