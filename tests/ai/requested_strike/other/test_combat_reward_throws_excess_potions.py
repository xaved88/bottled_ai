from ai.requested_strike.rs_test_handler_fixture import RsTestHandlerFixture
from rs.common.handlers.common_combat_reward_handler import CommonCombatRewardHandler


class CombatRewardHandlerTestCase(RsTestHandlerFixture):
    handler = CommonCombatRewardHandler

    def test_discards_potions_when_full(self):
        self.execute_handler_tests('/combat_reward/combat_reward_full_potions.json', ['wait 30', 'potion discard 1'])
