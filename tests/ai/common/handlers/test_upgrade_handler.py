from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.ai._example.handlers.upgrade_handler import UpgradeHandler


class TestUpgradeHandler(CoTestHandlerFixture):
    handler = UpgradeHandler

    def test_upgrade_bash(self):
        self.execute_handler_tests('/other/upgrade_apo.json', ['choose apotheosis'])
