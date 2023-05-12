from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.campfire_handler import CampfireHandler


class CampfireHandlerTestCase(SgTestHandlerFixture):
    handler = CampfireHandler

    def test_rest(self):
        self.execute_handler_tests('/campfire/campfire_rest.json', ['choose 0'])

    def test_smith(self):
        self.execute_handler_tests('/campfire/campfire_smith.json', ['choose smith'])

    def test_rest_pantograph_boss(self):
        self.execute_handler_tests('/campfire/campfire_rest_pantograph_boss.json', ['choose 0'])

    def test_rest_pantograph_not_boss(self):
        self.execute_handler_tests('/campfire/campfire_rest_pantograph_not_boss.json', ['choose 0'])

    def test_smith_pantograph_boss(self):
        self.execute_handler_tests('/campfire/campfire_smith_pantograph_boss.json', ['choose smith'])

    def test_smith_pantograph_not_boss(self):
        self.execute_handler_tests('/campfire/campfire_smith_pantograph_not_boss.json', ['choose smith'])

    def test_lift(self):
        self.execute_handler_tests('/campfire/campfire_girya_lift.json', ['choose lift'])

    def test_rest_despite_girya(self):
        self.execute_handler_tests('/campfire/campfire_girya_rest.json', ['choose 0'])

    def test_smith_despite_girya_because_deck(self):
        self.execute_handler_tests('/campfire/campfire_girya_smith_because_deck.json', ['choose smith'])

    def test_smith_despite_girya_because_counter(self):
        self.execute_handler_tests('/campfire/campfire_girya_smith_because_counter.json', ['choose smith'])
