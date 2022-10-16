import unittest

from rs.calculator.cards import CardId, get_card
from rs.calculator.hand_state import HandState
from rs.calculator.play_path import PlayPath, get_paths
from rs.calculator.powers import PowerId
from rs.calculator.targets import Player, Target, Monster


class CalculatorTestFixture(unittest.TestCase):

    def given_state(self, card_id: CardId, upgrade: int = 0, targets: int = 1, player_powers=None) -> HandState:
        return HandState(
            player=Player(50, 100, 0, {} if player_powers is None else player_powers, 5),
            hand=[get_card(card_id, None, upgrade)],
            monsters=[Monster(100, 100, 0, {}) for i in range(targets)]
        )

    def when_calculating_state_play(self, hand_state: HandState) -> PlayPath:
        paths = {}
        get_paths(PlayPath([], hand_state), paths)
        return list(paths.values())[-1]

    def see_enemy_lost_hp(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, 100 - play.state.monsters[enemy_index].current_hp)

    def see_enemy_block_is(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.monsters[enemy_index].block)

    def see_enemy_has_status(self, play: PlayPath, power_id: PowerId, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.monsters[enemy_index].powers.get(power_id, 0))

    def see_player_lost_hp(self, play: PlayPath, amount: int):
        self.assertEqual(amount, 50 - play.state.player.current_hp)

    def see_player_spent_energy(self, play: PlayPath, amount: int):
        self.assertEqual(amount, 5 - play.state.player.energy)

    def see_player_has_energy(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.player.energy)

    def see_player_gained_block(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.player.block)

    def see_player_has_status(self, play: PlayPath, power_id: PowerId, amount: int):
        self.assertEqual(amount, play.state.player.powers.get(power_id, 0))

    def see_cards_played(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.plays))

    def see_player_discard_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.discard_pile))

    def see_player_exhaust_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.exhaust_pile))

    def see_player_hand_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.hand))

    def see_player_drew_cards(self, play: PlayPath, amount: int, energy: int):
        card_id = CardId.DRAW_3P if energy >= 3 \
            else CardId.DRAW_2 if energy == 2 \
            else CardId.DRAW_1 if energy == 0 \
            else CardId.DRAW_0
        actual = len([1 for c in play.state.hand if c.id == card_id])
        self.assertEqual(amount, actual)

    def see_player_does_not_have_power(self, play: PlayPath, power_id: PowerId):
        self.assertEqual(None, play.state.player.powers.get(power_id))
