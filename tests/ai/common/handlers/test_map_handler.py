from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_map_handler import CommonMapHandler


class MapHandlerTestCase(CoTestHandlerFixture):
    handler = CommonMapHandler

    def test_no_errors_on_basic(self):
        self.execute_handler_tests('/path/path_basic.json', ['choose 0'])
