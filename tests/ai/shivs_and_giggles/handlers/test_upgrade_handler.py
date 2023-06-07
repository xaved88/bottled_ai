from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.upgrade_handler import UpgradeHandler


class TestUpgradeHandler(SgTestHandlerFixture):
    handler = UpgradeHandler

    def test_upgrade_terror(self):
        self.execute_handler_tests('/other/shivs_and_giggles_upgrade_terror.json', ['choose terror'])

    def test_upgrade_snecko_eye_not_terror(self):
        self.execute_handler_tests('/other/shivs_and_giggles_upgrade_snecko_eye_not_terror.json', ['choose die die die'])
