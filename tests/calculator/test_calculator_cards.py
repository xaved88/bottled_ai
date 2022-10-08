import unittest

from rs.calculator.cards import CardId, get_card
from rs.calculator.hand_state import HandState
from rs.calculator.play_path import PlayPath, get_paths
from rs.calculator.powers import PowerId, Powers
from rs.calculator.targets import Player, Target


class CalculatorCardsTest(unittest.TestCase):

    ##############
    # Test cases #
    ##############

    def test_strike_r(self):
        state = self.given_state(CardId.STRIKE_R)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)

    def test_strike_r_upgraded(self):
        state = self.given_state(CardId.STRIKE_R, 1)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_spent_energy(play, 1)

    def test_defend_r(self):
        state = self.given_state(CardId.DEFEND_R)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_gained_block(play, 5)

    def test_defend_r_upgraded(self):
        state = self.given_state(CardId.DEFEND_R, 1)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_gained_block(play, 8)

    def test_bash(self):
        state = self.given_state(CardId.BASH)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_has_debuff(play, PowerId.VULNERABLE, 2)
        self.see_player_spent_energy(play, 2)

    def test_bash_upgraded(self):
        state = self.given_state(CardId.BASH, 1)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_enemy_has_debuff(play, PowerId.VULNERABLE, 3)
        self.see_player_spent_energy(play, 2)

    def test_anger(self):
        state = self.given_state(CardId.ANGER)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 0)

    def test_cleave(self):
        state = self.given_state(CardId.CLEAVE, targets=2)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 8, enemy_index=0)
        self.see_enemy_lost_hp(play, 8, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_clothesline(self):
        state = self.given_state(CardId.CLOTHESLINE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_enemy_has_debuff(play, PowerId.WEAK, 2)
        self.see_player_spent_energy(play, 2)

    def test_heavy_blade(self):
        state = self.given_state(CardId.HEAVY_BLADE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 2)

    def test_heavy_blade_with_strength(self):
        state = self.given_state(CardId.HEAVY_BLADE, player_powers={PowerId.STRENGTH: 3})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 21)
        self.see_player_spent_energy(play, 2)

    def test_heavy_blade_upgraded_with_strength(self):
        state = self.given_state(CardId.HEAVY_BLADE, upgrade=1, player_powers={PowerId.STRENGTH: 3})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 27)
        self.see_player_spent_energy(play, 2)

    def test_iron_wave(self):
        state = self.given_state(CardId.IRON_WAVE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_gained_block(play, 5)
        self.see_player_spent_energy(play, 1)

    def test_perfected_strike(self):
        state = self.given_state(CardId.PERFECTED_STRIKE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 2)

    def test_perfected_strike_with_strikes_and_other_cards(self):
        state = self.given_state(CardId.PERFECTED_STRIKE)
        state.discard_pile.append(get_card(CardId.BASH))
        state.discard_pile.append(get_card(CardId.POMMEL_STRIKE))
        state.draw_pile.append(get_card(CardId.BASH))
        state.draw_pile.append(get_card(CardId.PERFECTED_STRIKE))
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 2)

    def test_pommel_strike(self):
        state = self.given_state(CardId.POMMEL_STRIKE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_spent_energy(play, 1)

    def test_shrug_it_off(self):
        state = self.given_state(CardId.SHRUG_IT_OFF)
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 8)
        self.see_player_spent_energy(play, 1)

    def test_thunderclap(self):
        state = self.given_state(CardId.THUNDERCLAP, targets=2)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 4, enemy_index=0)
        self.see_enemy_lost_hp(play, 4, enemy_index=1)
        self.see_enemy_has_debuff(play, PowerId.VULNERABLE, 1, enemy_index=0)
        self.see_enemy_has_debuff(play, PowerId.VULNERABLE, 1, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_twin_strike(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 1)

    def test_twin_strike_with_strength(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.STRENGTH: 3})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 16)
        self.see_player_spent_energy(play, 1)

    ##################
    # Helper Methods #
    ##################

    def given_state(self, card_id: CardId, upgrade: int = 0, targets: int = 1, player_powers=None) -> HandState:
        return HandState(
            player=Player(50, 100, 50, {} if player_powers is None else player_powers, 5),
            hand=[get_card(card_id, None, upgrade)],
            targets=[Target(100, 100, 0, {}) for i in range(targets)]
        )

    def when_calculating_state_play(self, hand_state: HandState) -> PlayPath:
        return get_paths(PlayPath([], hand_state))[-1]

    def see_enemy_lost_hp(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(100 - amount, play.state.targets[enemy_index].current_hp)

    def see_enemy_has_debuff(self, play: PlayPath, power_id: PowerId, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.targets[enemy_index].powers.get(power_id, 0))

    def see_player_spent_energy(self, play: PlayPath, amount: int):
        self.assertEqual(5 - amount, play.state.player.energy)

    def see_player_gained_block(self, play: PlayPath, amount: int):
        self.assertEqual(50 + amount, play.state.player.block)
