import unittest

from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.potions_handler import PotionsBossHandler, PotionsEliteHandler
from rs.ai.shivs_and_giggles.handlers.battle_handler import BattleHandler


class PotionsHandlerTestCase(SgTestHandlerFixture):

    def test_boss_potions_handler(self):
        self.handler = PotionsBossHandler
        self.execute_handler_tests('/other/potions_boss.json', ['wait 30', 'potion use 0 0', 'wait 30'])

    def test_do_not_use_potion(self):
        self.handler = BattleHandler
        self.execute_handler_tests('/other/potions_boss_disliked_potion.json', ['play 4 0'])


if __name__ == '__main__':
    unittest.main()
