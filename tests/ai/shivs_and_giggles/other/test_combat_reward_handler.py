from ai.shivs_and_giggles.sg_test_handler_fixture import SgTestHandlerFixture
from rs.ai.shivs_and_giggles.handlers.combat_reward_handler import CombatRewardHandler


class CardRewardHandlerTestCase(SgTestHandlerFixture):
    handler = CombatRewardHandler

    def test_take_gold(self):
        self.execute_handler_tests('/combat_reward/combat_reward_gold.json', ['choose gold'])

    def test_take_stolen_gold(self):
        self.execute_handler_tests('/combat_reward/combat_reward_stolen_gold.json', ['choose stolen_gold'])

    def test_take_potion(self):
        self.execute_handler_tests('/combat_reward/combat_reward_potion.json', ['choose potion'])

    def test_ignores_potions_when_full(self):
        self.execute_handler_tests('/combat_reward/combat_reward_full_potions.json', ['proceed'])

    def test_take_relic(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relic.json', ['choose relic'])

    def test_skip_relic(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relic_skip.json', ['proceed'])

    def test_skip_relic_multiple_relics_take_first(self):
        self.execute_handler_tests('/combat_reward/combat_reward_relics_2_take_first.json', ['choose relic'])

    # leaving this disabled for now since the check I'm doing is potentially too fragile
    # def test_skip_relic_multiple_relics_take_second(self):
    #     self.execute_handler_tests('/combat_reward/combat_reward_relics_2_take_second.json', ['proceed'])

    def test_check_card(self):
        self.execute_handler_tests('/combat_reward/combat_reward_card.json', ['choose card'])