from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.upgrade_handler import UpgradeHandler


class TestUpgradeHandler(RsTestHandlerFixture):
    handler = UpgradeHandler

    def test_upgrade_bash(self):
        self.execute_handler_tests('/other/upgrade_bash.json', ['choose bash'])
