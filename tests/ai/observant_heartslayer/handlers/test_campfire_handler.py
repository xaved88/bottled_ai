from ai.observant_heartslayer.oh_test_handler_fixture import OhTestHandlerFixture
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler


class CampfireHandlerTestCase(OhTestHandlerFixture):
    handler = CommonCampfireHandler

    def test_recall_if_slay_heart(self):
        self.execute_handler_tests('/campfire/campfire_recall.json', ['choose recall'])

    def test_last_recall_possibility(self):
        self.execute_handler_tests('/campfire/campfire_recall_last_possibility.json', ['choose recall'])

    def test_should_not_recall(self):
        self.execute_handler_tests('/campfire/campfire_should_not_recall.json', ['choose rest'])

    def test_recall_not_available(self):
        self.execute_handler_tests('/campfire/campfire_recall_not_available.json', ['choose smith'])
