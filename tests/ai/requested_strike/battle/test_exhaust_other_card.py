import unittest

from ai.requested_strike.requested_scaling.exhaust_test_fixture import ExhaustHandlerFixture
from rs.ai.requested_scaling.handlers.synergy_handlers.exhaust_handler import ExhaustHandler


class ExhaustHandlerTest(ExhaustHandlerFixture):
    handler = ExhaustHandler

    def test_exhaust_others(self):
        self.execute_handler_tests('battles/Synergies/learn_to_choose_cards.json', [])
