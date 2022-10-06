import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.potions_handler import PotionsEliteHandler


class PotionsHandlerTestCase(RsTestHandlerFixture):
    def test_elite_potions_handler(self):
        self.handler = PotionsEliteHandler
        self.execute_handler_tests('/other/potions_elite.json', ['wait 30', 'potion use 0 0', 'wait 30'])


if __name__ == '__main__':
    unittest.main()
