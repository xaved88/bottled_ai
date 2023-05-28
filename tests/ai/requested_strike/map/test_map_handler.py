from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.common_map_handler import CommonMapHandler


class MapHandlerTestCase(RsTestHandlerFixture):
    handler = CommonMapHandler

    def test_no_errors_on_basic(self):
        self.execute_handler_tests('/path/path_basic.json', ['choose 0'])
