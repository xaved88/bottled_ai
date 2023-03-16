from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.smart_battle_handler import SmartBattleHandler


class SmartBattleHandlerTestCase(SgTestHandlerFixture):
    handler = SmartBattleHandler

    def test_discard_works_correctly(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard.json', ['choose 1'])

    def test_smart_battle_says_confirm_after_discards_are_chosen(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard_confirm.json', ['confirm', 'wait 30'])
