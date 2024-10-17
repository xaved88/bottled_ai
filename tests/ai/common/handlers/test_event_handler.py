from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.ai._example.handlers.event_handler import EventHandler


class TestEventHandler(CoTestHandlerFixture):
    handler = EventHandler

    def test_handle_divine_fountain(self):
        self.execute_handler_tests('/event/divine_fountain.json', ['choose 1', 'wait 30'])
        # tests that an event choice is correctly overridden by a strategy-level decision

    def test_handle_purifier(self):
        self.execute_handler_tests('/event/event_purifier.json', ['choose 0', 'wait 30'])

    def test_cleric_purge(self):
        self.execute_handler_tests('/event/event_cleric_purge.json', ['choose purify', 'wait 30'])

    def test_cleric_heal(self):
        self.execute_handler_tests('/event/event_cleric_heal.json', ['choose heal', 'wait 30'])

    def test_cleric_leave(self):
        self.execute_handler_tests('/event/event_cleric_leave.json', ['choose leave', 'wait 30'])

    def test_council_of_ghosts(self):
        self.execute_handler_tests('/event/event_council_of_ghosts.json', ['choose accept', 'wait 30'])

    def test_council_of_ghosts_skip_because_we_have_bites(self):
        self.execute_handler_tests('/event/event_council_of_ghosts_with_bite.json', ['choose refuse', 'wait 30'])

    def test_vampires(self):
        self.execute_handler_tests('/event/vampires.json', ['choose accept', 'wait 30'])

    def test_vampires_with_apparition(self):
        self.execute_handler_tests('/event/vampires_with_apparition.json', ['choose refuse', 'wait 30'])

    def test_vampires_with_few_strikes(self):
        self.execute_handler_tests('/event/vampires_with_few_strikes.json', ['choose refuse', 'wait 30'])

    def test_vampires_with_many_strikes(self):
        self.execute_handler_tests('/event/vampires_with_many_strikes.json', ['choose accept', 'wait 30'])

    def test_library_heal(self):
        self.execute_handler_tests('/event/event_library_heal.json', ['choose sleep', 'wait 30'])
