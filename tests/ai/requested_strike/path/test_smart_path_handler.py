from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.smart_path_handler import SmartPathHandler


class SmartPathHandlerTestCase(RsTestHandlerFixture):
    handler = SmartPathHandler

    def test_no_errors_on_basic(self):
        self.execute_handler_tests('/path/path_basic.json', ['choose 0'])
