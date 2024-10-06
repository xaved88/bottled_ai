from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.memory_items import MemoryItem


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

    def test_block_cannot_exceed_990(self):
        state = self.given_state(CardId.DEFEND_R)
        state.player.block = 990
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 990)

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
        self.see_player_discard_pile_count(play, 0)
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
        self.see_player_discard_pile_count(play, 0)  # powers should not be discarded
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
        # Technically incorrect but we do not model Plated Armor adding block to monsters
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

    def test_feed_no_trigger_on_minion(self):
        state = self.given_state(CardId.FEED)
        state.player.current_hp = 10
        state.player.max_hp = 10
        state.monsters[0].current_hp = 9
        state.monsters[0].powers = {PowerId.MINION: 1}
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(10, play.state.player.max_hp)
        self.assertEqual(10, play.state.player.current_hp)

    def test_fiend_fire(self):
        state = self.given_state(CardId.FIEND_FIRE, player_powers={PowerId.FEEL_NO_PAIN: 1})
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_exhaust_count(play, 2)
        self.see_player_hand_count(play, 0)
        self.see_cards_played(play, 1)
        self.see_player_has_block(play, 2)

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
        self.see_player_discard_pile_count(play, 2)

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
        self.see_player_discard_pile_count(play, 1)

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
        self.see_player_discard_pile_count(play, 1)

    def test_clash_with_a_skill(self):
        state = self.given_state(CardId.CLASH)
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand[1].cost = 99
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_discard_pile_count(play, 0)

    def test_flex(self):
        state = self.given_state(CardId.FLEX)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)

    def test_wild_strike(self):
        state = self.given_state(CardId.WILD_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_discard_pile_count(play, 1)
        self.assertEqual(play.state.draw_pile[0].id, CardId.WOUND)
        self.see_player_draw_pile_count(play, 1)

    def test_battle_trance(self):
        state = self.given_state(CardId.BATTLE_TRANCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_drew_cards(play, 3)
        self.see_hand_card_is(play, CardId.CARD_FROM_DRAW)

    def test_burning_pact_does_not_exhaust_drawn_cards(self):
        state = self.given_state(CardId.BURNING_PACT)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 0)

    def test_burning_pact(self):
        state = self.given_state(CardId.BURNING_PACT)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_upgraded_burning_pact(self):
        state = self.given_state(CardId.BURNING_PACT, upgrade=1)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 3)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_rage(self):
        state = self.given_state(CardId.RAGE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.RAGE, 3)

    def test_rampage(self):
        state = self.given_state(CardId.RAMPAGE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(5, play.state.get_memory_by_card(CardId.RAMPAGE, "default"))

    def test_rampage_respects_and_increases_its_memory(self):
        state = self.given_state(CardId.RAMPAGE)
        state.add_memory_by_card(CardId.RAMPAGE, "default", 5)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(10, play.state.get_memory_by_card(CardId.RAMPAGE, "default"))

    def test_metallicize(self):
        state = self.given_state(CardId.METALLICIZE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.METALLICIZE, 3)

    def test_reckless_charge(self):
        state = self.given_state(CardId.RECKLESS_CHARGE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_draw_pile_count(play, 1)
        self.assertEqual(play.state.draw_pile[0].id, CardId.DAZED)

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
        self.see_player_discard_pile_count(play, 2)

    def test_spot_weakness_against_attacking_enemy(self):
        state = self.given_state(CardId.SPOT_WEAKNESS)
        state.monsters[0].damage = 0
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 3)

    def test_spot_weakness_against_idle_enemy(self):
        state = self.given_state(CardId.SPOT_WEAKNESS)
        state.monsters[0].damage = -1
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_does_not_have_power(play, PowerId.STRENGTH)

    def test_reaper(self):
        state = self.given_state(CardId.REAPER, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
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
        self.see_player_spent_energy(play, 0)
        self.see_player_lost_hp(play, -4)

    def test_dark_shackles(self):
        state = self.given_state(CardId.DARK_SHACKLES)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -9)

    def test_flash_of_steel(self):
        state = self.given_state(CardId.FLASH_OF_STEEL)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_drew_cards(play, 1)
        self.see_player_spent_energy(play, 0)

    def test_swift_strike(self):
        state = self.given_state(CardId.SWIFT_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_discard_pile_count(play, 1)
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
        self.see_player_has_power(play, PowerId.INTANGIBLE_PLAYER, 1)

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
        state.player.block = 3
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 5)

    def test_decay(self):
        state = self.given_state(CardId.DECAY)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 2)

    def test_multiple_decay(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.DECAY))
        state.hand.append(get_card(CardId.DECAY))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 4)

    def test_decay_blockable(self):
        state = self.given_state(CardId.DECAY)
        state.hand.append(get_card(CardId.DEFEND_G))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 0)

    def test_burn(self):
        state = self.given_state(CardId.BURN)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 2)

    def test_burn_and_burn_upgraded(self):
        state = self.given_state(CardId.BURN, upgrade=1)
        for i in range(3):
            state.hand.append(get_card(CardId.BURN))
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 10)

    def test_doubt(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.DOUBT))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_power(play, PowerId.WEAKENED, 1)

    def test_doubt_more(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.DOUBT))
        state.hand.append(get_card(CardId.DOUBT))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_power(play, PowerId.WEAKENED, 2)

    def test_shame(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.SHAME))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_power(play, PowerId.FRAIL, 1)

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
        self.see_player_discard_pile_count(play, 1)

    def test_blade_dance_with_full_hand(self):
        state = self.given_state(CardId.BLADE_DANCE)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_pile_count(play, 3)

    def test_cloak_and_dagger_with_full_hand(self):
        state = self.given_state(CardId.CLOAK_AND_DAGGER)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_pile_count(play, 1)

    def test_cloak_and_dagger_upgraded_with_full_hand(self):
        state = self.given_state(CardId.CLOAK_AND_DAGGER, 1)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_pile_count(play, 2)

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
        self.see_player_discard_pile_count(play, 1)
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
        self.see_enemy_lost_hp(play, 0)
        self.see_player_discard_pile_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_accuracy(self):
        state = self.given_state(CardId.ACCURACY)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ACCURACY, 4)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 0)  # powers should not be discarded
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
        self.see_player_discard_pile_count(play, 0)  # powers should not be discarded
        self.see_player_exhaust_count(play, 0)  # powers should not be exhausted

    def test_after_image(self):
        state = self.given_state(CardId.AFTER_IMAGE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.AFTER_IMAGE, 1)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 0)
        self.see_player_discard_pile_count(play, 0)  # powers should not be discarded
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

    def test_survivor(self):
        state = self.given_state(CardId.SURVIVOR)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 8)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 2)

    def test_survivor_when_it_is_the_last_card(self):
        state = self.given_state(CardId.SURVIVOR)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 8)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_poisoned_stab(self):
        state = self.given_state(CardId.POISONED_STAB)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 6)
        play.end_turn()
        self.see_enemy_lost_hp(play, 9)

    def test_upgraded_poisoned_stab(self):
        state = self.given_state(CardId.POISONED_STAB, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        play.end_turn()
        self.see_enemy_lost_hp(play, 12)

    def test_tools_of_the_trade(self):
        state = self.given_state(CardId.TOOLS_OF_THE_TRADE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.TOOLS_OF_THE_TRADE, 1)

    def test_storm_of_steel_with_no_cards(self):
        state = self.given_state(CardId.STORM_OF_STEEL)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_hand_count(play, 0)

    def test_storm_of_steel_with_many_cards(self):
        state = self.given_state(CardId.STORM_OF_STEEL)
        for _ in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 10)
        self.see_player_hand_count(play, 9)
        self.see_hand_card_is(play, CardId.SHIV)
        self.see_hand_card_upgrade(play, 0)

    def test_storm_of_steel_upgraded(self):
        state = self.given_state(CardId.STORM_OF_STEEL, upgrade=1)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_hand_count(play, 1)
        self.see_hand_card_is(play, CardId.SHIV)
        self.see_hand_card_upgrade(play, 1)

    def test_eviscerate(self):
        state = self.given_state(CardId.EVISCERATE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_enemy_lost_hp(play, 21)

    def test_eviscerate_cost_goes_down_with_a_discard(self):
        state = self.given_state(CardId.WOUND, amount_to_discard=1)
        state.hand.append(get_card(CardId.EVISCERATE))
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_hand_card_is(play, CardId.EVISCERATE)
        self.see_hand_card_cost(play, 2)

    def test_eviscerate_cost_goes_down_with_multiple_discards(self):
        state = self.given_state(CardId.UNLOAD)
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.EVISCERATE))
        play = self.when_playing_the_first_card(state)
        self.see_hand_card_is(play, CardId.EVISCERATE)
        self.see_hand_card_cost(play, 1)

    def test_sneaky_strike_without_discards(self):
        state = self.given_state(CardId.SNEAKY_STRIKE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 2)

    def test_sneaky_strike_when_cards_have_been_discarded(self):
        state = self.given_state(CardId.SNEAKY_STRIKE, cards_discarded_this_turn=1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 0)

    def test_sneaky_strike_when_cards_have_been_discarded_but_player_lacks_energy(self):
        state = self.given_state(CardId.SNEAKY_STRIKE, cards_discarded_this_turn=1)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_hand_count(play, 1)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_has_energy(play, 0)

    def test_prepared(self):
        state = self.given_state(CardId.PREPARED)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_hand_count(play, 1)

    def test_prepared_when_its_the_only_card(self):
        state = self.given_state(CardId.PREPARED)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_hand_count(play, 0)

    def test_dagger_throw(self):
        state = self.given_state(CardId.DAGGER_THROW)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_hand_count(play, 1)

    def test_dagger_throw_when_its_the_only_card(self):
        state = self.given_state(CardId.DAGGER_THROW)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_hand_count(play, 0)

    def test_unload_with_empty_hand(self):
        state = self.given_state(CardId.UNLOAD)
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_hand_count(play, 0)

    def test_unload_with_all_card_types(self):
        state = self.given_state(CardId.UNLOAD)
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.AFTER_IMAGE))
        state.hand.append(get_card(CardId.DEFEND_G))
        state.hand.append(get_card(CardId.STRIKE_G))
        state.hand.append(get_card(CardId.REGRET))
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 5)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_hand_count(play, 1)

    def test_crippling_cloud(self):
        state = self.given_state(CardId.CRIPPLING_CLOUD)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 4)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)

    def test_panacea(self):
        state = self.given_state(CardId.PANACEA)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_power(play, PowerId.ARTIFACT, 1)

    def test_backflip(self):
        state = self.given_state(CardId.BACKFLIP)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 5)
        self.see_player_hand_count(play, 2)

    def test_acrobatics(self):
        state = self.given_state(CardId.ACROBATICS)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 2)

    def test_deadly_poison(self):
        state = self.given_state(CardId.DEADLY_POISON)
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 5)
        self.see_enemy_has_power(play, PowerId.POISON, 4)

    def test_bite(self):
        state = self.given_state(CardId.BITE)
        state.monsters[0].damage = 5
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, -2)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 7)

    def test_good_instincts(self):
        state = self.given_state(CardId.GOOD_INSTINCTS)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 6)
        self.see_player_spent_energy(play, 0)

    def test_mind_blast_nothing_in_draw(self):
        state = self.given_state(CardId.MIND_BLAST)
        state.draw_pile.clear()
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_draw_pile_count(play, 0)
        self.see_enemy_lost_hp(play, 0)

    def test_mind_blast_one_in_draw(self):
        state = self.given_state(CardId.MIND_BLAST)
        state.draw_pile.clear()
        for i in range(5):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_draw_pile_count(play, 5)
        self.see_enemy_lost_hp(play, 5)

    def test_tactician(self):
        state = self.given_state(CardId.TACTICIAN, amount_to_discard=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_spent_energy(play, -1)

    def test_reflex(self):
        state = self.given_state(CardId.REFLEX, amount_to_discard=1)
        state.draw_pile.append(get_card(CardId.WOUND))
        state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_drew_cards(play, 2)

    def test_concentrate(self):
        state = self.given_state(CardId.CONCENTRATE, upgrade=1)
        state.player.energy = 0
        state.hand.append(get_card(CardId.DEFEND_R))  # On top so the others are discarded rather than this one
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 5)

    def test_flechettes_no_skills(self):
        state = self.given_state(CardId.FLECHETTES)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 0)

    def test_flechettes_multiple_skills(self):
        state = self.given_state(CardId.FLECHETTES)
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.DEFEND_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 12)

    def test_expertise(self):
        state = self.given_state(CardId.EXPERTISE)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 5)

    def test_expertise_draws_0(self):
        state = self.given_state(CardId.EXPERTISE)
        for i in range(6):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 0)

    def test_bane_no_poison(self):
        state = self.given_state(CardId.BANE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 7)

    def test_bane_yes_poison(self):
        state = self.given_state(CardId.BANE)
        state.monsters[0].powers[PowerId.POISON] = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 14)

    def test_bullet_time(self):
        state = self.given_state(CardId.BULLET_TIME, upgrade=1)
        state.player.energy = 2
        state.hand.append(get_card(CardId.BLUDGEON))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_energy(play, 0)
        self.see_enemy_lost_hp(play, 32)

    def test_choke(self):
        state = self.given_state(CardId.CHOKE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 12)
        self.see_enemy_has_power(play, PowerId.CHOKED, 3)

    def test_flying_knee(self):
        state = self.given_state(CardId.FLYING_KNEE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_has_power(play, PowerId.ENERGIZED, 1)

    def test_predator(self):
        state = self.given_state(CardId.PREDATOR)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 15)
        self.see_player_has_power(play, PowerId.DRAW_CARD, 2)

    def test_dodge_and_roll(self):
        state = self.given_state(CardId.DODGE_AND_ROLL)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 4)
        self.see_player_has_power(play, PowerId.NEXT_TURN_BLOCK, 4)

    def test_outmaneuver(self):
        state = self.given_state(CardId.OUTMANEUVER)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.ENERGIZED, 2)

    def test_envenom(self):
        state = self.given_state(CardId.ENVENOM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.ENVENOM, 1)

    def test_noxious_fumes(self):
        state = self.given_state(CardId.NOXIOUS_FUMES)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.NOXIOUS_FUMES, 2)

    def test_endless_agony(self):
        state = self.given_state(CardId.ENDLESS_AGONY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 4)

    def test_corpse_explosion(self):
        state = self.given_state(CardId.CORPSE_EXPLOSION)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.POISON, 6)
        self.see_enemy_has_power(play, PowerId.CORPSE_EXPLOSION, 1)

    def test_grand_finale_is_not_playable(self):
        state = self.given_state(CardId.GRAND_FINALE, targets=2)
        state.draw_pile.append(get_card(CardId.DEFEND_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_draw_pile_count(play, 1)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)

    def test_grand_finale_is_playable(self):
        state = self.given_state(CardId.GRAND_FINALE, targets=2)
        state.draw_pile.clear()
        play = self.when_playing_the_first_card(state)
        self.see_player_draw_pile_count(play, 0)
        self.see_enemy_lost_hp(play, 50, enemy_index=0)
        self.see_enemy_lost_hp(play, 50, enemy_index=1)

    def test_wraith_form(self):
        state = self.given_state(CardId.WRAITH_FORM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_has_power(play, PowerId.INTANGIBLE_PLAYER, 2)
        self.see_player_has_power(play, PowerId.WRAITH_FORM_POWER, 1)

    def test_piercing_wail(self):
        state = self.given_state(CardId.PIERCING_WAIL, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -6, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -6, enemy_index=1)

    def test_blur(self):
        state = self.given_state(CardId.BLUR)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 5)
        self.see_player_has_power(play, PowerId.BLUR, 1)

    def test_catalyst(self):
        state = self.given_state(CardId.CATALYST)
        state.monsters[0].powers[PowerId.POISON] = 2
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_has_power(play, PowerId.POISON, 4)

    def test_catalyst_upgraded(self):
        state = self.given_state(CardId.CATALYST, upgrade=1)
        state.monsters[0].powers[PowerId.POISON] = 2
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_has_power(play, PowerId.POISON, 6)

    def test_phantasmal_killer(self):
        state = self.given_state(CardId.PHANTASMAL_KILLER)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.PHANTASMAL, 1)

    def test_sword_boomerang_deals_damage_with_single_target(self):
        state = self.given_state(CardId.SWORD_BOOMERANG)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_random_damage_dealt(play, 0)

    def test_sword_boomerang_upgraded(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_random_damage_dealt(play, 0)

    def test_sword_boomerang_works_with_vulnerable(self):
        state = self.given_state(CardId.SWORD_BOOMERANG)
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_random_damage_dealt(play, 0)

    def test_sword_boomerang_see_random_damage_with_multiple_targets(self):
        state = self.given_state(CardId.SWORD_BOOMERANG, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 9)

    def test_juggernaut(self):
        state = self.given_state(CardId.JUGGERNAUT)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.JUGGERNAUT, 5)

    def test_juggernaut_upgraded(self):
        state = self.given_state(CardId.JUGGERNAUT, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.JUGGERNAUT, 7)

    def test_bouncing_flask_single_target(self):
        state = self.given_state(CardId.BOUNCING_FLASK)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.POISON, 9)

    def test_bouncing_flask_single_target_upgraded(self):
        state = self.given_state(CardId.BOUNCING_FLASK, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.POISON, 12)

    def test_bouncing_flask_multi_target(self):
        state = self.given_state(CardId.BOUNCING_FLASK, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.POISON, 0)
        self.assertEqual(play.state.total_random_poison_added, 9)

    def test_blind(self):
        state = self.given_state(CardId.BLIND, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 0, enemy_index=1)

    def test_blind_upgraded(self):
        state = self.given_state(CardId.BLIND, upgrade=1, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2, enemy_index=1)

    def test_deep_breath(self):
        state = self.given_state(CardId.DEEP_BREATH)
        for i in range(2):
            state.discard_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_drew_cards(play, 1)
        self.see_player_spent_energy(play, 0)
        self.see_player_draw_pile_count(play, 1)
        self.see_player_discard_pile_count(play, 1)

    def test_enlightenment(self):
        state = self.given_state(CardId.DASH)
        state.hand.append(get_card(CardId.DASH))
        state.hand.append(get_card(CardId.ENLIGHTENMENT))  # At the bottom to force this as first play
        state.player.energy = 2
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 20)

    def test_impatience_draws(self):
        state = self.given_state(CardId.IMPATIENCE)
        state.hand.append(get_card(CardId.DEFEND_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_drew_cards(play, 2)

    def test_impatience_does_not_draw(self):
        state = self.given_state(CardId.IMPATIENCE)
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_drew_cards(play, 0)

    def test_mayhem(self):
        state = self.given_state(CardId.MAYHEM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.MAYHEM, 1)

    def test_mayhem_upgraded(self):
        state = self.given_state(CardId.MAYHEM, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.MAYHEM, 1)

    def test_panache(self):
        state = self.given_state(CardId.PANACHE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.assertEqual(5, play.state.get_memory_value(MemoryItem.PANACHE_COUNTER))
        self.assertEqual(10, play.state.get_memory_value(MemoryItem.PANACHE_DAMAGE))
        self.see_player_has_power(play, PowerId.PANACHE_INTERNAL, 1)

    def test_panache_upgraded(self):
        state = self.given_state(CardId.PANACHE, upgrade=1)
        state.hand.append(get_card(CardId.PANACHE))
        play = self.when_making_the_most_plays(state)
        self.see_player_spent_energy(play, 0)
        self.assertEqual(4, play.state.get_memory_value(MemoryItem.PANACHE_COUNTER))
        self.assertEqual(24, play.state.get_memory_value(MemoryItem.PANACHE_DAMAGE))

    def test_sadistic_nature(self):
        state = self.given_state(CardId.SADISTIC_NATURE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_power(play, PowerId.SADISTIC, 5)

    def test_strike_b(self):
        state = self.given_state(CardId.STRIKE_B)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)

    def test_defend_B(self):
        state = self.given_state(CardId.DEFEND_B)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 5)

    def test_beam_cell(self):
        state = self.given_state(CardId.BEAM_CELL)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 1)
        self.see_player_spent_energy(play, 0)

    def test_leap(self):
        state = self.given_state(CardId.LEAP)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 9)

    def test_charge_battery(self):
        state = self.given_state(CardId.CHARGE_BATTERY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 7)
        self.see_player_has_power(play, PowerId.ENERGIZED, 1)

    def test_buffer(self):
        state = self.given_state(CardId.BUFFER)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.BUFFER, 1)

    def test_skim(self):
        state = self.given_state(CardId.SKIM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 3)

    def test_rip_and_tear_single_target(self):
        state = self.given_state(CardId.RIP_AND_TEAR)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 14)

    def test_rip_and_tear_multi_target(self):
        state = self.given_state(CardId.RIP_AND_TEAR, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_random_damage_dealt(play, 14)

    def test_sweeping_beam(self):
        state = self.given_state(CardId.SWEEPING_BEAM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 1)
        self.see_enemy_lost_hp(play, 6)

    def test_core_surge(self):
        state = self.given_state(CardId.CORE_SURGE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 11)
        self.see_player_has_power(play, PowerId.ARTIFACT, 1)
        self.see_player_exhaust_count(play, 1)

    def test_boot_sequence(self):
        state = self.given_state(CardId.BOOT_SEQUENCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_block(play, 10)
        self.see_player_exhaust_count(play, 1)

    def test_stack(self):
        state = self.given_state(CardId.STACK, player_powers={PowerId.DEXTERITY: 1})
        state.discard_pile.append(get_card(CardId.WOUND))
        state.discard_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 3)

    def test_auto_shields_without_block(self):
        state = self.given_state(CardId.AUTO_SHIELDS)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 11)

    def test_auto_shields_with_block(self):
        state = self.given_state(CardId.AUTO_SHIELDS)
        state.hand.append(get_card(CardId.DEFEND_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_block(play, 5)

    def test_streamline(self):
        state = self.given_state(CardId.STREAMLINE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 15)
        self.assertEqual(1, play.state.discard_pile[0].cost)

    def test_streamline_does_not_go_below_0(self):
        state = self.given_state(CardId.STREAMLINE)
        state.hand[0].cost = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 15)
        self.assertEqual(0, play.state.discard_pile[0].cost)

    def test_turbo(self):
        state = self.given_state(CardId.TURBO)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -2)
        self.see_player_discard_pile_count(play, 2)

    def test_aggregate_empty_draw(self):
        state = self.given_state(CardId.AGGREGATE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)

    def test_aggregate_7_in_draw(self):
        state = self.given_state(CardId.AGGREGATE)
        for i in range(7):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -1)

    def test_aggregate_9_in_draw(self):
        state = self.given_state(CardId.AGGREGATE)
        for i in range(9):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -2)

    def test_aggregate_upgraded_9_in_draw(self):
        state = self.given_state(CardId.AGGREGATE, upgrade=1)
        for i in range(9):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -3)

    def test_double_energy(self):
        state = self.given_state(CardId.DOUBLE_ENERGY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -3)

    def test_double_energy_upgraded(self):
        state = self.given_state(CardId.DOUBLE_ENERGY, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -5)

    def test_heatsinks(self):
        state = self.given_state(CardId.HEATSINKS)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.HEATSINK, 1)

    def test_overclock(self):
        state = self.given_state(CardId.OVERCLOCK)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 2)
        self.see_player_discard_pile_count(play, 2)

    def test_self_repair(self):
        state = self.given_state(CardId.SELF_REPAIR)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.REPAIR, 7)

    def test_machine_learning(self):
        state = self.given_state(CardId.MACHINE_LEARNING)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.MACHINE_LEARNING, 1)

    def test_electrodynamics(self):
        state = self.given_state(CardId.ELECTRODYNAMICS, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.ELECTRO, 1)
        self.see_orb_count(play, 2)
        self.see_orb_type_count(play, 2, OrbId.LIGHTNING)

    def test_electrodynamics_upgraded(self):
        state = self.given_state(CardId.ELECTRODYNAMICS, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.ELECTRO, 1)
        self.see_orb_count(play, 3)
        self.see_orb_type_count(play, 3, OrbId.LIGHTNING)

    def test_zap(self):
        state = self.given_state(CardId.ZAP, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.LIGHTNING)

    def test_upgraded_zap(self):
        state = self.given_state(CardId.ZAP, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.LIGHTNING)

    def test_dualcast(self):
        state = self.given_state(CardId.DUALCAST, orbs=[(OrbId.LIGHTNING, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 0)
        self.see_enemy_lost_hp(play, 16)

    def test_dualcast_with_no_orbs(self):
        state = self.given_state(CardId.DUALCAST, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 0)
        self.see_enemy_lost_hp(play, 0)

    def test_ball_lightning(self):
        state = self.given_state(CardId.BALL_LIGHTNING, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.LIGHTNING)
        self.see_enemy_lost_hp(play, 7)

    def test_ball_lightning_upgraded(self):
        state = self.given_state(CardId.BALL_LIGHTNING, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.LIGHTNING)
        self.see_enemy_lost_hp(play, 10)

    def test_coolheaded(self):
        state = self.given_state(CardId.COOLHEADED, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.FROST)
        self.see_player_drew_cards(play, 1)

    def test_coolheaded_upgraded(self):
        state = self.given_state(CardId.COOLHEADED, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.FROST)
        self.see_player_drew_cards(play, 2)

    def test_cold_snap(self):
        state = self.given_state(CardId.COLD_SNAP, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.FROST)
        self.see_enemy_lost_hp(play, 6)

    def test_cold_snap_upgraded(self):
        state = self.given_state(CardId.COLD_SNAP, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.FROST)
        self.see_enemy_lost_hp(play, 9)

    def test_doom_and_gloom(self):
        state = self.given_state(CardId.DOOM_AND_GLOOM, orb_slots=3, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.DARK)
        self.see_enemy_lost_hp(play, 10, enemy_index=0)
        self.see_enemy_lost_hp(play, 10, enemy_index=1)

    def test_doom_and_gloom_upgraded(self):
        state = self.given_state(CardId.DOOM_AND_GLOOM, upgrade=1, orb_slots=3, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.DARK)
        self.see_enemy_lost_hp(play, 14, enemy_index=0)
        self.see_enemy_lost_hp(play, 14, enemy_index=1)

    def test_glacier(self):
        state = self.given_state(CardId.GLACIER, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_count(play, 2)
        self.see_orb_type_count(play, 2, OrbId.FROST)
        self.see_player_has_block(play, 7)

    def test_glacier_upgraded(self):
        state = self.given_state(CardId.GLACIER, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_count(play, 2)
        self.see_orb_type_count(play, 2, OrbId.FROST)
        self.see_player_has_block(play, 10)

    def test_defragment(self):
        state = self.given_state(CardId.DEFRAGMENT)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FOCUS, 1)

    def test_defragment_upgraded(self):
        state = self.given_state(CardId.DEFRAGMENT, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FOCUS, 2)

    def test_biased_cognition(self):
        state = self.given_state(CardId.BIASED_COGNITION)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FOCUS, 4)
        self.see_player_has_power(play, PowerId.BIAS, 1)

    def test_capacitor(self):
        state = self.given_state(CardId.CAPACITOR, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_slots_count(play, 5)

    def test_capacitor_upgraded(self):
        state = self.given_state(CardId.CAPACITOR, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_slots_count(play, 6)

    def test_cannot_have_more_than_10_orb_slots(self):
        state = self.given_state(CardId.CAPACITOR, orb_slots=9)
        play = self.when_playing_the_first_card(state)
        self.see_orb_slots_count(play, 10)

    def test_consume(self):
        state = self.given_state(CardId.CONSUME, orbs=[(OrbId.FROST, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_slots_count(play, 2)
        self.see_orb_count(play, 1)

    def test_consume_removes_last_orb(self):
        state = self.given_state(CardId.CONSUME, orbs=[(OrbId.LIGHTNING, 1), (OrbId.FROST, 1), (OrbId.DARK, 1)],
                                 orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_slots_count(play, 2)
        self.see_orb_count(play, 2)
        self.assertEqual(OrbId.LIGHTNING, play.state.orbs[0][0])
        self.assertEqual(OrbId.FROST, play.state.orbs[1][0])

    def test_chill_single_target(self):
        state = self.given_state(CardId.CHILL, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_orb_count(play, 1)

    def test_chill_multi_target(self):
        state = self.given_state(CardId.CHILL, orb_slots=3, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_orb_count(play, 2)

    def test_barrage(self):
        state = self.given_state(CardId.BARRAGE, orbs=[(OrbId.FROST, 1)], orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 4)

    def test_barrage_multiple_orbs(self):
        state = self.given_state(CardId.BARRAGE, orbs=[(OrbId.FROST, 1), (OrbId.FROST, 1), (OrbId.FROST, 1)],
                                 orb_slots=3, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 18)

    def test_storm(self):
        state = self.given_state(CardId.STORM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.STORM, 1)

    def test_meteor_strike(self):
        state = self.given_state(CardId.METEOR_STRIKE, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 5)
        self.see_enemy_lost_hp(play, 24)
        self.see_orb_count(play, 3)

    def test_rainbow(self):
        state = self.given_state(CardId.RAINBOW, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.assertListEqual([(OrbId.LIGHTNING, 1), (OrbId.FROST, 1), (OrbId.DARK, 6)], play.state.orbs)
        self.see_player_exhaust_count(play, 1)

    def test_rainbow_upgraded(self):
        state = self.given_state(CardId.RAINBOW, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.assertListEqual([(OrbId.LIGHTNING, 1), (OrbId.FROST, 1), (OrbId.DARK, 6)], play.state.orbs)
        self.see_player_exhaust_count(play, 0)

    def test_reprogram(self):
        state = self.given_state(CardId.REPROGRAM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FOCUS, -1)
        self.see_player_has_power(play, PowerId.STRENGTH, 1)
        self.see_player_has_power(play, PowerId.DEXTERITY, 1)

    def test_reprogram_upgraded_with_artifact(self):
        state = self.given_state(CardId.REPROGRAM, upgrade=1, player_powers={PowerId.ARTIFACT: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FOCUS, 0)
        self.see_player_has_power(play, PowerId.ARTIFACT, 0)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)
        self.see_player_has_power(play, PowerId.DEXTERITY, 2)

    def test_hyperbeam(self):
        state = self.given_state(CardId.HYPERBEAM, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 26, enemy_index=0)
        self.see_enemy_lost_hp(play, 26, enemy_index=1)
        self.see_player_has_power(play, PowerId.FOCUS, -3)

    def test_fission(self):
        state = self.given_state(CardId.FISSION, orbs=[(OrbId.FROST, 1), (OrbId.FROST, 1), (OrbId.FROST, 1)],
                                 orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -3)
        self.see_player_drew_cards(play, 3)
        self.see_player_has_block(play, 0)
        self.see_orb_count(play, 0)

    def test_fission_upgraded(self):
        state = self.given_state(CardId.FISSION, orbs=[(OrbId.FROST, 1), (OrbId.FROST, 1), (OrbId.FROST, 1)],
                                 orb_slots=3, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -3)
        self.see_player_drew_cards(play, 3)
        self.see_player_has_block(play, 15)
        self.see_orb_count(play, 0)

    def test_creative_ai(self):
        state = self.given_state(CardId.CREATIVE_AI)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_has_power(play, PowerId.CREATIVE_AI, 1)

    def test_fusion(self):
        state = self.given_state(CardId.FUSION, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.PLASMA)

    def test_reboot(self):
        state = self.given_state(CardId.REBOOT)
        state.hand.append(get_card(CardId.WOUND))
        for i in range(5):
            state.draw_pile.append(get_card(CardId.WOUND))
        for i in range(4):
            state.discard_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_hand_count(play, 4)
        self.see_player_exhaust_count(play, 1)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_draw_pile_count(play, 6)

    def test_loop(self):
        state = self.given_state(CardId.LOOP)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.LOOP, 1)

    def test_loop_upgraded(self):
        state = self.given_state(CardId.LOOP, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.LOOP, 2)

    def test_sunder_no_kill(self):
        state = self.given_state(CardId.SUNDER)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_enemy_lost_hp(play, 24)

    def test_sunder_yes_kill(self):
        state = self.given_state(CardId.SUNDER)
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_hp_is(play, 0)

    def test_recursion(self):
        state = self.given_state(CardId.RECURSION, orb_slots=3, orbs=[(OrbId.LIGHTNING, 1), (OrbId.FROST, 1)])
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.assertListEqual([(OrbId.FROST, 1), (OrbId.LIGHTNING, 1)], play.state.orbs)
        self.see_enemy_lost_hp(play, 8)

    def test_melter(self):
        state = self.given_state(CardId.MELTER)
        state.monsters[0].block = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 10)

    def test_bullseye(self):
        state = self.given_state(CardId.BULLSEYE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_has_power(play, PowerId.LOCK_ON, 2)

    def test_bullseye_upgraded(self):
        state = self.given_state(CardId.BULLSEYE, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 11)
        self.see_enemy_has_power(play, PowerId.LOCK_ON, 3)

    def test_calculated_gamble(self):
        state = self.given_state(CardId.CALCULATED_GAMBLE)
        for i in range(5):
            state.hand.append(get_card(CardId.WOUND))
        for i in range(6):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_hand_count(play, 5)
        self.see_player_draw_pile_count(play, 1)
        self.see_player_discard_pile_count(play, 5)
        self.see_player_exhaust_count(play, 1)

    def test_calculated_gamble_upgraded(self):
        state = self.given_state(CardId.CALCULATED_GAMBLE, upgrade=1)
        for i in range(5):
            state.hand.append(get_card(CardId.WOUND))
        for i in range(6):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_hand_count(play, 5)
        self.see_player_draw_pile_count(play, 1)
        self.see_player_discard_pile_count(play, 6)
        self.see_player_exhaust_count(play, 0)

    def test_compile_driver_four_unique_orbs(self):
        state = self.given_state(CardId.COMPILE_DRIVER, orb_slots=3,
                                 orbs=[(OrbId.LIGHTNING, 1), (OrbId.FROST, 1), (OrbId.DARK, 1), (OrbId.PLASMA, 1)])
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 4)
        self.see_enemy_lost_hp(play, 7)

    def test_compile_driver_with_similar_orbs(self):
        state = self.given_state(CardId.COMPILE_DRIVER, orb_slots=3,
                                 orbs=[(OrbId.FROST, 1), (OrbId.FROST, 1), (OrbId.DARK, 1), (OrbId.DARK, 1)])
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 2)
        self.see_enemy_lost_hp(play, 7)

    def test_compile_driver_with_no_orbs(self):
        state = self.given_state(CardId.COMPILE_DRIVER)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 0)
        self.see_enemy_lost_hp(play, 7)

    def test_compile_driver_upgraded(self):
        state = self.given_state(CardId.COMPILE_DRIVER, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 0)
        self.see_enemy_lost_hp(play, 10)

    def test_fire_breathing(self):
        state = self.given_state(CardId.FIRE_BREATHING)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FIRE_BREATHING, 6)

    def test_evolve(self):
        state = self.given_state(CardId.EVOLVE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.EVOLVE, 1)

    def test_demon_form(self):
        state = self.given_state(CardId.DEMON_FORM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_has_power(play, PowerId.DEMON_FORM, 2)

    def test_berserk(self):
        state = self.given_state(CardId.BERSERK)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_power(play, PowerId.VULNERABLE, 2)
        self.see_player_has_power(play, PowerId.BERSERK, 1)

    def test_go_for_the_eyes(self):
        state = self.given_state(CardId.GO_FOR_THE_EYES)
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)

    def test_go_for_the_eyes_upgraded(self):
        state = self.given_state(CardId.GO_FOR_THE_EYES, upgrade=1)
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 4)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)

    def test_go_for_the_eyes_does_not_trigger(self):
        state = self.given_state(CardId.GO_FOR_THE_EYES)
        state.monsters[0].damage = -1
        state.monsters[0].hits = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_does_not_have_power(play, PowerId.WEAKENED)

    def test_amplify(self):
        state = self.given_state(CardId.AMPLIFY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.AMPLIFY, 1)

    def test_amplify_upgraded(self):
        state = self.given_state(CardId.AMPLIFY, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.AMPLIFY, 2)

    def test_burst(self):
        state = self.given_state(CardId.BURST)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.BURST, 1)

    def test_double_tap(self):
        state = self.given_state(CardId.DOUBLE_TAP)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.DOUBLE_TAP, 1)

    def test_chaos(self):
        state = self.given_state(CardId.CHAOS, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.INTERNAL_RANDOM_ORB)

    def test_chaos_upgraded(self):
        state = self.given_state(CardId.CHAOS, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 2)
        self.see_orb_type_count(play, 2, OrbId.INTERNAL_RANDOM_ORB)

    def test_darkness(self):
        state = self.given_state(CardId.DARKNESS, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_orb_type_count(play, 1, OrbId.DARK)

    def test_darkness_upgraded(self):
        state = self.given_state(CardId.DARKNESS, upgrade=1, orb_slots=3)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)

        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.DARK, orb_id)
        self.assertEqual(12, amount)

    def test_darkness_upgraded_triggering_evoke(self):
        state = self.given_state(CardId.DARKNESS, upgrade=1, orb_slots=1, orbs=[(OrbId.DARK, 6)])
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_orb_count(play, 1)
        self.see_enemy_lost_hp(play, 12)

        orb_id, amount = play.state.orbs[0]
        self.assertEqual(OrbId.DARK, orb_id)
        self.assertEqual(12, amount)

    def test_hello_world(self):
        state = self.given_state(CardId.HELLO_WORLD)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.HELLO, 1)

    def test_magnetism(self):
        state = self.given_state(CardId.MAGNETISM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.MAGNETISM, 1)

    def test_all_for_one(self):
        state = self.given_state(CardId.ALL_FOR_ONE)
        state.discard_pile.append(get_card(CardId.STRIKE_R))
        state.discard_pile.append(get_card(CardId.NEUTRALIZE))
        state.discard_pile.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_hand_count(play, 1)
        self.see_hand_card_is(play, CardId.NEUTRALIZE, 0)
        self.see_player_discard_pile_count(play, 3)

    def test_all_for_one_limited_by_hand_size(self):
        state = self.given_state(CardId.ALL_FOR_ONE)
        for i in range(8):
            state.hand.append(get_card(CardId.WOUND))
        state.discard_pile.append(get_card(CardId.NEUTRALIZE))
        for j in range(5):
            state.discard_pile.append(get_card(CardId.WOUND))
        state.discard_pile.append(get_card(CardId.NEUTRALIZE))
        state.discard_pile.append(get_card(CardId.NEUTRALIZE))
        state.discard_pile.append(get_card(CardId.NEUTRALIZE))
        state.discard_pile.append(get_card(CardId.NEUTRALIZE))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_hand_count(play, 10)
        self.see_player_discard_pile_count(play, 9)
        self.see_hand_card_is(play, CardId.NEUTRALIZE, 8)
        self.see_hand_card_is(play, CardId.NEUTRALIZE, 9)

    def test_all_for_one_retrieves_and_plays_discounted_streamline(self):
        state = self.given_state(CardId.STREAMLINE)
        state.hand.append(get_card(CardId.ALL_FOR_ONE))
        state.hand[0].cost = 1
        play = self.when_making_the_most_plays(state)
        # self.see_player_spent_energy(play, 3) # energy when coming back from discard seems to be odd
        self.see_enemy_lost_hp(play, 40)

    def test_equilibrium(self):
        state = self.given_state(CardId.EQUILIBRIUM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_block(play, 13)
        self.see_player_has_power(play, PowerId.EQUILIBRIUM, 1)

    def test_flying_sleeves(self):
        state = self.given_state(CardId.FLYING_SLEEVES)
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)

    def test_flying_sleeves_stays_in_hand(self):
        state = self.given_state(CardId.FLYING_SLEEVES)
        state.player.energy = 0
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_hand_count(play, 1)
        self.assertEqual(CardId.FLYING_SLEEVES, play.state.hand[0].id)

    def test_safety(self):
        state = self.given_state(CardId.SAFETY)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.see_player_has_block(play, 12)

    def test_safety_stays_in_hand(self):
        state = self.given_state(CardId.SAFETY)
        state.player.energy = 0
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_hand_count(play, 1)
        self.assertEqual(CardId.SAFETY, play.state.hand[0].id)

    def test_establishment(self):
        state = self.given_state(CardId.ESTABLISHMENT)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.ESTABLISHMENT, 1)

    def test_battle_hymn(self):
        state = self.given_state(CardId.BATTLE_HYMN)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.BATTLE_HYMN, 1)

    def test_study(self):
        state = self.given_state(CardId.STUDY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.STUDY, 1)

    def test_strike_p(self):
        state = self.given_state(CardId.STRIKE_P)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)

    def test_strike_p_upgraded(self):
        state = self.given_state(CardId.STRIKE_P, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_spent_energy(play, 1)

    def test_defend_p(self):
        state = self.given_state(CardId.DEFEND_P)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 5)

    def test_defend_p_upgraded(self):
        state = self.given_state(CardId.DEFEND_P, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 8)

    def test_bowling_bash_single(self):
        state = self.given_state(CardId.BOWLING_BASH, targets=1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_spent_energy(play, 1)

    def test_bowling_bash_poly(self):
        state = self.given_state(CardId.BOWLING_BASH, targets=3)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 21, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_bowling_bash_poly_some_dead(self):
        state = self.given_state(CardId.BOWLING_BASH, targets=3)
        state.monsters[2].current_hp = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 14, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_player_spent_energy(play, 1)

    def test_consecrate(self):
        state = self.given_state(CardId.CONSECRATE, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5, enemy_index=0)
        self.see_enemy_lost_hp(play, 5, enemy_index=1)
        self.see_player_spent_energy(play, 0)

    def test_conclude(self):
        state = self.given_state(CardId.CONCLUDE, targets=2)
        state.hand.append(get_card(CardId.REGRET))
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12, enemy_index=0)
        self.see_enemy_lost_hp(play, 12, enemy_index=1)
        self.see_player_spent_energy(play, 1)
        self.see_player_lost_hp(play, 1)

    def test_ragnarok(self):
        state = self.given_state(CardId.RAGNAROK, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 25)

    def test_ragnarok_upgraded(self):
        state = self.given_state(CardId.RAGNAROK, upgrade=1, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 36)

    def test_insight(self):
        state = self.given_state(CardId.INSIGHT)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 2)
        self.see_player_exhaust_count(play, 1)

    def test_protect(self):
        state = self.given_state(CardId.PROTECT)
        state.hand.append(get_card(CardId.PROTECT))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 12)
        play.end_turn()
        self.see_player_hand_count(play, 1)
        self.assertEqual(CardId.PROTECT, play.state.hand[0].id)

    def test_smite(self):
        state = self.given_state(CardId.SMITE)
        state.hand.append(get_card(CardId.SMITE))
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        play.end_turn()
        self.see_player_hand_count(play, 1)

    def test_feel_no_pain(self):
        state = self.given_state(CardId.FEEL_NO_PAIN)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.FEEL_NO_PAIN, 3)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 0)

    def test_dark_embrace(self):
        state = self.given_state(CardId.DARK_EMBRACE)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.DARK_EMBRACE, 1)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 0)

    def test_corruption(self):
        state = self.given_state(CardId.CORRUPTION)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.CORRUPTION, 1)
        self.see_player_spent_energy(play, 3)
        self.see_player_discard_pile_count(play, 0)

    def test_sentinel(self):
        state = self.given_state(CardId.SENTINEL)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 5)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)

    def test_sentinel_exhausted(self):
        state = self.given_state(CardId.SENTINEL)
        state.hand[0].exhausts = True
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 5)
        self.see_player_spent_energy(play, -1)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_sentinel_upgraded_exhausted(self):
        state = self.given_state(CardId.SENTINEL, upgrade=1)
        state.hand[0].exhausts = True
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 8)
        self.see_player_spent_energy(play, -2)
        self.see_player_discard_pile_count(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_sever_soul(self):
        state = self.given_state(CardId.SEVER_SOUL)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 2)
        self.see_player_hand_count(play, 1)

    def test_second_wind(self):
        state = self.given_state(CardId.SECOND_WIND, player_powers={PowerId.JUGGERNAUT: 5, PowerId.DEXTERITY: 1})
        state.hand.append(get_card(CardId.BLUDGEON))
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 2)
        self.see_player_hand_count(play, 1)
        self.see_player_has_block(play, 12)
        self.see_enemy_lost_hp(play, 10)

    def test_ritual_dagger(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 15)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_ritual_dagger_deals_more_damage_when_powered_up(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.add_memory_by_card(CardId.RITUAL_DAGGER, "default", 3)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_ritual_dagger_can_power_up(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(3, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_ritual_dagger_can_power_up_upgraded(self):
        state = self.given_state(CardId.RITUAL_DAGGER, upgrade=1)
        state.add_memory_by_card(CardId.RITUAL_DAGGER, "default", 3)
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(8, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_ritual_dagger_no_power_up_on_minion(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.monsters[0].current_hp = 5
        state.monsters[0].powers[PowerId.MINION] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(0, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_ritual_dagger_power_up_on_life_link_one_alive(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.monsters[0].current_hp = 5
        state.monsters[0].powers[PowerId.LIFE_LINK] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.assertEqual(3, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_ritual_dagger_no_power_up_on_life_link_one_alive(self):
        state = self.given_state(CardId.RITUAL_DAGGER, targets=2)
        state.monsters[0].current_hp = 5
        state.monsters[0].powers[PowerId.LIFE_LINK] = 1
        state.monsters[1].current_hp = 5
        state.monsters[1].powers[PowerId.LIFE_LINK] = 1
        play = self.when_playing_the_first_card(state)
        self.assertEqual(0, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_ritual_dagger_extra_damage_applies_per_uuid(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.hand[0].uuid = "different_uuid"
        state.monsters[0].current_hp = 15
        state.add_memory_by_card(CardId.RITUAL_DAGGER, "default", 69)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.assertEqual(69, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))
        self.assertEqual(3, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "different_uuid"))

    def test_ritual_dagger_does_not_power_up_across_paths(self):
        state = self.given_state(CardId.RITUAL_DAGGER, player_powers={PowerId.STRENGTH: -4})
        for i in range(9):
            state.hand.append(get_card(CardId.SHIV))
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(3, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_finisher(self):
        state = self.given_state(CardId.FINISHER)
        state.hand.append(get_card(CardId.SHIV))
        state.hand.append(get_card(CardId.SHIV))
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(3, play.state.get_memory_value(MemoryItem.ATTACKS_THIS_TURN))

    def test_claw(self):
        state = self.given_state(CardId.CLAW)
        state.add_memory_value(MemoryItem.CLAWS_THIS_BATTLE, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_spent_energy(play, 0)
        self.assertEqual(2, play.state.get_memory_value(MemoryItem.CLAWS_THIS_BATTLE))

    def test_claw_upgraded(self):
        state = self.given_state(CardId.CLAW, upgrade=1)
        state.add_memory_value(MemoryItem.CLAWS_THIS_BATTLE, 1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_spent_energy(play, 0)
        self.assertEqual(2, play.state.get_memory_value(MemoryItem.CLAWS_THIS_BATTLE))

    def test_multiple_claws(self):
        state = self.given_state(CardId.CLAW)
        state.hand.append(get_card(CardId.CLAW))
        state.hand.append(get_card(CardId.CLAW))
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 15)
        self.see_player_spent_energy(play, 0)
        self.assertEqual(3, play.state.get_memory_value(MemoryItem.CLAWS_THIS_BATTLE))

    def test_genetic_algorithm(self):
        state = self.given_state(CardId.GENETIC_ALGORITHM)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 1)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_genetic_algorithm_blocks_more_powered_up_and_can_power_up(self):
        state = self.given_state(CardId.GENETIC_ALGORITHM)
        state.add_memory_by_card(CardId.GENETIC_ALGORITHM, "default", 2)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 3)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(4, play.state.get_memory_by_card(CardId.GENETIC_ALGORITHM, "default"))

    def test_genetic_algorithm_can_power_up_upgraded(self):
        state = self.given_state(CardId.GENETIC_ALGORITHM, upgrade=1)
        state.add_memory_by_card(CardId.GENETIC_ALGORITHM, "default", 2)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 3)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(5, play.state.get_memory_by_card(CardId.GENETIC_ALGORITHM, "default"))

    def test_genetic_algorithm_blocks_per_uuid(self):
        state = self.given_state(CardId.GENETIC_ALGORITHM)
        state.hand[0].uuid = "different_uuid"
        state.add_memory_by_card(CardId.GENETIC_ALGORITHM, "default", 69)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 1)
        self.assertEqual(69, play.state.get_memory_by_card(CardId.GENETIC_ALGORITHM, "default"))
        self.assertEqual(2, play.state.get_memory_by_card(CardId.GENETIC_ALGORITHM, "different_uuid"))

    def test_recycle_on_one_cost_card(self):
        state = self.given_state(CardId.RECYCLE)
        state.hand.insert(0,get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 0)  # no energy difference, spent one and then gained one
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_recycle_upgraded(self):
        state = self.given_state(CardId.RECYCLE, upgrade=1)
        state.hand.insert(0,get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, -1)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_recycle_on_unplayable_card(self):
        state = self.given_state(CardId.RECYCLE)
        state.hand.insert(0, get_card(CardId.PAIN))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_recycle_on_x_cost_card(self):
        state = self.given_state(CardId.RECYCLE)
        state.hand.insert(0, get_card(CardId.WHIRLWIND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, -3) # start with 5, -1, *2 = 8 which is 3 more than start
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)

    def test_recycle_upgraded_on_x_cost_card(self):
        state = self.given_state(CardId.RECYCLE, upgrade=1)
        state.hand.insert(0, get_card(CardId.WHIRLWIND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, -5)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_exhaust_count(play, 1)


    def test_same_uuid_different_cards_do_not_overlap(self):
        state = self.given_state(CardId.GENETIC_ALGORITHM)
        state.hand[0].uuid = "default"
        state.hand.append(get_card(CardId.RITUAL_DAGGER))
        state.add_memory_by_card(CardId.RITUAL_DAGGER, "default", 69)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 1)
        self.assertEqual(2, play.state.get_memory_by_card(CardId.GENETIC_ALGORITHM, "default"))
        self.assertEqual(69, play.state.get_memory_by_card(CardId.RITUAL_DAGGER, "default"))

    def test_steam_barrier(self):
        state = self.given_state(CardId.STEAM_BARRIER)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 6)
        self.see_player_spent_energy(play, 0)
        self.assertEqual(1, play.state.get_memory_by_card(CardId.STEAM_BARRIER, "default"))

    def test_steam_barrier_upgraded(self):
        state = self.given_state(CardId.STEAM_BARRIER, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 8)
        self.assertEqual(1, play.state.get_memory_by_card(CardId.STEAM_BARRIER, "default"))

    def test_steam_barrier_powers_down(self):
        state = self.given_state(CardId.STEAM_BARRIER)
        state.add_memory_by_card(CardId.STEAM_BARRIER, "default", 2)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 4)
        self.assertEqual(3, play.state.get_memory_by_card(CardId.STEAM_BARRIER, "default"))

    def test_steam_barrier_does_not_go_below_0(self):
        state = self.given_state(CardId.STEAM_BARRIER)
        state.add_memory_by_card(CardId.STEAM_BARRIER, "default", 10)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 0)
        self.assertEqual(11, play.state.get_memory_by_card(CardId.STEAM_BARRIER, "default"))

    def test_glass_knife(self):
        state = self.given_state(CardId.GLASS_KNIFE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 16)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(2, play.state.get_memory_by_card(CardId.GLASS_KNIFE, "default"))

    def test_glass_knife_upgraded(self):
        state = self.given_state(CardId.GLASS_KNIFE, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 24)
        self.assertEqual(2, play.state.get_memory_by_card(CardId.GLASS_KNIFE, "default"))

    def test_glass_knife_powers_down(self):
        state = self.given_state(CardId.GLASS_KNIFE)
        state.add_memory_by_card(CardId.GLASS_KNIFE, "default", 2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.assertEqual(4, play.state.get_memory_by_card(CardId.GLASS_KNIFE, "default"))

    def test_glass_knife_does_not_go_below_0(self):
        state = self.given_state(CardId.GLASS_KNIFE)
        state.add_memory_by_card(CardId.GLASS_KNIFE, "default", 10)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(12, play.state.get_memory_by_card(CardId.GLASS_KNIFE, "default"))

    def test_ftl(self):
        state = self.given_state(CardId.FTL)
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.assertEqual(3, play.state.get_memory_value(MemoryItem.CARDS_THIS_TURN))

    def test_ftl_does_not_draw(self):
        state = self.given_state(CardId.FTL, upgrade=1)
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 4)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 0)
        self.see_player_drew_cards(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.assertEqual(5, play.state.get_memory_value(MemoryItem.CARDS_THIS_TURN))

    def test_scrape(self):
        state = self.given_state(CardId.SCRAPE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 4)
        self.see_player_discard_pile_count(play, 1)

    def test_blizzard(self):
        state = self.given_state(CardId.BLIZZARD)
        state.add_memory_value(MemoryItem.FROST_THIS_BATTLE, 4)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(4, play.state.get_memory_value(MemoryItem.FROST_THIS_BATTLE))

    def test_frost_value_increases(self):
        state = self.given_state(CardId.COOLHEADED)
        state.add_memory_value(MemoryItem.FROST_THIS_BATTLE, 4)
        play = self.when_playing_the_first_card(state)
        self.see_player_drew_cards(play, 1)
        self.assertEqual(5, play.state.get_memory_value(MemoryItem.FROST_THIS_BATTLE))

    def test_blizzard_does_nothing(self):
        state = self.given_state(CardId.BLIZZARD)
        state.add_memory_value(MemoryItem.FROST_THIS_BATTLE, 0)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.FROST_THIS_BATTLE))

    def test_thunder_strike(self):
        state = self.given_state(CardId.THUNDER_STRIKE, targets=2)
        state.add_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE, 4)
        play = self.when_playing_the_first_card(state)
        self.see_random_damage_dealt(play, 28)
        self.see_player_spent_energy(play, 3)
        self.assertEqual(4, play.state.get_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE))

    def test_lightning_value_increases(self):
        state = self.given_state(CardId.ZAP)
        state.add_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE, 4)
        play = self.when_playing_the_first_card(state)
        self.assertEqual(5, play.state.get_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE))

    def test_thunder_strike_does_nothing(self):
        state = self.given_state(CardId.THUNDER_STRIKE, targets=2)
        state.add_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE, 0)
        play = self.when_playing_the_first_card(state)
        self.see_random_damage_dealt(play, 0)
        self.see_player_spent_energy(play, 3)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE))

    def test_judgement(self):
        state = self.given_state(CardId.JUDGEMENT)
        state.monsters[0].current_hp = 15
        state.monsters[0].block = 40
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_hp_is(play, 0)

    def test_judgement_upgraded(self):
        state = self.given_state(CardId.JUDGEMENT, upgrade=1)
        state.monsters[0].current_hp = 40
        state.monsters[0].block = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_hp_is(play, 0)

    def test_judgement_does_not_kill(self):
        state = self.given_state(CardId.JUDGEMENT)
        state.monsters[0].current_hp = 31
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_hp_is(play, 31)

    def test_scrawl(self):
        state = self.given_state(CardId.SCRAWL)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 9)

    def test_scrawl_draws_1(self):
        state = self.given_state(CardId.SCRAWL)
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_crush_joints(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.CRUSH_JOINTS))
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)

    def test_crush_joints_triggers(self):
        state = self.given_state(CardId.DEFEND_R)
        state.hand.append(get_card(CardId.CRUSH_JOINTS))
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 1)

    def test_crush_joints_triggers_upgraded(self):
        state = self.given_state(CardId.DEFEND_R)
        state.hand.append(get_card(CardId.CRUSH_JOINTS))
        state.hand[1].upgrade = 1
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)

    def test_sash_whip(self):
        state = self.given_state(CardId.DEFEND_R)
        state.hand.append(get_card(CardId.SASH_WHIP))
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 0)

    def test_sash_whip_triggers(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.SASH_WHIP))
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)

    def test_sash_whip_triggers_upgraded(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.SASH_WHIP))
        state.hand[1].upgrade = 1
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 16)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)

    def test_follow_up(self):
        state = self.given_state(CardId.DEFEND_R)
        state.hand.append(get_card(CardId.FOLLOW_UP))
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_spent_energy(play, 2)

    def test_follow_up_triggers(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.FOLLOW_UP))
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_player_discard_pile_count(play, 2)
        self.see_player_spent_energy(play, 1)

    def test_sanctity(self):
        state = self.given_state(CardId.CLEAVE)
        state.hand.append(get_card(CardId.SANCTITY))
        play = self.when_making_the_most_plays(state)
        self.see_player_has_block(play, 6)
        self.see_player_spent_energy(play, 2)
        self.see_player_drew_cards(play, 0)

    def test_sanctity_triggers(self):
        state = self.given_state(CardId.DEFEND_R)
        state.hand.append(get_card(CardId.SANCTITY))
        play = self.when_making_the_most_plays(state)
        self.see_player_has_block(play, 11)
        self.see_player_spent_energy(play, 2)
        self.see_player_drew_cards(play, 2)

    def test_like_water(self):
        state = self.given_state(CardId.LIKE_WATER)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.LIKE_WATER, 5)

    def test_miracle(self):
        state = self.given_state(CardId.MIRACLE)
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_spent_energy(play, -1)

    def test_devotion(self):
        state = self.given_state(CardId.DEVOTION)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.DEVOTION, 2)

    def test_pray(self):
        state = self.given_state(CardId.PRAY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 3)
        self.see_player_draw_pile_count(play, 1)
        self.assertEqual(CardId.INSIGHT, play.state.draw_pile[0].id)

    def test_worship(self):
        state = self.given_state(CardId.WORSHIP)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.MANTRA_INTERNAL, 5)
        self.see_player_discard_pile_count(play, 1)

    def test_worship_upgraded(self):
        state = self.given_state(CardId.WORSHIP, upgrade=1)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_discard_pile_count(play, 0)
        self.see_hand_card_is(play, CardId.WORSHIP)

    def test_mental_fortress(self):
        state = self.given_state(CardId.MENTAL_FORTRESS)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.MENTAL_FORTRESS, 4)

    def test_rushdown(self):
        state = self.given_state(CardId.RUSHDOWN)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.RUSHDOWN, 2)

    def test_wreath_of_flame(self):
        state = self.given_state(CardId.WREATH_OF_FLAME)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_has_power(play, PowerId.VIGOR, 5)

    def test_evaluate(self):
        state = self.given_state(CardId.EVALUATE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 6)
        self.see_player_draw_pile_count(play, 1)
        self.assertEqual(CardId.INSIGHT, play.state.draw_pile[0].id)

    def test_deceive_reality(self):
        state = self.given_state(CardId.DECEIVE_REALITY)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 4)
        self.see_player_hand_count(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.assertEqual(CardId.SAFETY, play.state.hand[0].id)

    def test_master_reality(self):
        state = self.given_state(CardId.MASTER_REALITY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.MASTER_REALITY, 1)

    def test_carve_reality(self):
        state = self.given_state(CardId.CARVE_REALITY)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_hand_count(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.assertEqual(CardId.SMITE, play.state.hand[0].id)

    def test_perseverance(self):
        state = self.given_state(CardId.PERSEVERANCE)
        state.hand.append(get_card(CardId.PERSEVERANCE))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_block(play, 5)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_hand_count(play, 1)

    def test_perseverance_blocks_more_when_powered_up(self):
        state = self.given_state(CardId.PERSEVERANCE, upgrade=1)
        state.add_memory_by_card(CardId.PERSEVERANCE, "default", 2)
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 9)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(2, play.state.get_memory_by_card(CardId.PERSEVERANCE, "default"))

    def test_perseverance_powers_up_by_retaining(self):
        state = self.given_state(CardId.PERSEVERANCE, upgrade=1)
        state.player.energy = 0
        play = self.when_playing_the_whole_hand(state)
        play.state.end_turn()
        self.see_player_has_block(play, 0)
        self.assertEqual(3, play.state.get_memory_by_card(CardId.PERSEVERANCE, "default"))

    def test_reach_heaven(self):
        state = self.given_state(CardId.REACH_HEAVEN)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)
        self.assertEqual(CardId.THROUGH_VIOLENCE, play.state.draw_pile[0].id)

    def test_through_violence(self):
        state = self.given_state(CardId.THROUGH_VIOLENCE)
        state.hand.append(get_card(CardId.THROUGH_VIOLENCE))
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)
        self.see_player_hand_count(play, 1)

    def test_signature_move(self):
        state = self.given_state(CardId.SIGNATURE_MOVE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 30)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_signature_cannot_be_played(self):
        state = self.given_state(CardId.SIGNATURE_MOVE)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.player.energy = 2
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_discard_pile_count(play, 1)

    def test_wheel_kick(self):
        state = self.given_state(CardId.WHEEL_KICK)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 15)
        self.see_player_drew_cards(play, 2)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_spirit_shield(self):
        state = self.given_state(CardId.SPIRIT_SHIELD)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 0)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_spirit_shield_multiple_cards(self):
        state = self.given_state(CardId.SPIRIT_SHIELD)
        for i in range(3):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 9)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_spirit_shield_upgraded(self):
        state = self.given_state(CardId.SPIRIT_SHIELD, upgrade=1)
        for i in range(3):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 12)
        self.see_player_spent_energy(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_wallop(self):
        state = self.given_state(CardId.WALLOP)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_enemy_lost_hp(play, 9)
        self.see_player_has_block(play, 9)

    def test_wallop_less_block_when_less_hp_damage(self):
        state = self.given_state(CardId.WALLOP)
        state.monsters[0].block = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_has_block(play, 6)

    def test_windmill_strike(self):
        state = self.given_state(CardId.WINDMILL_STRIKE)
        state.hand.append(get_card(CardId.WINDMILL_STRIKE))
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_enemy_lost_hp(play, 7)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_hand_count(play, 1)

    def test_windmill_strike_damages_more_when_powered_up(self):
        state = self.given_state(CardId.WINDMILL_STRIKE, upgrade=1)
        state.add_memory_by_card(CardId.WINDMILL_STRIKE, "default", 2)
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 1)
        self.assertEqual(2, play.state.get_memory_by_card(CardId.WINDMILL_STRIKE, "default"))

    def test_windmill_strike_powers_up_by_retaining(self):
        state = self.given_state(CardId.WINDMILL_STRIKE, upgrade=1)
        state.player.energy = 0
        play = self.when_playing_the_whole_hand(state)
        play.state.end_turn()
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(5, play.state.get_memory_by_card(CardId.WINDMILL_STRIKE, "default"))

    def test_deva_form(self):
        state = self.given_state(CardId.DEVA_FORM)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_has_power(play, PowerId.DEVA, 1)

    def test_deva_form_ethereal(self):
        state = self.given_state(CardId.DEVA_FORM)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.assertEqual(True, play.state.hand[0].ethereal)

    def test_wave_of_the_hand(self):
        state = self.given_state(CardId.WAVE_OF_THE_HAND)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.WAVE_OF_THE_HAND, 1)

    def test_sands_of_time(self):
        state = self.given_state(CardId.SANDS_OF_TIME)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 4)
        self.see_enemy_lost_hp(play, 20)

    def test_sands_of_time_retaining_reduces_cost(self):
        state = self.given_state(CardId.SANDS_OF_TIME)
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(3, play.state.hand[0].cost)

    def test_sands_of_time_retaining_reduces_cost_combo_with_establishment(self):
        state = self.given_state(CardId.SANDS_OF_TIME, player_powers={PowerId.ESTABLISHMENT: 1})
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(2, play.state.hand[0].cost)

    def test_fasting(self):
        state = self.given_state(CardId.FASTING)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_power(play, PowerId.STRENGTH, 3)
        self.see_player_has_power(play, PowerId.DEXTERITY, 3)
        self.see_player_has_power(play, PowerId.FASTING, 1)

    def test_swivel(self):
        state = self.given_state(CardId.SWIVEL)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_has_block(play, 8)
        self.see_player_has_power(play, PowerId.FREE_ATTACK_POWER, 1)

    def test_talk_to_the_hand(self):
        state = self.given_state(CardId.TALK_TO_THE_HAND)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 5)
        self.see_player_exhaust_count(play, 1)
        self.see_enemy_has_power(play, PowerId.BLOCK_RETURN, 2)

    def test_collect(self):
        state = self.given_state(CardId.COLLECT, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 5)
        self.see_player_has_power(play, PowerId.COLLECT, 6)

    def test_pressure_points(self):
        state = self.given_state(CardId.PRESSURE_POINTS)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_has_power(play, PowerId.MARK, 8)

    def test_pressure_points_multi_target(self):
        state = self.given_state(CardId.PRESSURE_POINTS, targets=2)
        state.monsters[1].powers = {PowerId.MARK: 15}
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 8, enemy_index=0)
        self.see_enemy_lost_hp(play, 15, enemy_index=1)

    def test_brilliance(self):
        state = self.given_state(CardId.BRILLIANCE)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_player_spent_energy(play, 1)
        self.see_player_discard_pile_count(play, 1)

    def test_brilliance_damages_more_when_powered_up(self):
        state = self.given_state(CardId.BRILLIANCE, upgrade=1)
        state.add_memory_value(MemoryItem.MANTRA_THIS_BATTLE, 3)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 19)
        self.see_player_spent_energy(play, 1)

    def test_cut_through_fate(self):
        state = self.given_state(CardId.CUT_THROUGH_FATE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_enemy_lost_hp(play, 7)
        self.see_player_drew_cards(play, 1)
        self.see_player_scryed(play, 2)

    def test_just_lucky(self):
        state = self.given_state(CardId.JUST_LUCKY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_scryed(play, 1)
        self.see_player_has_block(play, 2)
        self.see_enemy_lost_hp(play, 3)

    def test_just_lucky_upgraded(self):
        state = self.given_state(CardId.JUST_LUCKY, upgrade=1)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_scryed(play, 2)
        self.see_player_has_block(play, 3)
        self.see_enemy_lost_hp(play, 4)

    def test_third_eye(self):
        state = self.given_state(CardId.THIRD_EYE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 7)
        self.see_player_scryed(play, 3)

    def test_foresight(self):
        state = self.given_state(CardId.FORESIGHT)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.FORESIGHT, 3)

    def test_nirvana(self):
        state = self.given_state(CardId.NIRVANA)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.NIRVANA, 3)

    def test_weave(self):
        state = self.given_state(CardId.WEAVE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_enemy_lost_hp(play, 4)

    def test_weave_returns_to_hand_on_scry(self):
        state = self.given_state(CardId.THIRD_EYE)
        state.discard_pile.append(get_card(CardId.WEAVE))
        play = self.when_playing_the_first_card(state)
        self.see_player_scryed(play, 3)
        self.see_hand_card_is(play, CardId.WEAVE)

    def test_alpha(self):
        state = self.given_state(CardId.ALPHA)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(CardId.BETA, play.state.draw_pile[0].id)
        self.see_player_has_power(play, PowerId.FAKE_ALPHA_BETA, 1)

    def test_beta(self):
        state = self.given_state(CardId.BETA)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(CardId.OMEGA, play.state.draw_pile[0].id)
        self.see_player_has_power(play, PowerId.FAKE_ALPHA_BETA, 1)

    def test_omega(self):
        state = self.given_state(CardId.OMEGA)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_exhaust_count(play, 0)
        self.see_player_has_power(play, PowerId.OMEGA, 50)

    def test_lesson_learned(self):
        state = self.given_state(CardId.LESSON_LEARNED)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 2)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.KILLED_WITH_LESSON_LEARNED))

    def test_lesson_learned_triggers(self):
        state = self.given_state(CardId.LESSON_LEARNED)
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 2)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.KILLED_WITH_LESSON_LEARNED))

    def test_lesson_learned_no_power_up_on_minion(self):
        state = self.given_state(CardId.RITUAL_DAGGER)
        state.monsters[0].current_hp = 5
        state.monsters[0].powers[PowerId.MINION] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_spent_energy(play, 1)
        self.see_player_exhaust_count(play, 1)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.KILLED_WITH_LESSON_LEARNED))

    def test_lesson_learned_power_up_on_life_link_one_alive(self):
        state = self.given_state(CardId.LESSON_LEARNED)
        state.monsters[0].current_hp = 5
        state.monsters[0].powers[PowerId.LIFE_LINK] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.KILLED_WITH_LESSON_LEARNED))

    def test_lesson_learned_no_power_up_on_life_link_one_alive(self):
        state = self.given_state(CardId.RITUAL_DAGGER, targets=2)
        state.monsters[0].current_hp = 5
        state.monsters[0].powers[PowerId.LIFE_LINK] = 1
        state.monsters[1].current_hp = 5
        state.monsters[1].powers[PowerId.LIFE_LINK] = 1
        play = self.when_playing_the_first_card(state)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.KILLED_WITH_LESSON_LEARNED))

    def test_simmering_fury(self):
        state = self.given_state(CardId.SIMMERING_FURY)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.SIMMERING_RAGE, 2)

    def test_wish(self):
        state = self.given_state(CardId.WISH)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_has_power(play, PowerId.STRENGTH, 3)

    def test_foreign_influence(self):
        state = self.given_state(CardId.FOREIGN_INFLUENCE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 0)
        self.see_player_exhaust_count(play, 1)

    def test_normality(self):
        state = self.given_state(CardId.NORMALITY)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.hand.append(get_card(CardId.STRIKE_R))
        state.add_memory_value(MemoryItem.CARDS_THIS_TURN, 2)
        play = self.when_playing_the_whole_hand(state)
        # see that only 2 of the 2 strikes are played because normality stops it
        self.see_enemy_lost_hp(play, 6)

    def test_barricade(self):
        state = self.given_state(CardId.BARRICADE)
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 3)
        self.see_player_has_power(play, PowerId.BARRICADE, 1)
