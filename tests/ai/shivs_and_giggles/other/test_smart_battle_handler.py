from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.smart_battle_handler import SmartBattleHandler


class SmartBattleHandlerTestCase(SgTestHandlerFixture):
    handler = SmartBattleHandler

    def test_discard_works_correctly(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard.json',
                                   ['choose 1', 'confirm', 'wait 30'])

    def test_discard_is_okay_with_no_cards(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_discard_no_cards.json', [])

    def test_attacks_into_block_when_barricade_is_up(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_attack_barricade.json', ['play 1'])

    def test_plays_powers_when_nothing_better_to_do(self):
        self.execute_handler_tests('/battles/smart_battle/smart_battle_play_powers.json', ['play 3'])
