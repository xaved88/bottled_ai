from ai.requested_scaling.exhaust_action.exhaust_test_fixture import ExhaustHandlerFixture
from rs.ai.requested_scaling.handlers.synergy_handlers.exhaust_action.exhaust_handler import ExhaustHandler


class ExhaustHandlerTest(ExhaustHandlerFixture):
    handler = ExhaustHandler

    def test_exhaust_a_defend_which_is_not_first_card_in_the_hand(self):
        self.execute_handler_tests('battles/synergy_states/exhaust_a_defend_which_is_not_first_card_in_hand.json', [])
