from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import CardId, get_card
from rs.calculator.powers import PowerId


class CalculatorCardsTest(CalculatorTestFixture):

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
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 2)
        self.see_player_spent_energy(play, 2)

    def test_bash_upgraded(self):
        state = self.given_state(CardId.BASH, 1)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 3)
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
        self.see_enemy_has_status(play, PowerId.WEAK, 2)
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
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 1, enemy_index=0)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 1, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_twin_strike(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 1)

    def test_blood_for_blood(self):
        state = self.given_state(CardId.BLOOD_FOR_BLOOD)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_player_spent_energy(play, 4)

    def test_bloodletting(self):
        state = self.given_state(CardId.BLOODLETTING)
        play = self.when_calculating_state_play(state)
        self.see_player_lost_hp(play, 3)
        self.see_player_spent_energy(play, -2)

    def test_carnage(self):
        state = self.given_state(CardId.CARNAGE)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_spent_energy(play, 2)

    def test_uppercut(self):
        state = self.given_state(CardId.UPPERCUT)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_enemy_has_status(play, PowerId.WEAK, 1)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 1)
        self.see_player_spent_energy(play, 2)

    def test_disarm(self):
        state = self.given_state(CardId.DISARM)
        state.monsters[0].damage = 5
        state.monsters[0].hits = 2
        play = self.when_calculating_state_play(state)
        play.end_turn()
        self.see_player_lost_hp(play, 6)
        self.see_enemy_has_status(play, PowerId.STRENGTH, -2)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_dropkick_vs_normal(self):
        state = self.given_state(CardId.DROPKICK)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_spent_energy(play, 1)
        self.see_cards_played(play, 1)

    def test_dropkick_vs_vulnerable(self):
        state = self.given_state(CardId.DROPKICK)
        state.monsters[0].powers = {PowerId.VULNERABLE: 1}
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_spent_energy(play, 0)
        self.see_cards_played(play, 1)

    def test_entrench(self):
        state = self.given_state(CardId.ENTRENCH)
        state.player.block = 32
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 32)
        self.see_player_spent_energy(play, 2)

    def test_flame_barrier(self):
        state = self.given_state(CardId.FLAME_BARRIER)
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 12)
        self.see_player_has_status(play, PowerId.FLAME_BARRIER, 4)
        self.see_player_spent_energy(play, 2)

    def test_ghostly_armor(self):
        state = self.given_state(CardId.GHOSTLY_ARMOR)
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 10)
        self.see_player_spent_energy(play, 1)

    def test_hemokinesis(self):
        state = self.given_state(CardId.HEMOKINESIS)
        play = self.when_calculating_state_play(state)
        self.see_player_lost_hp(play, 2)
        self.see_enemy_lost_hp(play, 15)
        self.see_player_spent_energy(play, 1)

    def test_inflame(self):
        state = self.given_state(CardId.INFLAME)
        play = self.when_calculating_state_play(state)
        self.see_player_has_status(play, PowerId.STRENGTH, 2)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_intimidate(self):
        state = self.given_state(CardId.INTIMIDATE, targets=2)
        play = self.when_calculating_state_play(state)
        self.see_enemy_has_status(play, PowerId.WEAK, amount=1, enemy_index=0)
        self.see_enemy_has_status(play, PowerId.WEAK, amount=1, enemy_index=1)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_pummel(self):
        state = self.given_state(CardId.PUMMEL)
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_pummel_with_str_vs_plated_armor(self):  # technically everything is covered but a good systems check
        state = self.given_state(CardId.PUMMEL)
        state.player.powers[PowerId.STRENGTH] = 3
        state.monsters[0].powers[PowerId.PLATED_ARMOR] = 5
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_enemy_has_status(play, PowerId.PLATED_ARMOR, 1)

    def test_seeing_red(self):
        state = self.given_state(CardId.SEEING_RED)
        play = self.when_calculating_state_play(state)
        self.see_player_spent_energy(play, -1)
        self.see_player_exhaust_count(play, 1)

    def test_seeing_red_not_played_with_no_energy(self):
        state = self.given_state(CardId.SEEING_RED)
        state.player.energy = 0
        play = self.when_calculating_state_play(state)
        self.see_cards_played(play, 0)

    def test_shockwave(self):
        state = self.given_state(CardId.SHOCKWAVE, targets=2)
        play = self.when_calculating_state_play(state)
        self.see_enemy_has_status(play, PowerId.WEAK, amount=3, enemy_index=0)
        self.see_enemy_has_status(play, PowerId.WEAK, amount=3, enemy_index=1)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, amount=3, enemy_index=0)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, amount=3, enemy_index=1)
        self.see_player_spent_energy(play, 2)
        self.see_player_exhaust_count(play, 1)
