from ai.shivs_and_giggles.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.upgrade_handler import UpgradeHandler


class TestUpgradeHandler(RsTestHandlerFixture):
    handler = UpgradeHandler

    def test_upgrade_terror(self):
        self.execute_handler_tests('/other/shivs_and_giggles_upgrade_terror.json', ['choose terror'])

    def test_upgrade_snecko_eye_not_terror(self):
        self.execute_handler_tests('/other/shivs_and_giggles_upgrade_snecko_eye_not_terror.json', ['choose die die die'])
