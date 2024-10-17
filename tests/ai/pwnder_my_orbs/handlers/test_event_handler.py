from ai.pwnder_my_orbs.pmo_test_handler_fixture import PmoTestHandlerFixture
from rs.ai.pwnder_my_orbs.handlers.event_handler import EventHandler


class TestEventHandler(PmoTestHandlerFixture):
    handler = EventHandler

    def test_falling(self):
        self.execute_handler_tests('/event/event_falling_pmo.json', ['choose 2', 'wait 30'])
