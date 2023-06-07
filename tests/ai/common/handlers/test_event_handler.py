from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.ai._example.handlers.event_handler import EventHandler


class TestEventHandler(CoTestHandlerFixture):
    handler = EventHandler

    def test_handle_purifier(self):
        self.execute_handler_tests('/other/event_purifier.json', ['choose 0', 'wait 30'])

    def test_cleric_purge(self):
        self.execute_handler_tests('/event/event_cleric_purge.json', ['choose purify', 'wait 30'])

    def test_cleric_heal(self):
        self.execute_handler_tests('/event/event_cleric_heal.json', ['choose heal', 'wait 30'])

    def test_cleric_leave(self):
        self.execute_handler_tests('/event/event_cleric_leave.json', ['choose leave', 'wait 30'])