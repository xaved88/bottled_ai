from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_purge_handler import CommonPurgeHandler


class TestPurgeHandler(CoTestHandlerFixture):
    handler = CommonPurgeHandler

    def test_regular_purge(self):
        self.execute_handler_tests('/other/purge_regular.json', ['choose 3', 'wait 30'])

    def test_empty_cage(self):
        self.execute_handler_tests('/other/purge_empty_cage.json', ['choose 0', 'wait 30', 'choose 4', 'wait 30'])

    def test_event_bonfire_spirits(self):
        self.execute_handler_tests('/other/purge_bonfire_spirits.json', ['choose 2', 'wait 30'])
