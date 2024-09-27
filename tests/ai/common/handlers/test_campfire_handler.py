from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_campfire_handler import CommonCampfireHandler


class CampfireHandlerTestCase(CoTestHandlerFixture):
    handler = CommonCampfireHandler

    def test_rest(self):
        self.execute_handler_tests('/campfire/campfire_rest.json', ['choose rest'])

    def test_rest_we_do_not_have_pantograph(self):
        self.execute_handler_tests('/campfire/campfire_rest_without_pantograph_boss.json', ['choose rest'])

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

    def test_lift(self):
        self.execute_handler_tests('/campfire/campfire_girya_lift.json', ['choose lift'])

    def test_rest_despite_girya(self):
        self.execute_handler_tests('/campfire/campfire_girya_rest.json', ['choose rest'])

    def test_smith_despite_girya_because_deck(self):
        self.execute_handler_tests('/campfire/campfire_girya_smith_because_deck.json', ['choose smith'])

    def test_smith_despite_girya_because_counter(self):
        self.execute_handler_tests('/campfire/campfire_girya_smith_because_counter.json', ['choose smith'])

    def test_default_because_nothing_matches(self):
        self.execute_handler_tests('/campfire/campfire_default_because_options_blocked.json', ['choose 0'])

    def test_dig(self):
        self.execute_handler_tests('/campfire/campfire_dig.json', ['choose dig'])

    def test_toke(self):
        self.execute_handler_tests('/campfire/campfire_toke.json', ['choose toke'])

    def test_toke_do_not_toke_because_curse_cannot_be_removed(self):
        self.execute_handler_tests('/campfire/campfire_do_not_toke.json', ['choose dig'])

    def test_dig_because_cannot_smith(self):
        self.execute_handler_tests('/campfire/campfire_cannot_smith_so_dig.json', ['choose dig'])

    def test_toke_because_cannot_smith(self):
        self.execute_handler_tests('/campfire/campfire_cannot_smith_so_toke.json', ['choose toke'])

    # we had it hard-coded to _always_ try to rest on floor 49...
    def test_cannot_rest_floor_49_because_coffee_dripper(self):
        self.execute_handler_tests('/campfire/campfire_cannot_rest_because_coffee.json', ['choose smith'])

    def test_rest_floor_49(self):
        self.execute_handler_tests('/campfire/campfire_rest_floor_49.json', ['choose rest'])

    def test_no_rest_floor_49(self):
        self.execute_handler_tests('/campfire/campfire_do_not_rest_floor_49.json', ['choose smith'])

    def test_pantograph_no_rest_floor_49(self):
        self.execute_handler_tests('/campfire/campfire_do_not_rest_pantograph_floor_49.json', ['choose smith'])

    def test_no_recall_if_not_slay_heart(self):
        self.execute_handler_tests('/campfire/campfire_recall.json', ['choose smith'])
