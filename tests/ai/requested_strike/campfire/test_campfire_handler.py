from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler


class CampfireHandlerTestCase(RsTestHandlerFixture):
    handler = CommonCampfireHandler

    def test_rest(self):
        self.execute_handler_tests('/campfire/campfire_rest.json', ['choose rest'])

    def test_smith(self):
        self.execute_handler_tests('/campfire/campfire_smith.json', ['choose smith'])

    def test_rest_pantograph_boss(self):
        self.execute_handler_tests('/campfire/campfire_rest_pantograph_boss.json', ['choose rest'])

    def test_rest_pantograph_not_boss(self):
        self.execute_handler_tests('/campfire/campfire_rest_pantograph_not_boss.json', ['choose rest'])

    def test_smith_pantograph_boss(self):
        self.execute_handler_tests('/campfire/campfire_smith_pantograph_boss.json', ['choose smith'])

    def test_smith_pantograph_not_boss(self):
        self.execute_handler_tests('/campfire/campfire_smith_pantograph_not_boss.json', ['choose smith'])
