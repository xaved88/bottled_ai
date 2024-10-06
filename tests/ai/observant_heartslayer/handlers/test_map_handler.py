from ai.observant_heartslayer.oh_test_handler_fixture import OhTestHandlerFixture
from rs.common.handlers.common_map_handler import CommonMapHandler


class MapHandlerTestCase(OhTestHandlerFixture):
    handler = CommonMapHandler

    def test_prefer_path_with_burning_elite(self):
        self.execute_handler_tests('/path/path_includes_burning_elite.json', ['choose 0'])

    def test_do_not_be_scared_of_burning_elite(self):
        self.execute_handler_tests('/path/path_includes_burning_elite_on_desired_path.json', ['choose 1'])
