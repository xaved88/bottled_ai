from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.common_purge_handler import CommonPurgeHandler


class TestPurgeHandler(RsTestHandlerFixture):
    handler = CommonPurgeHandler

    def test_regular_purge(self):
        self.execute_handler_tests('/other/purge_regular.json', ['choose 5', 'wait 30'])

    def test_empty_cage(self):
        self.execute_handler_tests('/other/purge_empty_cage.json', ['choose 5', 'wait 30', 'choose 6', 'wait 30'])
