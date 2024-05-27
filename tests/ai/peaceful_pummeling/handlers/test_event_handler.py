from ai.peaceful_pummeling.pp_test_handler_fixture import PpTestHandlerFixture
from rs.ai.peaceful_pummeling.handlers.event_handler import EventHandler


class TestEventHandler(PpTestHandlerFixture):
    handler = EventHandler

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

    def test_library_heal(self):
        self.execute_handler_tests('/event/event_library_heal.json', ['choose sleep', 'wait 30'])

    def test_library_grab_card(self):
        self.execute_handler_tests('/event/event_library_read.json', ['choose read', 'wait 30'])
