from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.ai.requested_strike.handlers.combat_reward_handler import CombatRewardHandler


class CombatRewardHandlerTestCase(RsTestHandlerFixture):
    handler = CombatRewardHandler

    def test_discards_potions_when_full(self):
        self.execute_handler_tests('/other/combat_reward_full_potions.json', ['potion discard 0'])
