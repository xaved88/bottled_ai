from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.event_handler import EventHandler


class TestUpgradeHandler(SgTestHandlerFixture):
    handler = EventHandler

    def test_cleric_purge(self):
        self.execute_handler_tests('/event/event_cleric_purge.json', ['choose purify', 'wait 30'])

    def test_cleric_heal(self):
        self.execute_handler_tests('/event/event_cleric_heal.json', ['choose heal', 'wait 30'])

    def test_cleric_leave(self):
        self.execute_handler_tests('/event/event_cleric_leave.json', ['choose leave', 'wait 30'])
