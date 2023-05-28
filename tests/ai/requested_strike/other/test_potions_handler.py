import unittest

from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.potions_handler import PotionsEliteHandler, PotionsBossHandler
from rs.common.handlers.common_battle_handler import CommonBattleHandler


class PotionsHandlerTestCase(RsTestHandlerFixture):
    def test_elite_potions_handler(self):
        self.handler = PotionsEliteHandler
        self.execute_handler_tests('/other/potions_elite.json', ['wait 30', 'potion use 0 0', 'wait 30'])

    def test_potions_dead_minions(self):
        self.handler = PotionsEliteHandler
        self.execute_handler_tests('/other/potions_dead_minions.json', ['wait 30', 'potion use 1 4', 'wait 30'])

    def test_potions_reptomancer(self):
        self.handler = PotionsEliteHandler
        self.execute_handler_tests('/other/potions_reptomancer.json', ['wait 30', 'potion use 1 3', 'wait 30'])

    def test_boss_potions_handler(self):
        self.handler = PotionsBossHandler
        self.execute_handler_tests('/other/potions_boss.json', ['wait 30', 'potion use 0 0', 'wait 30'])

    def test_do_not_use_potion(self):
        self.handler = CommonBattleHandler
        self.execute_handler_tests('/other/potions_boss_disliked_potion.json', ['play 4 0'])


if __name__ == '__main__':
    unittest.main()
