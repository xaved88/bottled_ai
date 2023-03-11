from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import CardId, get_card
from rs.calculator.powers import PowerId


class CalculatorCardsTest(CalculatorTestFixture):

    def test_strike_r(self):
        state = self.given_state(CardId.STRIKE_R)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)

    def test_strike_r_upgraded(self):
        state = self.given_state(CardId.STRIKE_R, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_spent_energy(play, 1)

    def test_defend_r(self):
        state = self.given_state(CardId.DEFEND_R)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 5)

    def test_defend_r_upgraded(self):
        state = self.given_state(CardId.DEFEND_R, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 8)

    def test_strike_g(self):
        state = self.given_state(CardId.STRIKE_G)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)

    def test_strike_g_upgraded(self):
        state = self.given_state(CardId.STRIKE_G, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_spent_energy(play, 1)

    def test_defend_g(self):
        state = self.given_state(CardId.DEFEND_G)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 5)

    def test_defend_g_upgraded(self):
        state = self.given_state(CardId.DEFEND_G, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 8)

    def test_bash(self):
        state = self.given_state(CardId.BASH)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)
        self.see_player_spent_energy(play, 2)

    def test_bash_upgraded(self):
        state = self.given_state(CardId.BASH, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 3)
        self.see_player_spent_energy(play, 2)

    def test_anger(self):
        state = self.given_state(CardId.ANGER)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 0)

    def test_cleave(self):
        state = self.given_state(CardId.CLEAVE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8, enemy_index=0)
        self.see_enemy_lost_hp(play, 8, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_clothesline(self):
        state = self.given_state(CardId.CLOTHESLINE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)
        self.see_player_spent_energy(play, 2)

    def test_heavy_blade(self):
        state = self.given_state(CardId.HEAVY_BLADE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 2)

    def test_heavy_blade_with_strength(self):
        state = self.given_state(CardId.HEAVY_BLADE, player_powers={PowerId.STRENGTH: 3})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 21)
        self.see_player_spent_energy(play, 2)

    def test_heavy_blade_upgraded_with_strength(self):
        state = self.given_state(CardId.HEAVY_BLADE, upgrade=1, player_powers={PowerId.STRENGTH: 3})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 27)
        self.see_player_spent_energy(play, 2)

    def test_iron_wave(self):
        state = self.given_state(CardId.IRON_WAVE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_has_block(play, 5)
        self.see_player_spent_energy(play, 1)

    def test_perfected_strike(self):
        state = self.given_state(CardId.PERFECTED_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 2)

    def test_perfected_strike_with_strikes_and_other_cards(self):
        state = self.given_state(CardId.PERFECTED_STRIKE)
        state.discard_pile.append(get_card(CardId.BASH))
        state.discard_pile.append(get_card(CardId.POMMEL_STRIKE))
        state.draw_pile.append(get_card(CardId.BASH))
        state.draw_pile.append(get_card(CardId.PERFECTED_STRIKE))
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 2)

    def test_pommel_strike(self):
        state = self.given_state(CardId.POMMEL_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_shrug_it_off(self):
        state = self.given_state(CardId.SHRUG_IT_OFF)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 8)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_thunderclap(self):
        state = self.given_state(CardId.THUNDERCLAP, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 4, enemy_index=0)
        self.see_enemy_lost_hp(play, 4, enemy_index=1)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 1, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 1, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_twin_strike(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 1)

    def test_blood_for_blood(self):
        state = self.given_state(CardId.BLOOD_FOR_BLOOD)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_player_spent_energy(play, 4)

    def test_bloodletting(self):
        state = self.given_state(CardId.BLOODLETTING)
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 3)
        self.see_player_spent_energy(play, -2)

    def test_carnage(self):
        state = self.given_state(CardId.CARNAGE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_spent_energy(play, 2)

    def test_uppercut(self):
        state = self.given_state(CardId.UPPERCUT)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 1)
        self.see_player_spent_energy(play, 2)

    def test_disarm(self):
        state = self.given_state(CardId.DISARM)
        state.monsters[0].damage = 5
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 6)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -2)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_dropkick_vs_normal(self):
        state = self.given_state(CardId.DROPKICK)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_spent_energy(play, 1)
        self.see_cards_played(play, 1)
        self.see_player_hand_count(play, 0)
        self.see_player_drew_cards(play, 0)

    def test_dropkick_vs_vulnerable(self):
        state = self.given_state(CardId.DROPKICK)
        state.monsters[0].powers = {PowerId.VULNERABLE: 1}
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_spent_energy(play, 0)
        self.see_cards_played(play, 1)
        self.see_player_hand_count(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_entrench(self):
        state = self.given_state(CardId.ENTRENCH)
        state.player.block = 32
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 64)
        self.see_player_spent_energy(play, 2)

    def test_flame_barrier(self):
        state = self.given_state(CardId.FLAME_BARRIER)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 12)
        self.see_player_has_power(play, PowerId.FLAME_BARRIER, 4)
        self.see_player_spent_energy(play, 2)

    def test_ghostly_armor(self):
        state = self.given_state(CardId.GHOSTLY_ARMOR)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 10)
        self.see_player_spent_energy(play, 1)

    def test_hemokinesis(self):
        state = self.given_state(CardId.HEMOKINESIS)
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 2)
        self.see_enemy_lost_hp(play, 15)
        self.see_player_spent_energy(play, 1)

    def test_inflame(self):
        state = self.given_state(CardId.INFLAME)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_intimidate(self):
        state = self.given_state(CardId.INTIMIDATE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.WEAKENED, amount=1, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, amount=1, enemy_index=1)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_pummel(self):
        state = self.given_state(CardId.PUMMEL)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_pummel_with_str_vs_plated_armor(self):  # technically everything is covered but a good systems check
        state = self.given_state(CardId.PUMMEL)
        state.player.powers[PowerId.STRENGTH] = 3
        state.monsters[0].powers[PowerId.PLATED_ARMOR] = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_enemy_has_power(play, PowerId.PLATED_ARMOR, 1)

    def test_seeing_red(self):
        state = self.given_state(CardId.SEEING_RED)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -1)
        self.see_player_exhaust_count(play, 1)

    def test_seeing_red_not_played_with_no_energy(self):
        state = self.given_state(CardId.SEEING_RED)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_cards_played(play, 0)

    def test_shockwave(self):
        state = self.given_state(CardId.SHOCKWAVE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.WEAKENED, amount=3, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, amount=3, enemy_index=1)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, amount=3, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, amount=3, enemy_index=1)
        self.see_player_spent_energy(play, 2)
        self.see_player_exhaust_count(play, 1)

    def test_bludgeon(self):
        state = self.given_state(CardId.BLUDGEON)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_enemy_lost_hp(play, 32)

    def test_feed(self):
        state = self.given_state(CardId.FEED)
        state.player.max_hp = 10
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 10)
        self.assertEqual(10, play.state.player.max_hp)
        self.see_player_exhaust_count(play, 1)

    def test_feed_on_kill(self):
        state = self.given_state(CardId.FEED)
        state.player.current_hp = 10
        state.player.max_hp = 10
        state.monsters[0].current_hp = 9
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(13, play.state.player.max_hp)
        self.assertEqual(13, play.state.player.current_hp)

    def test_fiend_fire(self):
        state = self.given_state(CardId.FIEND_FIRE)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_exhaust_count(play, 2)
        self.see_player_hand_count(play, 0)
        self.see_cards_played(play, 1)

    def test_fiend_fire_with_large_hand(self):
        state = self.given_state(CardId.FIEND_FIRE)
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 42)
        self.see_player_exhaust_count(play, 7)
        self.see_player_hand_count(play, 0)
        self.see_cards_played(play, 1)

    def test_immolate(self):
        state = self.given_state(CardId.IMMOLATE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 21, 0)
        self.see_enemy_lost_hp(play, 21, 1)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_count(play, 2)

    def test_impervious(self):
        state = self.given_state(CardId.IMPERVIOUS)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 30)
        self.see_player_spent_energy(play, 2)
        self.see_player_exhaust_count(play, 1)

    def test_limit_break(self):
        state = self.given_state(CardId.LIMIT_BREAK, player_powers={PowerId.STRENGTH: 3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 6)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_limit_break_upgraded(self):
        state = self.given_state(CardId.LIMIT_BREAK, upgrade=1, player_powers={PowerId.STRENGTH: 3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 6)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 0)
        self.see_player_discard_count(play, 1)

    def test_limit_break_no_strength(self):
        state = self.given_state(CardId.LIMIT_BREAK)
        play = self.when_playing_the_first_card(state)
        self.see_player_does_not_have_power(play, PowerId.STRENGTH)

    def test_limit_break_negative_strength(self):
        state = self.given_state(CardId.LIMIT_BREAK, player_powers={PowerId.STRENGTH: -3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, -6)

    def test_offering(self):
        state = self.given_state(CardId.OFFERING)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_has_energy(play, 2)
        self.see_player_lost_hp(play, 6)
        self.see_player_exhaust_count(play, 1)
        self.see_player_hand_count(play, 3)
        self.see_player_drew_cards(play, 3)

    def test_jax(self):
        state = self.given_state(CardId.JAX)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_lost_hp(play, 3)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)

    def test_jax_when_having_strength(self):
        state = self.given_state(CardId.JAX, player_powers={PowerId.STRENGTH: 2})
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_lost_hp(play, 3)
        self.see_player_has_power(play, PowerId.STRENGTH, 4)

    def test_body_slam(self):
        state = self.given_state(CardId.BODY_SLAM)
        state.player.block = 22
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 22)

    def test_clash_with_another_attack(self):
        state = self.given_state(CardId.CLASH)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.hand[1].cost = 99
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_discard_count(play, 1)

    def test_clash_with_a_skill(self):
        state = self.given_state(CardId.CLASH)
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand[1].cost = 99
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_discard_count(play, 0)

    def test_flex(self):
        state = self.given_state(CardId.FLEX)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)

    def test_wild_strike(self):
        state = self.given_state(CardId.WILD_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_discard_count(play, 1)
        self.see_player_draw_pile_count(play, 1)

    def test_battle_trance(self):
        state = self.given_state(CardId.BATTLE_TRANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_count(play, 1)
        self.see_player_drew_cards(play, 3)

    def test_rage(self):
        state = self.given_state(CardId.RAGE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.RAGE, 3)

    def test_rampage(self):
        state = self.given_state(CardId.RAMPAGE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)

    def test_metallicize(self):
        state = self.given_state(CardId.METALLICIZE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.METALLICIZE, 3)

    def test_reckless_charge(self):
        state = self.given_state(CardId.RECKLESS_CHARGE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_draw_pile_count(play, 1)

    def test_power_through(self):
        state = self.given_state(CardId.POWER_THROUGH)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 15)
        self.see_player_hand_count(play, 2)

    def test_power_through_with_full_hand(self):
        state = self.given_state(CardId.POWER_THROUGH)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 15)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_count(play, 2)

    def test_spot_weakness_against_attacking_enemy(self):
        state = self.given_state(CardId.SPOT_WEAKNESS)
        state.monsters[0].damage = 0
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 3)

    def test_spot_weakness_against_idle_enemy(self):
        state = self.given_state(CardId.SPOT_WEAKNESS)
        play = self.when_playing_the_first_card(state)
        self.see_player_does_not_have_power(play, PowerId.STRENGTH)

    def test_reaper(self):
        state = self.given_state(CardId.REAPER, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 4)
        self.see_enemy_lost_hp(play, 4, 1)
        self.see_player_lost_hp(play, -8)

    def test_reaper_does_not_heal_through_block(self):
        state = self.given_state(CardId.REAPER)
        state.monsters[0].block = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 1)
        self.see_player_lost_hp(play, -1)

    def test_bandage_up(self):
        state = self.given_state(CardId.BANDAGE_UP)
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, -4)

    def test_dark_shackles(self):
        state = self.given_state(CardId.DARK_SHACKLES)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -9)

    def test_flash_of_steel(self):
        state = self.given_state(CardId.FLASH_OF_STEEL)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_player_discard_count(play, 1)
        self.see_player_drew_cards(play, 1)
        self.see_player_spent_energy(play, 0)

    def test_swift_strike(self):
        state = self.given_state(CardId.SWIFT_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_discard_count(play, 1)
        self.see_player_spent_energy(play, 0)

    def test_trip(self):
        state = self.given_state(CardId.TRIP)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)

    def test_upgraded_trip(self):
        state = self.given_state(CardId.TRIP, upgrade=1, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2, 1)

    def test_apotheosis(self):
        state = self.given_state(CardId.APOTHEOSIS)
        state.draw_pile.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        self.assertEqual(play.state.draw_pile[0].upgrade, 1)
        self.see_player_exhaust_count(play, 1)

    def test_hand_of_greed(self):
        state = self.given_state(CardId.HAND_OF_GREED)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)

    def test_master_of_strategy(self):
        state = self.given_state(CardId.MASTER_OF_STRATEGY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 3)
        self.see_player_exhaust_count(play, 1)

    def test_apparition(self):
        state = self.given_state(CardId.APPARITION)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.INTANGIBLE, 1)

    def test_slimed(self):
        state = self.given_state(CardId.SLIMED)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_pain(self):
        state = self.given_state(CardId.PAIN)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 1)

    def test_regret(self):
        state = self.given_state(CardId.REGRET)
        for i in range(4):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 5)

    def test_neutralize(self):
        state = self.given_state(CardId.NEUTRALIZE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        self.see_player_spent_energy(play, 0)

    def test_shiv(self):
        state = self.given_state(CardId.SHIV)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 4)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_terror(self):
        state = self.given_state(CardId.TERROR)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 99)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_terror_upgraded(self):
        state = self.given_state(CardId.TERROR, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 99)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_adrenaline(self):
        state = self.given_state(CardId.ADRENALINE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -1)
        self.see_player_hand_count(play, 2)
        self.see_player_drew_cards(play, 2)

    def test_die_die_die(self):
        state = self.given_state(CardId.DIE_DIE_DIE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 13, enemy_index=0)
        self.see_enemy_lost_hp(play, 13, enemy_index=1)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_blade_dance(self):
        state = self.given_state(CardId.BLADE_DANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 3)
        self.see_player_discard_count(play, 1)

    def test_blade_dance_with_full_hand(self):
        state = self.given_state(CardId.BLADE_DANCE)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_count(play, 3)

    def test_cloak_and_dagger_with_full_hand(self):
        state = self.given_state(CardId.CLOAK_AND_DAGGER)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_count(play, 1)

    def test_cloak_and_dagger_upgraded_with_full_hand(self):
        state = self.given_state(CardId.CLOAK_AND_DAGGER, 1)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_count(play, 2)

    def test_leg_sweep(self):
        state = self.given_state(CardId.LEG_SWEEP)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)
        self.see_player_has_block(play, 11)
        self.see_player_spent_energy(play, 2)

    def test_sucker_punch(self):
        state = self.given_state(CardId.SUCKER_PUNCH)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        self.see_player_spent_energy(play, 1)

    def test_escape_plan(self):
        state = self.given_state(CardId.ESCAPE_PLAN)
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 1)
        self.see_player_discard_count(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_heel_hook_vs_vulnerable(self):
        state = self.given_state(CardId.HEEL_HOOK)
        state.monsters[0].powers = {PowerId.WEAKENED: 1}
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_spent_energy(play, 0)
        self.see_cards_played(play, 1)
        self.see_player_hand_count(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_dagger_spray(self):
        state = self.given_state(CardId.DAGGER_SPRAY, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8, enemy_index=0)
        self.see_enemy_lost_hp(play, 8, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_backstab(self):
        state = self.given_state(CardId.BACKSTAB)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 11)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_caltrops(self):
        state = self.given_state(CardId.CALTROPS)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.THORNS, 3)
        self.see_player_spent_energy(play, 1)

    def test_a_thousand_cuts(self):
        state = self.given_state(CardId.A_THOUSAND_CUTS)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.THOUSAND_CUTS, 1)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_accuracy(self):
        state = self.given_state(CardId.ACCURACY)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ACCURACY, 4)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_shiv_damage_with_accuracy(self):
        state = self.given_state(CardId.SHIV)
        state.player.powers = {PowerId.ACCURACY: 4}
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ACCURACY, 4)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 8)

    def test_infinite_blades(self):
        state = self.given_state(CardId.INFINITE_BLADES)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.INFINITE_BLADES, 1)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_after_image(self):
        state = self.given_state(CardId.AFTER_IMAGE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.AFTER_IMAGE, 1)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_finesse(self):
        state = self.given_state(CardId.FINESSE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 1)
        self.see_player_has_block(play, 2)

    def test_dramatic_entrance(self):
        state = self.given_state(CardId.DRAMATIC_ENTRANCE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 8, enemy_index=0)
        self.see_enemy_lost_hp(play, 8, enemy_index=1)