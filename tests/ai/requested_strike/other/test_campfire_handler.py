from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.campfire_handler import CampfireHandler


class CampfireHandlerTestCase(RsTestHandlerFixture):
    handler = CampfireHandler

    def test_rest(self):
        self.execute_handler_tests('/other/campfire_rest.json', ['choose 0'])

    def test_smith(self):
        self.execute_handler_tests('/other/campfire_smith.json', ['choose 1'])
