from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_map_handler import CommonMapHandler


class MapHandlerTestCase(CoTestHandlerFixture):
    handler = CommonMapHandler

    def test_no_errors_on_basic(self):
        self.execute_handler_tests('/path/path_basic.json', ['choose 0'])

    def test_not_influenced_by_burning_elite(self):
        self.execute_handler_tests('/path/path_includes_burning_elite.json', ['choose 1'])

    def test_be_scared_of_burning_elite(self):
        self.execute_handler_tests('/path/path_includes_burning_elite_on_desired_path.json', ['choose 0'])
