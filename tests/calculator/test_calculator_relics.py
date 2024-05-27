from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.memory_items import MemoryItem


class CalculatorRelicsTest(CalculatorTestFixture):

    def test_strike_dummy(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.STRIKE_DUMMY] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)

    def test_wrist_blade(self):
        state = self.given_state(CardId.SHIV)
        state.relics[RelicId.WRIST_BLADE] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)

    def test_no_wrist_blade(self):
        state = self.given_state(CardId.SHIV)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 4)

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

    def test_paper_phrog_no_extra_damage_from_tingsha(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.PAPER_PHROG: 1, RelicId.TINGSHA: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_random_damage_dealt(play, 0)

    def test_paper_krane(self):
        state = self.given_state(CardId.NEUTRALIZE)
        state.relics[RelicId.PAPER_KRANE] = 1
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        play.end_turn()
        self.see_player_lost_hp(play, 6)

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

    def test_pen_nib_increments_with_empty_x_cost_attack(self):
        state = self.given_state(CardId.WHIRLWIND)
        state.player.energy = 0
        state.relics[RelicId.PEN_NIB] = 3
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.PEN_NIB, 4)

    def test_ornamental_fan_increments(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.ORNAMENTAL_FAN] = 0
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_has_block(play, 0)
        self.see_relic_value(play, RelicId.ORNAMENTAL_FAN, 1)

    def test_ornamental_fan_gives_block(self):
        state = self.given_state(CardId.STRIKE_R)
        state.relics[RelicId.ORNAMENTAL_FAN] = 2
        play = self.when_playing_the_first_card(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_has_block(play, 4)
        self.see_relic_value(play, RelicId.ORNAMENTAL_FAN, 0)

    def test_orichalcum_gives_block_when_player_has_none(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.ORICHALCUM: 1})
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
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.VULNERABLE: 1},
                                 relics={RelicId.ODD_MUSHROOM: 1})
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 12)

    def test_champion_belt_applies_weak(self):
        state = self.given_state(CardId.BASH, relics={RelicId.CHAMPION_BELT: 1})
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

    def test_tough_bandages_blocks_from_discard(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.TOUGH_BANDAGES: 1})
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 11)

    def test_tough_bandages_blocks_more_from_2_discards(self):
        state = self.given_state(CardId.PREPARED, 1, relics={RelicId.TOUGH_BANDAGES: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 6)

    def test_tough_bandages_blocks_more_from_X_discard(self):
        state = self.given_state(CardId.UNLOAD, relics={RelicId.TOUGH_BANDAGES: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 3)
        self.see_player_has_block(play, 6)

    def test_tough_bandages_no_extra_block_when_nothing_to_discard(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.TOUGH_BANDAGES: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_hand_count(play, 0)
        self.see_player_has_block(play, 8)

    def test_hovering_kite_1_extra_energy_on_first_discard(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.HOVERING_KITE: 1})
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_hand_count(play, 0)
        self.see_player_has_energy(play, 5)

    def test_hovering_kite_1_extra_energy_on_second_discard(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.HOVERING_KITE: 1})
        state.hand.append(get_card(CardId.SURVIVOR))
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_energy(play, 4)

    def test_hovering_kite_empty_hand(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.HOVERING_KITE: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_has_energy(play, 4)

    def test_hovering_kite_no_discard(self):
        state = self.given_state(CardId.STRIKE_G, relics={RelicId.HOVERING_KITE: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_has_energy(play, 4)

    def test_hovering_kite_not_present_but_discarding(self):
        state = self.given_state(CardId.SURVIVOR)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_energy(play, 4)

    def test_bird_faced_urn(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.BIRD_FACED_URN: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_lost_hp(play, -2)

    def test_gremlin_horn_triggers_on_kill(self):
        state = self.given_state(CardId.ANGER, relics={RelicId.GREMLIN_HORN: 1})
        state.monsters[0].current_hp = 1
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_spent_energy(play, -1)
        self.see_player_hand_count(play, 1)

    def test_gremlin_horn_multi_kill(self):
        state = self.given_state(CardId.DEFLECT, targets=2, relics={RelicId.LETTER_OPENER: 2, RelicId.GREMLIN_HORN: 1})
        state.monsters[0].current_hp = 1
        state.monsters[1].current_hp = 1
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_hp_is(play, amount=0, enemy_index=0)
        self.see_enemy_hp_is(play, amount=0, enemy_index=1)
        self.see_relic_value(play, RelicId.LETTER_OPENER, 0)
        self.see_player_spent_energy(play, -2)
        self.see_player_hand_count(play, 2)

    def test_gremlin_horn_only_get_energy_on_kill(self):
        state = self.given_state(CardId.ANGER, relics={RelicId.GREMLIN_HORN: 1})
        state.monsters[0].current_hp = 7
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_hp_is(play, 1)
        self.see_player_spent_energy(play, 0)
        self.see_player_hand_count(play, 0)

    def test_unceasing_top_triggers_when_hand_empty(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.UNCEASING_TOP: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_hand_count(play, 1)

    def test_unceasing_top_no_trigger_when_not_empty(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.UNCEASING_TOP: 1})
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_hand_count(play, 2)

    def test_ink_bottle_increments(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.INK_BOTTLE: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 2)
        self.see_player_hand_count(play, 0)

    def test_ink_bottle_triggers_and_resets(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.INK_BOTTLE: 9})
        play = self.when_playing_the_whole_hand(state)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 0)
        self.see_player_hand_count(play, 1)

    def test_stone_calendar_triggers_after_turn_7(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.STONE_CALENDAR: 7})
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 52)

    def test_stone_calendar_triggers_needs_turn_end_on_turn_7(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.STONE_CALENDAR: 7})
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 0)

    def test_stone_calendar_does_not_trigger_earlier(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.STONE_CALENDAR: 6})
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 0)

    def test_snecko_skull(self):
        state = self.given_state(CardId.DEADLY_POISON, relics={RelicId.SNECKO_SKULL: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 6)

    def test_snecko_skull_and_envenom_power_interaction_simple(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.ENVENOM: 1}, relics={RelicId.SNECKO_SKULL: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_has_power(play, PowerId.POISON, 2)

    def test_snecko_skull_and_envenom_power_interaction_advanced(self):
        state = self.given_state(CardId.POISONED_STAB, player_powers={PowerId.ENVENOM: 1},
                                 relics={RelicId.SNECKO_SKULL: 1})
        state.monsters[0].powers[PowerId.POISON] = 1
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_has_power(play, PowerId.POISON, 7)

    def test_snecko_skull_and_catalyst_interaction(self):
        state = self.given_state(CardId.CATALYST, relics={RelicId.SNECKO_SKULL: 1})
        state.monsters[0].powers[PowerId.POISON] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 7)

    def test_shuriken_increments(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.SHURIKEN: 0})
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.SHURIKEN, 1)

    def test_shuriken_triggers_and_gives_strength(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.SHURIKEN: 2})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 1)
        self.see_relic_value(play, RelicId.SHURIKEN, 0)

    def test_shuriken_does_not_increment(self):
        state = self.given_state(CardId.DEADLY_POISON, relics={RelicId.SHURIKEN: 0})
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.SHURIKEN, 0)

    def test_kunai_increments(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.KUNAI: 0})
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.KUNAI, 1)

    def test_kunai_triggers_and_gives_dexterity(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.KUNAI: 2})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.DEXTERITY, 1)
        self.see_relic_value(play, RelicId.KUNAI, 0)

    def test_kunai_does_not_increment(self):
        state = self.given_state(CardId.DEADLY_POISON, relics={RelicId.KUNAI: 1})
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.KUNAI, 1)

    def test_hand_drill_provides_vulnerable_on_block_break(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.HAND_DRILL: 1})
        state.monsters[0].block = 6
        play = self.when_playing_the_first_card(state)
        self.see_enemy_block_is(play, 0)
        self.see_enemy_lost_hp(play, 0)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)

    def test_hand_drill_provides_vulnerable_on_block_over_break(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.HAND_DRILL: 1})
        state.monsters[0].block = 4
        play = self.when_playing_the_first_card(state)
        self.see_enemy_block_is(play, 0)
        self.see_enemy_lost_hp(play, 2)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 2)

    def test_hand_drill_provides_no_vulnerable_when_block_unsuccessfully_broken(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.HAND_DRILL: 1})
        state.monsters[0].block = 8
        play = self.when_playing_the_first_card(state)
        self.see_enemy_block_is(play, 2)
        self.see_enemy_lost_hp(play, 0)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)

    def test_hand_drill_provides_no_vulnerable_when_block_was_not_present(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.HAND_DRILL: 1})
        state.monsters[0].block = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_block_is(play, 0)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)

    def test_hand_drill_provides_no_vulnerable_when_block_bypassed(self):
        state = self.given_state(CardId.DEADLY_POISON, relics={RelicId.HAND_DRILL: 1})
        state.monsters[0].block = 8
        state.monsters[0].powers = {PowerId.BARRICADE: 1}
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_block_is(play, 8)
        self.see_enemy_lost_hp(play, 5)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)

    def test_tingsha_deals_direct_damage_with_single_target(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.TINGSHA: 1})
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_random_damage_dealt(play, 0)

    def test_tingsha_direct_damage_blocked(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.TINGSHA: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.monsters[0].block = 5
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_random_damage_dealt(play, 0)

    def test_tingsha_deals_multi_damage_with_single_target_and_multi_discard(self):
        state = self.given_state(CardId.PREPARED, upgrade=1, relics={RelicId.TINGSHA: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_random_damage_dealt(play, 0)

    def test_tingsha_deals_no_damage_if_nothing_to_discard(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.TINGSHA: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_random_damage_dealt(play, 0)

    def test_tingsha_see_random_damage_with_multiple_targets(self):
        state = self.given_state(CardId.SURVIVOR, relics={RelicId.TINGSHA: 1}, targets=2)
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 3)

    def test_tingsha_see_random_multi_damage_with_multiple_targets(self):
        state = self.given_state(CardId.PREPARED, upgrade=1, relics={RelicId.TINGSHA: 1}, targets=2)
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 6)

    def test_gain_block_from_abacus(self):
        state = self.given_state(CardId.PREPARED, upgrade=1, relics={RelicId.THE_ABACUS: 1})
        state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 6)

    def test_do_not_gain_block_from_abacus_because_we_did_not_reset_draw_pile_yet(self):
        state = self.given_state(CardId.FLASH_OF_STEEL, relics={RelicId.THE_ABACUS: 1})
        state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 0)

    def test_sundial_increments(self):
        state = self.given_state(CardId.PREPARED, upgrade=1)
        state.relics[RelicId.SUNDIAL] = 1
        state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.SUNDIAL, 2)

    def test_sundial_triggers(self):
        state = self.given_state(CardId.PREPARED, upgrade=1)
        state.relics[RelicId.SUNDIAL] = 2
        state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_spent_energy(play, -2)
        self.see_relic_value(play, RelicId.SUNDIAL, 0)

    def test_reboot_increments_sundial(self):
        state = self.given_state(CardId.REBOOT)
        state.hand.append(get_card(CardId.WOUND))
        state.relics[RelicId.SUNDIAL] = 1
        for i in range(6):
            state.draw_pile.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 4)
        self.see_player_discard_pile_count(play, 0)
        self.see_relic_value(play, RelicId.SUNDIAL, 2)

    def test_cloak_clasp(self):
        state = self.given_state(CardId.BLUDGEON, relics={RelicId.CLOAK_CLASP: 1})
        for i in range(4):
            state.hand.append(get_card(CardId.BLUDGEON))
        state.player.energy = 1
        play = self.when_playing_the_first_card(state)
        state.end_turn()
        self.see_player_has_block(play, 5)

    def test_frozen_core(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.FROZEN_CORE: 1}, orb_slots=2,
                                 orbs=[(OrbId.LIGHTNING, 1)])
        play = self.when_playing_the_first_card(state)
        state.end_turn()
        self.see_orb_count(play, 2)
        self.assertEqual(OrbId.FROST, play.state.orbs[1][0])
        self.assertEqual(1, play.state.get_memory_value(MemoryItem.FROST_THIS_BATTLE))

    def test_frozen_core_not_enough_slots(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.FROZEN_CORE: 1}, orb_slots=1,
                                 orbs=[(OrbId.LIGHTNING, 1)])
        play = self.when_playing_the_first_card(state)
        state.end_turn()
        self.see_orb_count(play, 1)
        self.assertEqual(OrbId.LIGHTNING, play.state.orbs[0][0])

    def test_charons_ashes(self):
        state = self.given_state(CardId.VOID, targets=2, relics={RelicId.CHARONS_ASHES: 1})
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_playing_the_whole_hand(state)
        state.end_turn()
        self.see_enemy_lost_hp(play, 3, enemy_index=0)
        self.see_enemy_lost_hp(play, 3, enemy_index=1)
        self.see_player_exhaust_count(play, 1)

    def test_medical_kit(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.MEDICAL_KIT: 1})
        for i in range(5):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        state.end_turn()
        self.see_player_exhaust_count(play, 5)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)
        self.see_enemy_lost_hp(play, 6)

    def test_cracked_orb_increases_thunder_strike_damage(self):
        state = self.given_state(CardId.THUNDER_STRIKE, targets=2, relics={RelicId.CRACKED_CORE: 1})
        state.add_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE, 0)
        play = self.when_playing_the_first_card(state)
        self.see_random_damage_dealt(play, 7)
        self.see_player_spent_energy(play, 3)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE))

    def test_magic_flower_increases_healing(self):
        state = self.given_state(CardId.BANDAGE_UP, relics={RelicId.MAGIC_FLOWER: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, -6)

    def test_magic_flower_healing_removes_decimals(self):
        state = self.given_state(CardId.INFLAME, relics={RelicId.MAGIC_FLOWER: 1, RelicId.BIRD_FACED_URN: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, -3)

    def test_gold_plated_cables(self):
        state = self.given_state(CardId.WOUND, orbs=[(OrbId.LIGHTNING, 1), (OrbId.LIGHTNING, 1), (OrbId.FROST, 1)],
                                 relics={RelicId.GOLD_PLATED_CABLES: 1})
        play = self.when_playing_the_whole_hand(state)
        state.end_turn()
        self.see_enemy_lost_hp(play, 9)

    def test_mark_of_the_bloom(self):
        state = self.given_state(CardId.BANDAGE_UP, relics={RelicId.MARK_OF_THE_BLOOM: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_lost_hp(play, 0)

    def test_necronomicon_triggers(self):
        state = self.given_state(CardId.CARNAGE, relics={RelicId.NECRONOMICON: 1})
        self.assertEqual(1, state.get_memory_value(MemoryItem.NECRONOMICON_READY))
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 40)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.NECRONOMICON_READY))

    def test_necronomicon_does_not_trigger(self):
        state = self.given_state(CardId.CARNAGE, relics={RelicId.NECRONOMICON: 1})
        state.add_memory_value(MemoryItem.NECRONOMICON_READY, -1)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.NECRONOMICON_READY))

    def test_necronomicon_duplication_stops_when_enemy_is_dead_but_still_reduces_counter(self):
        state = self.given_state(CardId.CARNAGE, relics={RelicId.INK_BOTTLE: 0, RelicId.NECRONOMICON: 1})
        self.assertEqual(1, state.get_memory_value(MemoryItem.NECRONOMICON_READY))
        state.monsters[0].current_hp = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 1)
        self.assertEqual(0, play.state.get_memory_value(MemoryItem.NECRONOMICON_READY))

    def test_chemical_x_increases_x_cost_cards_when_there_is_energy(self):
        state = self.given_state(CardId.WHIRLWIND, relics={RelicId.CHEMICAL_X: 1})
        state.player.energy = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)
        self.see_player_has_energy(play, 0)

    def test_chemical_x_increases_x_cost_cards_when_there_is_no_energy(self):
        state = self.given_state(CardId.WHIRLWIND, relics={RelicId.CHEMICAL_X: 1})
        state.player.energy = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_has_energy(play, 0)

    def test_runic_pyramid_holds_onto_hand(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.RUNIC_PYRAMID: 1})
        state.hand.append(get_card(CardId.DEFEND_G))
        state.hand.append(get_card(CardId.DEFEND_G))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_hand_count(play, 2)

    def test_runic_pyramid_does_not_retain_ethereals(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.RUNIC_PYRAMID: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.VOID))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_exhaust_count(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 0)

    def test_runic_pyramid_does_not_retain_auto_played_end_of_turn_cards(self):
        state = self.given_state(CardId.REGRET, relics={RelicId.RUNIC_PYRAMID: 1})
        state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_lost_hp(play, 2)
        self.see_player_exhaust_count(play, 0)
        self.see_player_hand_count(play, 1)
        self.see_player_discard_pile_count(play, 1)

    def test_runic_pyramid_does_not_duplicate_retained_cards(self):
        state = self.given_state(CardId.FLYING_SLEEVES, relics={RelicId.RUNIC_PYRAMID: 1})
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_cards_played(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_runic_pyramid_overlapping_with_equilibrium_and_individual_retain_does_not_duplicate_cards(self):
        state = self.given_state(CardId.FLYING_SLEEVES, relics={RelicId.RUNIC_PYRAMID: 1},
                                 player_powers={PowerId.EQUILIBRIUM: 1})
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_cards_played(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_runic_pyramid_does_not_trigger_retain_effects(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.RUNIC_PYRAMID: 1},
                                 player_powers={PowerId.ESTABLISHMENT: 1})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(1, play.state.hand[0].cost)

    def test_orange_pellets_clear_debuffs_when_triggered(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.ORANGE_PELLETS: 1},
                                 player_powers={PowerId.WEAKENED: 4})
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.INFLAME))
        play = self.when_making_the_most_plays(state)
        self.see_player_has_power(play, PowerId.WEAKENED, 0)

    def test_orange_pellets_does_nothing_if_not_triggerd(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.ORANGE_PELLETS: 1},
                                 player_powers={PowerId.WEAKENED: 4})
        state.hand.append(get_card(CardId.DEFEND_R))
        play = self.when_making_the_most_plays(state)
        self.see_player_has_power(play, PowerId.WEAKENED, 4)

    def test_golden_eye(self):
        state = self.given_state(CardId.CUT_THROUGH_FATE, relics={RelicId.GOLDEN_EYE: 1})
        play = self.when_playing_the_whole_hand(state)
        self.see_player_scryed(play, 4)

    def test_calipers_saves_minus_15_block_for_next_turn(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.CALIPERS: 1})
        state.player.block = 20
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 20)
        self.assertEqual(5, play.state.saved_block_for_next_turn)

    def test_calipers_does_not_save_less_than_15_block_for_next_turn(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.CALIPERS: 1})
        state.player.block = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 3)
        self.assertEqual(0, play.state.saved_block_for_next_turn)

    def test_duality(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.DUALITY: 1})
        state.hand.append(get_card(CardId.TERROR))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_cards_played(play, 2)
        self.see_player_has_power(play, PowerId.FAKE_DEXTERITY_TEMP, 1)

    def test_lizard_tail_heals(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.LIZARD_TAIL: -1})
        state.monsters[0].hits = 1
        state.monsters[0].damage = 6
        state.player.current_hp = 5
        state.player.max_hp = 100
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 0)
        self.see_relic_value(play, RelicId.LIZARD_TAIL, -2)

    def test_lizard_tail_heals_prevents_overspill_damage(self):
        state = self.given_state(CardId.WOUND, relics={RelicId.LIZARD_TAIL: -1})
        state.monsters[0].hits = 2
        state.monsters[0].damage = 10
        state.player.current_hp = 5
        state.player.max_hp = 100
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 10)
        self.see_relic_value(play, RelicId.LIZARD_TAIL, -2)
