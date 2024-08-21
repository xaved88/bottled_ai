from ai.common.co_test_handler_fixture import CoTestHandlerFixture
from rs.common.handlers.common_mass_discard_handler import CommonMassDiscardHandler


class TestMassDiscardHandler(CoTestHandlerFixture):
    handler = CommonMassDiscardHandler

    def test_handle_mass_discard_with_relic(self):
        self.execute_handler_tests('/other/discard_relic.json', ['choose strike'])

    def test_handle_mass_discard_with_relic_curse(self):
        self.execute_handler_tests('/other/discard_relic_curse.json', ['choose pain'])

    def test_handle_mass_discard_with_relic_done(self):
        self.execute_handler_tests('/other/discard_relic_done.json', ['confirm'])

    def test_handle_mass_discard_everything_discarded(self):
        self.execute_handler_tests('/other/discarded_everything.json', ['confirm'])
