import unittest

from rs.calculator.cards import CardId, get_card
from rs.calculator.hand_state import HandState
from rs.calculator.play_path import PlayPath, get_paths
from rs.calculator.powers import PowerId
from rs.calculator.targets import Player, Target


class CalculatorTestFixture(unittest.TestCase):

    def given_state(self, card_id: CardId, upgrade: int = 0, targets: int = 1, player_powers=None) -> HandState:
        return HandState(
            player=Player(50, 100, 50, {} if player_powers is None else player_powers, 5),
            hand=[get_card(card_id, None, upgrade)],
            targets=[Target(100, 100, 0, {}) for i in range(targets)]
        )

    def when_calculating_state_play(self, hand_state: HandState) -> PlayPath:
        return get_paths(PlayPath([], hand_state))[-1]

    def see_enemy_lost_hp(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(amount,  100 - play.state.targets[enemy_index].current_hp)

    def see_enemy_has_debuff(self, play: PlayPath, power_id: PowerId, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.targets[enemy_index].powers.get(power_id, 0))

    def see_player_lost_hp(self, play: PlayPath, amount: int):
        self.assertEqual(amount, 50 - play.state.player.current_hp)

    def see_player_spent_energy(self, play: PlayPath, amount: int):
        self.assertEqual(amount, 5 - play.state.player.energy)

    def see_player_gained_block(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.player.block - 50)
