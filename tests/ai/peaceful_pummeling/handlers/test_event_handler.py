from ai.peaceful_pummeling.pp_test_handler_fixture import PpTestHandlerFixture
from rs.ai.peaceful_pummeling.handlers.event_handler import EventHandler


class TestEventHandler(PpTestHandlerFixture):
    handler = EventHandler

    def test_handle_divine_fountain(self):
        self.execute_handler_tests('/event/divine_fountain.json', ['choose 0', 'wait 30'])
        # tests the CommonEventHandler decision (it's modified in the Example strategy)

    # These Falling tests are here rather than the Common area because
    # this is the Strategy that the tests were originally set up for
    def test_falling(self):
        self.execute_handler_tests('/event/event_falling.json', ['choose 1', 'wait 30'])

    def test_falling_card_in_purge_list(self):
        self.execute_handler_tests('/event/event_falling_card_in_pickup_list.json', ['choose 1', 'wait 30'])

    def test_falling_card_not_in_pickup_list(self):
        self.execute_handler_tests('/event/event_falling_card_not_in_pickup_list.json', ['choose 2', 'wait 30'])

    def test_falling_card_in_pickup_list(self):
        self.execute_handler_tests('/event/event_falling_card_in_pickup_list.json', ['choose 1', 'wait 30'])

    def test_falling_with_disabled_option(self):
        self.execute_handler_tests('/event/event_falling_2_options.json', ['choose 1', 'wait 30'])
