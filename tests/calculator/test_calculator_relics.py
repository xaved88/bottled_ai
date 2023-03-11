from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import CardId, get_card
from rs.calculator.play_path import PlayPath
from rs.calculator.powers import PowerId
from rs.calculator.relics import RelicId


class CalculatorCardsTest(CalculatorTestFixture):

    def test_strike_dummy(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.STRIKE_DUMMY] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)

    def test_velvet_choker(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.hand.append(get_card(CardId.STRIKE_R))
        state.relics[RelicId.VELVET_CHOKER] = 4
        play = self.when_playing_the_whole_hand(state)
        # see that only 2 of the 3 strikes are played because choker stops it
        self.see_enemy_lost_hp(play, 12)

    def test_paper_phrog(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        state.relics[RelicId.PAPER_PHROG] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)

    def test_paper_krane(self):
        # state.monsters[0].powers[PowerId.WEAKENED] = 1
        # state.relics[RelicId.PAPER_KRANE] = 1
        pass

    def test_nunchaku_increments_with_attack(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.NUNCHAKU] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 1)
        self.see_relic_value(play, RelicId.NUNCHAKU, 4)

    def test_nunchaku_does_not_increment_with_skill(self):
        state = self.given_state(CardId.DEFEND_R)
        state.relics[RelicId.NUNCHAKU] = 3
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, 1)
        self.see_relic_value(play, RelicId.NUNCHAKU, 3)

    def test_nunchaku_gives_energy(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.NUNCHAKU] = 9
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 0)
        self.see_relic_value(play, RelicId.NUNCHAKU, 0)

    def test_nunchaku_cant_play_when_lacking_energy_but_would_receive_it(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.NUNCHAKU] = 9
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_relic_value(play, RelicId.NUNCHAKU, 9)

    def test_pen_nib_increments_with_attack(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.PEN_NIB] = 3
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.PEN_NIB, 4)

    def test_pen_nib_does_not_increment_with_skill(self):
        state = self.given_state(CardId.DEFEND_R)
        state.relics[RelicId.PEN_NIB] = 3
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.PEN_NIB, 3)

    def test_pen_nib_effect(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.relics[RelicId.PEN_NIB] = 9
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_spent_energy(play, 1)
        self.see_relic_value(play, RelicId.PEN_NIB, 0)

    def test_ornamental_fan_increments(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.ORNAMENTAL_FAN] = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_count(play, 1)
        self.see_player_has_block(play, 0)
        self.see_relic_value(play, RelicId.ORNAMENTAL_FAN, 1)

    def test_ornamental_fan_gives_block(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.ORNAMENTAL_FAN] = 2
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_count(play, 1)
        self.see_player_has_block(play, 4)
        self.see_relic_value(play, RelicId.ORNAMENTAL_FAN, 0)

    def test_orichalcum_gives_block_when_player_has_none(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.ORICHALCUM] = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_block(play, 6)

    def test_orichalcum_does_not_give_block_when_player_has_some(self):
        state = self.given_state(CardId.STRIKE_R)
        state.player.block = 1
        state.relics[RelicId.ORICHALCUM] = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_block(play, 1)

    def test_odd_mushroom_reduces_incoming_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.VULNERABLE: 1})
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        state.relics[RelicId.ODD_MUSHROOM] = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 12)

    def test_champion_belt_applies_weak(self):
        state = self.given_state(CardId.BASH)
        state.relics[RelicId.CHAMPION_BELT] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)

    def test_letter_opener_increments(self):
        state = self.given_state(CardId.DEFEND_R)
        state.relics[RelicId.LETTER_OPENER] = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_relic_value(play, RelicId.LETTER_OPENER, 1)

    def test_letter_opener_deals_damage_to_all_enemies(self):
        state = self.given_state(CardId.DEFEND_R, targets=2)
        state.relics[RelicId.LETTER_OPENER] = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, amount=5, enemy_index=0)
        self.see_enemy_lost_hp(play, amount=5, enemy_index=1)
        self.see_relic_value(play, RelicId.LETTER_OPENER, 0)

    def test_torii_reduces_small_damage(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.TORII: 1})
        state.monsters[0].damage = 5
        state.monsters[0].hits = 13
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 13)

    def test_torii_reduces_self_damage(self):
        state = self.given_state(CardId.BLOODLETTING, relics={RelicId.TORII: 1})
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 1)

    def test_torii_does_not_reduce_one_damage(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.TORII: 1})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 13
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 13)

    def test_torii_does_not_reduce_large_damage(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.TORII: 1})
        state.monsters[0].damage = 6
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 12)

    def test_tungsten_rod_reduces_damage(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.TUNGSTEN_ROD: 1})
        state.monsters[0].damage = 6
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 10)

    def test_tungsten_rod_reduces_self_damage(self):
        state = self.given_state(CardId.BLOODLETTING, relics={RelicId.TUNGSTEN_ROD: 1})
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 2)

    def test_tungsten_rod_and_torii_vs_five_damage(self):
        state = self.given_state(CardId.BLOODLETTING, relics={RelicId.TUNGSTEN_ROD: 1, RelicId.TORII: 1})
        state.monsters[0].damage = 5
        state.monsters[0].hits = 8
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 0)

    def test_tungsten_rod_and_torii_vs_six_damage(self):
        state = self.given_state(CardId.BLOODLETTING, relics={RelicId.TUNGSTEN_ROD: 1, RelicId.TORII: 1})
        state.monsters[0].damage = 6
        state.monsters[0].hits = 8
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 40)

    def test_the_boot_deals_extra_damage(self):
        state = self.given_state(CardId.PUMMEL, relics={RelicId.THE_BOOT: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)

    def test_the_boot_doesnt_deal_extra_damage_through_block(self):
        state = self.given_state(CardId.PUMMEL, relics={RelicId.THE_BOOT: 1})
        state.monsters[0].block = 8
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)

    def test_the_boots_extra_damage_is_calculated_for_each_hit(self):
        state = self.given_state(CardId.PUMMEL, relics={RelicId.THE_BOOT: 1})
        state.monsters[0].block = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 15)

    # HELPER METHODS
    def see_relic_value(self, play: PlayPath, relic_id: RelicId, value: int):
        self.assertEqual(value, play.state.relics.get(relic_id))
