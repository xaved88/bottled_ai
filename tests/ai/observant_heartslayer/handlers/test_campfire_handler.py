from ai.observant_heartslayer.oh_test_handler_fixture import OhTestHandlerFixture
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler


class CampfireHandlerTestCase(OhTestHandlerFixture):
    handler = CommonCampfireHandler

    def test_recall_if_slay_heart(self):
        self.execute_handler_tests('/campfire/campfire_recall.json', ['choose recall'])
