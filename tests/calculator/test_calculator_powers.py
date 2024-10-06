from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.memory_items import MemoryItem


class CalculatorPowersTest(CalculatorTestFixture):

    def test_correct_statuses_lose_stacks_after_turn_end(self):
        pass

    def test_strength_adds_to_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STRENGTH: 4})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)

    def test_strength_adds_to_multi_attack(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.STRENGTH: 3})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 16)

    def test_strength_when_negative(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STRENGTH: -1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)

    def test_strength_when_damage_below_zero(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STRENGTH: -100})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_cards_played(play, 1)

    def test_strength_does_not_add_to_self_damage(self):
        state = self.given_state(CardId.BLOODLETTING, player_powers={PowerId.STRENGTH: 3})
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 3)

    def test_dexterity_adds_to_block(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.DEXTERITY: 3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 8)

    def test_dexterity_when_negative(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.DEXTERITY: -3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 2)

    def test_dexterity_when_block_would_be_below_zero(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.DEXTERITY: -13})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 0)
        self.see_cards_played(play, 1)

    def test_vulnerable_when_attacking(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 9)

    def test_vulnerable_with_multi_attack_when_attacking(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 14)

    def test_vulnerable_when_defending(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.VULNERABLE: 1})
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 15)

    def test_vulnerable_with_multi_attack_when_defending(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.VULNERABLE: 1})
        state.monsters[0].damage = 7
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 20)

    def test_weak_when_attacking(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.WEAKENED: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 4)

    def test_weak_with_multi_attack_when_attacking(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.WEAKENED: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)

    def test_weak_when_defending(self):
        state = self.given_state(CardId.NEUTRALIZE)
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        play.end_turn()
        self.see_player_lost_hp(play, 7)

    def test_weak_when_defending_no_rounding_needed(self):
        state = self.given_state(CardId.NEUTRALIZE)
        state.monsters[0].damage = 20
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        play.end_turn()
        self.see_player_lost_hp(play, 15)

    def test_weak_with_multi_attack_when_defending(self):
        state = self.given_state(CardId.NEUTRALIZE)
        state.monsters[0].damage = 20
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 1)
        play.end_turn()
        self.see_player_lost_hp(play, 30)

    def test_frail(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.FRAIL: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 3)

    def test_entangled_no_attacks_played(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.ENTANGLED: 1})
        play = self.when_playing_the_first_card(state)
        self.see_cards_played(play, 0)

    def test_vigor(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.VIGOR: 8})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 14)
        self.see_player_does_not_have_power(play, PowerId.VIGOR)

    def test_curl_up(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.monsters[0].powers[PowerId.CURL_UP] = 8
        play = self.when_playing_the_whole_hand(state)
        self.see_cards_played(play, 2)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_block_is(play, 2)

    def test_artifact_blocks_debuff(self):
        state = self.given_state(CardId.BASH)
        state.monsters[0].powers[PowerId.ARTIFACT] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)
        self.see_enemy_has_power(play, PowerId.ARTIFACT, 0)

    def test_artifact_blocks_negative_buff(self):
        state = self.given_state(CardId.DARK_SHACKLES)
        state.monsters[0].powers[PowerId.ARTIFACT] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_does_not_have_power(play, PowerId.ARTIFACT)
        self.see_enemy_does_not_have_power(play, PowerId.STRENGTH)

    def test_artifact_does_not_block_buff(self):
        state = self.given_state(CardId.INFLAME, player_powers={PowerId.ARTIFACT: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ARTIFACT, 1)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)

    def test_artifact_multiple_debuffs(self):
        state = self.given_state(CardId.UPPERCUT)
        state.monsters[0].powers[PowerId.ARTIFACT] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 1)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 0)
        self.see_enemy_has_power(play, PowerId.ARTIFACT, 0)

    def test_artifact_multiple_stacks(self):
        state = self.given_state(CardId.UPPERCUT)
        state.monsters[0].powers[PowerId.ARTIFACT] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_enemy_has_power(play, PowerId.VULNERABLE, 0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 0)
        self.see_enemy_has_power(play, PowerId.ARTIFACT, 1)

    def test_plated_armor_adds_block(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.PLATED_ARMOR: 4})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 4)

    def test_plated_armor_gets_reduced_by_attack_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.PLATED_ARMOR: 4})
        state.player.block = 0
        state.monsters[0].damage = 5
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 6)
        self.see_player_has_power(play, PowerId.PLATED_ARMOR, 2)

    def test_plated_armor_does_not_get_reduced_by_orb_damage(self):
        state = self.given_state(CardId.DUALCAST, orb_slots=3, orbs=[(OrbId.LIGHTNING, 1)])
        state.monsters[0].powers[PowerId.PLATED_ARMOR] = 4
        # Technically wrong because we don't model Block from Plated Armor on monsters since it's handled by the game
        state.monsters[0].block = 4
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)
        self.see_enemy_has_power(play, PowerId.PLATED_ARMOR, 4)

    def test_buffer_blocks_incoming_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.BUFFER: 1})
        state.monsters[0].damage = 999
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 0)
        self.see_player_does_not_have_power(play, PowerId.BUFFER)

    def test_buffer_consumed_by_self_damage(self):
        state = self.given_state(CardId.BLOODLETTING, player_powers={PowerId.BUFFER: 1})
        state.monsters[0].damage = 8
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 8)
        self.see_player_does_not_have_power(play, PowerId.BUFFER)

    def test_multiple_buffer_stacks(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.BUFFER: 3})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 10
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 7)
        self.see_player_does_not_have_power(play, PowerId.BUFFER)

    def test_rage_adds_block_for_attack(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.RAGE: 3})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_block(play, 6)

    def test_rage_does_not_add_block_for_skill(self):
        state = self.given_state(CardId.BLOODLETTING, player_powers={PowerId.RAGE: 3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 0)

    def test_metallicize_adds_block(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.METALLICIZE: 3})
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_block(play, 3)

    def test_metallicize_adds_block_stacking_with_orichalcum(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.METALLICIZE: 3},
                                 relics={RelicId.ORICHALCUM: 1})
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_has_block(play, 9)

    def test_intangible_player_blocks_all_but_one_damage(self):
        state = self.given_state(CardId.STRIKE_R, targets=2, player_powers={PowerId.INTANGIBLE_PLAYER: 1})
        state.monsters[0].damage = 999
        state.monsters[0].hits = 1
        state.monsters[1].damage = 1
        state.monsters[1].hits = 5
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 6)

    def test_intangible_player_with_tungsten_rod_blocks_all_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.INTANGIBLE_PLAYER: 1},
                                 relics={RelicId.TUNGSTEN_ROD: 1})
        state.monsters[0].damage = 999
        state.monsters[0].hits = 20
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 0)

    def test_intangible_also_applies_to_block_damage(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.INTANGIBLE_PLAYER: 1})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 6
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 1)

    def test_intangible_player_blocks_self_damage(self):
        state = self.given_state(CardId.BLOODLETTING, targets=2, player_powers={PowerId.INTANGIBLE_PLAYER: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 1)

    def test_intangible_enemy_blocks_all_but_one_damage(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.INTANGIBLE_ENEMY] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 2)

    def test_flame_barrier_deals_damage_to_attacker(self):
        state = self.given_state(CardId.FLAME_BARRIER)
        state.monsters[0].damage = 1
        state.monsters[0].hits = 4
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 16)

    def test_flame_barrier_blocked_by_block(self):
        state = self.given_state(CardId.FLAME_BARRIER)
        state.monsters[0].damage = 1
        state.monsters[0].hits = 4
        state.monsters[0].powers = {PowerId.BARRICADE: 1}
        state.monsters[0].block = 10
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 6)

    def test_attacker_dies_to_flame_barrier_and_then_their_attack_stops(self):
        state = self.given_state(CardId.FLAME_BARRIER)
        state.monsters[0].damage = 1
        state.monsters[0].hits = 999
        state.monsters[0].current_hp = 20
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 0)
        self.see_enemy_hp_is(play, 0)

    def test_thorns_deals_damage(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.THORNS: 3})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 4
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 12)

    def test_thorns_deals_damage_when_attacked_for_0(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.THORNS: 3})
        state.monsters[0].damage = 0
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 6)

    def test_thorns_will_not_prevent_damage_defensively(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.THORNS: 3})
        state.monsters[0].current_hp = 3
        state.monsters[0].damage = 5
        state.monsters[0].hits = 1
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_enemy_hp_is(play, 0)
        self.see_player_lost_hp(play, 5)

    def test_thorns_will_hurt_even_if_the_target_having_thorns_dies(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].current_hp = 3
        state.monsters[0].powers = {PowerId.THORNS: 3}
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_enemy_hp_is(play, 0)
        self.see_player_lost_hp(play, 3)

    def test_sharp_hide_deals_damage_only_on_attack_play(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.SHARP_HIDE] = 4
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 4)

    def test_self_block_effects_block_return_happen_before_thorns(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.THORNS] = 3
        state.monsters[0].powers[PowerId.BLOCK_RETURN] = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 2)
        self.see_player_lost_hp(play, 0)

    def test_self_block_effects_block_return_happen_before_sharp_hide(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.THORNS] = 3
        state.monsters[0].powers[PowerId.BLOCK_RETURN] = 4
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 1)
        self.see_player_lost_hp(play, 0)

    def test_self_block_effects_rage_happen_before_thorns(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.RAGE: 5})
        state.monsters[0].powers[PowerId.THORNS] = 3
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 2)
        self.see_player_lost_hp(play, 0)

    def test_self_block_effects_wallop_happen_before_thorns(self):
        state = self.given_state(CardId.WALLOP)
        state.monsters[0].powers[PowerId.THORNS] = 3
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 6)
        self.see_player_lost_hp(play, 0)

    def test_reaper_before_thorns(self):
        state = self.given_state(CardId.REAPER)
        state.player.current_hp = 2
        state.monsters[0].powers[PowerId.THORNS] = 3
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 47)

    def test_self_block_effects_wallop_happen_before_sharp_hide(self):
        state = self.given_state(CardId.WALLOP)
        state.monsters[0].powers[PowerId.SHARP_HIDE] = 3
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 6)
        self.see_player_lost_hp(play, 0)

    def test_reaper_before_sharp_hide(self):
        state = self.given_state(CardId.REAPER)
        state.player.current_hp = 2
        state.monsters[0].powers[PowerId.SHARP_HIDE] = 3
        play = self.when_playing_the_first_card(state)
        self.see_player_lost_hp(play, 47)

    def test_attacking_angry_gives_strength(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.ANGRY] = 3
        state.monsters[0].damage = 1
        state.monsters[0].hits = 2
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 14)

    def test_playing_a_skill_when_anger_nob_present_gives_strength(self):
        state = self.given_state(CardId.DEFEND_G)
        state.monsters[0].powers[PowerId.ANGER_NOB] = 2
        state.monsters[0].damage = 5
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 2)

    def test_only_the_monster_with_anger_nob_gets_strength_up(self):
        state = self.given_state(CardId.DEFEND_G, targets=2)
        state.monsters[0].powers[PowerId.ANGER_NOB] = 2
        state.monsters[0].damage = 5
        state.monsters[0].hits = 1
        state.monsters[1].damage = 5
        state.monsters[1].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.STRENGTH, 2, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.STRENGTH, 0, enemy_index=1)

    def test_flight_reduces_damage(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.FLIGHT] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 4)
        self.see_enemy_has_power(play, PowerId.FLIGHT, 1)

    def test_flight_popped_causes_stun(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.FLIGHT] = 2
        state.monsters[0].damage = 999
        state.monsters[0].hits = 999
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 0)
        self.see_enemy_lost_hp(play, 4)
        self.see_enemy_does_not_have_power(play, PowerId.FLIGHT)

    def test_no_draw_prevents_draw(self):
        state = self.given_state(CardId.POMMEL_STRIKE, player_powers={PowerId.NO_DRAW: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_no_draw_blocked_by_artifact(self):
        state = self.given_state(CardId.BATTLE_TRANCE, player_powers={PowerId.ARTIFACT: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_hand_count(play, 3)
        self.see_player_discard_pile_count(play, 1)
        self.see_player_does_not_have_power(play, PowerId.ARTIFACT)
        self.see_player_does_not_have_power(play, PowerId.NO_DRAW)

    def test_split_removes_enemy_attack(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].damage = 13
        state.monsters[0].hits = 2
        state.monsters[0].current_hp = 46
        state.monsters[0].max_hp = 80
        state.monsters[0].powers = {PowerId.SPLIT: 1}
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_does_not_have_power(play, PowerId.SPLIT)
        self.see_player_lost_hp(play, 0)

    def test_not_quite_split_does_nothing(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].damage = 13
        state.monsters[0].hits = 2
        state.monsters[0].current_hp = 47
        state.monsters[0].max_hp = 80
        state.monsters[0].powers = {PowerId.SPLIT: 1}
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_has_power(play, PowerId.SPLIT, 1)
        self.see_player_lost_hp(play, 26)

    def test_mode_shift_removes_enemy_attack(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].damage = 13
        state.monsters[0].hits = 2
        state.monsters[0].powers = {PowerId.MODE_SHIFT: 1}
        play = self.when_playing_the_first_card(state)
        self.see_enemy_block_is(play, 20)
        play.end_turn()
        self.see_enemy_does_not_have_power(play, PowerId.MODE_SHIFT)
        self.see_player_lost_hp(play, 0)

    def test_mode_does_nothing_when_not_broken(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].damage = 13
        state.monsters[0].hits = 2
        state.monsters[0].powers = {PowerId.MODE_SHIFT: 8}
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_has_power(play, PowerId.MODE_SHIFT, 2)
        self.see_player_lost_hp(play, 26)
        self.see_enemy_block_is(play, 0)
        self.see_enemy_lost_hp(play, 6)

    def test_mode_shift_blocks(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].damage = 13
        state.monsters[0].hits = 2
        state.monsters[0].powers = {PowerId.MODE_SHIFT: 5}
        play = self.when_playing_the_first_card(state)
        self.see_enemy_block_is(play, 15)
        play.end_turn()
        self.see_enemy_does_not_have_power(play, PowerId.MODE_SHIFT)
        self.see_enemy_lost_hp(play, 5)

    def test_a_thousand_cuts_damage(self):
        state = self.given_state(CardId.DEFEND_G, player_powers={PowerId.THOUSAND_CUTS: 1})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 1)

    def test_after_image_block(self):
        state = self.given_state(CardId.STRIKE_G, player_powers={PowerId.AFTER_IMAGE: 1})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 0)

    def test_time_warp_not_incremented_when_not_present(self):
        state = self.given_state(CardId.STRIKE_R)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_does_not_have_power(play, PowerId.TIME_WARP)

    def test_time_warp_incremented_by_card_plays(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.hand.append(get_card(CardId.STRIKE_R))
        state.monsters[0].powers[PowerId.TIME_WARP] = 0
        play = self.when_playing_the_whole_hand(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_enemy_has_power(play, PowerId.TIME_WARP, 3)

    def test_time_warp_caps_card_plays(self):
        state = self.given_state(CardId.CLEAVE)
        state.hand.append(get_card(CardId.CLEAVE))
        state.hand.append(get_card(CardId.CLEAVE))
        state.monsters[0].powers[PowerId.TIME_WARP] = 10
        play = self.when_playing_the_whole_hand(state)
        # see that only 2 of the 3 cleaves are played because time warp stops it
        self.see_cards_played(play, 2)
        self.see_enemy_lost_hp(play, 16)
        self.see_enemy_has_power(play, PowerId.TIME_WARP, 12)

    def test_poison_damages_and_decrements(self):
        state = self.given_state(CardId.WOUND)
        state.monsters[0].powers[PowerId.POISON] = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.POISON, 2)

    def test_poison_kills_and_so_prevents_damage(self):
        state = self.given_state(CardId.WOUND)
        state.monsters[0].powers[PowerId.POISON] = 3
        state.monsters[0].current_hp = 3
        state.monsters[0].damage = 7
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_hp_is(play, 0)
        self.see_player_lost_hp(play, 0)

    def test_damaging_shifter_reduces_incoming_damage(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.SHIFTING] = 1
        state.monsters[0].damage = 7
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 6)
        self.see_player_lost_hp(play, 1)

    def test_damaging_shifter_more_complicated(self):
        state = self.given_state(CardId.NEUTRALIZE)
        state.monsters[0].powers[PowerId.SHIFTING] = 1
        state.monsters[0].powers[PowerId.STRENGTH] = -3
        state.monsters[0].damage = 20  # Strength-unadjusted damage
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 3)
        self.see_enemy_has_power(play, PowerId.STRENGTH, -6)
        self.see_player_lost_hp(play, 10)

    def test_damaging_shifter_reduces_incoming_damage_in_bigger_fight(self):
        state = self.given_state(CardId.STRIKE_R, targets=2)
        state.monsters[0].powers[PowerId.SHIFTING] = 1
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        state.monsters[1].damage = 1
        state.monsters[1].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 6, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_player_lost_hp(play, 1)

    def test_damaging_non_shifter_does_not_reduces_incoming_damage_in_bigger_fight(self):
        state = self.given_state(CardId.STRIKE_R, targets=2)
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        state.monsters[1].powers[PowerId.SHIFTING] = 1
        state.monsters[1].damage = 1
        state.monsters[1].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 6, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_player_lost_hp(play, 2)

    def test_damaging_all_in_bigger_fight_that_includes_shifter_does_reduce_damage(self):
        state = self.given_state(CardId.CLEAVE, targets=2)
        state.monsters[0].powers[PowerId.SHIFTING] = 1
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        state.monsters[1].damage = 1
        state.monsters[1].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 8, enemy_index=0)
        self.see_enemy_lost_hp(play, 8, enemy_index=1)
        self.see_player_lost_hp(play, 1)

    def test_constricted_does_damage(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.CONSTRICTED: 10})
        state.monsters[0].damage = 1
        state.monsters[0].hits = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 11)

    def test_malleable_blocks(self):
        state = self.given_state(CardId.CLEAVE)
        state.monsters[0].powers[PowerId.MALLEABLE] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.MALLEABLE, 4)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_block_is(play, 4)

    def test_malleable_blocks_after_double_attack(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.MALLEABLE] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.MALLEABLE, 5)
        self.see_enemy_lost_hp(play, 10)
        self.see_enemy_block_is(play, 9)

    def test_malleable_blocks_after_triple_attack(self):
        state = self.given_state(CardId.EVISCERATE)
        state.monsters[0].powers[PowerId.MALLEABLE] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.MALLEABLE, 6)
        self.see_enemy_lost_hp(play, 21)
        self.see_enemy_block_is(play, 15)

    def test_choked_causes_card_plays_to_damage(self):
        state = self.given_state(CardId.DEFEND_R)
        state.monsters[0].powers[PowerId.CHOKED] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 3)

    def test_only_the_monster_with_choked_gets_damaged_by_it(self):
        state = self.given_state(CardId.DEFEND_G, targets=2)
        state.monsters[0].powers[PowerId.CHOKED] = 2
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 2, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)

    def test_envenom_power_does_not_work_on_blocked_hit(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.ENVENOM: 1})
        state.monsters[0].block = 10
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ENVENOM, 1)
        self.see_enemy_block_is(play, 4)
        self.see_enemy_lost_hp(play, 0)
        self.see_enemy_does_not_have_power(play, PowerId.POISON)

    def test_envenom_power_applies_poison_on_unblocked_hit(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.ENVENOM: 1})
        state.monsters[0].block = 5
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ENVENOM, 1)
        self.see_enemy_block_is(play, 0)
        self.see_enemy_lost_hp(play, 1)
        self.see_enemy_has_power(play, PowerId.POISON, 1)

    def test_envenom_power_applies_poison_on_unblocked_multi_hit(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.ENVENOM: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ENVENOM, 1)
        self.see_enemy_lost_hp(play, 10)
        self.see_enemy_has_power(play, PowerId.POISON, 2)

    def test_envenom_power_stacks_onto_existing_poison(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.ENVENOM: 1})
        state.monsters[0].powers[PowerId.POISON] = 1
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.ENVENOM, 1)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_has_power(play, PowerId.POISON, 2)

    def test_corpse_explosion_deals_max_hp_damage_when_killed_actively(self):
        state = self.given_state(CardId.STRIKE_R, targets=2)
        state.monsters[0].powers[PowerId.CORPSE_EXPLOSION] = 1
        state.monsters[0].current_hp = 1
        state.monsters[0].max_hp = 10
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, state.monsters[0].max_hp, enemy_index=1)

    def test_corpse_explosion_deals_max_hp_damage_when_killed_passively(self):
        state = self.given_state(CardId.WOUND, targets=2)
        state.monsters[0].powers[PowerId.POISON] = 1
        state.monsters[0].powers[PowerId.CORPSE_EXPLOSION] = 1
        state.monsters[0].current_hp = 1
        state.monsters[0].max_hp = 50
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_hp_is(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, state.monsters[0].max_hp, enemy_index=1)

    def test_corpse_explosion_stacked_deals_more_damage(self):
        state = self.given_state(CardId.WOUND, targets=2)
        state.monsters[0].powers[PowerId.POISON] = 1
        state.monsters[0].powers[PowerId.CORPSE_EXPLOSION] = 2
        state.monsters[0].current_hp = 1
        state.monsters[0].max_hp = 50
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_hp_is(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play,
                               state.monsters[0].max_hp * 2, enemy_index=1)

    def test_wraith_form_power_decreases_dexterity_on_turn_end(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.WRAITH_FORM_POWER: 1})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_power(play, PowerId.DEXTERITY, -1)

    def test_wraith_form_power_dexterity_losses_stack(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.WRAITH_FORM_POWER: 1, PowerId.DEXTERITY: -3})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_power(play, PowerId.DEXTERITY, -4)

    def test_double_damage_doubles_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.DOUBLE_DAMAGE: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)

    def test_double_damage_doubles_damage_multi_hit(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.DOUBLE_DAMAGE: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 20)

    def test_double_damage_against_intangible(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.DOUBLE_DAMAGE: 1})
        state.monsters[0].powers[PowerId.INTANGIBLE_ENEMY] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 2)

    def test_juggernaut_block_from_card(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.JUGGERNAUT: 5})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 5)
        self.see_random_damage_dealt(play, 0)

    def test_juggernaut_block_from_power(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.JUGGERNAUT: 7, PowerId.METALLICIZE: 4}, targets=2)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 0)
        play.end_turn()
        self.see_enemy_lost_hp(play, 0, enemy_index=0)
        self.see_enemy_lost_hp(play, 0, enemy_index=1)
        self.see_random_damage_dealt(play, 7)

    def test_juggernaut_block_from_block_return(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.JUGGERNAUT: 5})
        state.monsters[0].powers[PowerId.BLOCK_RETURN] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 11)

    def test_juggernaut_does_not_damage_when_0_block_gained(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.JUGGERNAUT: 5, PowerId.DEXTERITY: -5})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_random_damage_dealt(play, 0)

    def test_panache_counter_decrements(self):
        state = self.given_state(CardId.DEFEND_R)
        state.add_memory_value(MemoryItem.PANACHE_DAMAGE, 10)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(4, play.state.get_memory_value(MemoryItem.PANACHE_COUNTER))

    def test_panache_counter_decrements_only_when_panache_damage_present(self):
        state = self.given_state(CardId.DEFEND_R)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.assertEqual(5, play.state.get_memory_value(MemoryItem.PANACHE_COUNTER))

    def test_panache_triggers_and_resets_when_counter_0(self):
        state = self.given_state(CardId.DEFEND_R)
        state.memory_general[MemoryItem.PANACHE_COUNTER] = 1
        state.add_memory_value(MemoryItem.PANACHE_DAMAGE, 22)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 22)
        self.assertEqual(5, play.state.get_memory_value(MemoryItem.PANACHE_COUNTER))

    def test_sadistic_triggers(self):
        state = self.given_state(CardId.BLIND, player_powers={PowerId.SADISTIC: 5})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)
        self.see_enemy_lost_hp(play, 5)

    def test_sadistic_triggers_on_multi_hit(self):
        state = self.given_state(CardId.BOUNCING_FLASK, player_powers={PowerId.SADISTIC: 5})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 9)
        self.see_enemy_lost_hp(play, 15)

    def test_sadistic_envenom_interaction(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.SADISTIC: 5, PowerId.ENVENOM: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 1)
        self.see_enemy_lost_hp(play, 11)

    def test_sadistic_should_not_damage_player(self):
        state = self.given_state(CardId.DOUBT, player_powers={PowerId.SADISTIC: 5})
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_has_power(play, PowerId.WEAKENED, 1)
        self.see_player_lost_hp(play, 0)

    def test_heatsinks_does_not_trigger_its_own_power_when_played(self):
        state = self.given_state(CardId.HEATSINKS)
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.HEATSINK, 1)
        self.see_player_drew_cards(play, 0)

    def test_heatsink(self):
        state = self.given_state(CardId.INFLAME, player_powers={PowerId.HEATSINK: 2})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)
        self.see_player_drew_cards(play, 2)

    def test_heatsink_hand_limit(self):
        state = self.given_state(CardId.INFLAME, player_powers={PowerId.HEATSINK: 2})
        for i in range(9):
            state.hand.append(get_card(CardId.WOUND))
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 2)
        self.see_player_drew_cards(play, 1)

    def test_electrodynamics(self):
        state = self.given_state(CardId.ELECTRODYNAMICS, orb_slots=3, targets=2)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_power(play, PowerId.ELECTRO, 1)
        self.see_enemy_lost_hp(play, 6, enemy_index=0)
        self.see_enemy_lost_hp(play, 6, enemy_index=1)

    def test_electrodynamics_evokes(self):
        state = self.given_state(CardId.ELECTRODYNAMICS, orb_slots=2, orbs=[(OrbId.LIGHTNING, 1)], targets=2)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_power(play, PowerId.ELECTRO, 1)
        self.see_enemy_lost_hp(play, 14, enemy_index=0)
        self.see_enemy_lost_hp(play, 14, enemy_index=1)

    def test_storm(self):
        state = self.given_state(CardId.INFLAME, orb_slots=3, player_powers={PowerId.STORM: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STORM, 1)
        self.see_orb_count(play, 1)

    def test_storm_multiple(self):
        state = self.given_state(CardId.INFLAME, orb_slots=3, player_powers={PowerId.STORM: 2})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STORM, 2)
        self.see_orb_count(play, 2)

    def test_lock_on_applies_on_passive(self):
        state = self.given_state(CardId.WOUND, orb_slots=3, orbs=[(OrbId.LIGHTNING, 1)])
        state.monsters[0].powers[PowerId.LOCK_ON] = 2
        play = self.when_playing_the_first_card(state)
        state.end_turn()
        self.see_orb_count(play, 1)
        self.see_enemy_lost_hp(play, 4)

    def test_lock_on_applies_on_evoke(self):
        state = self.given_state(CardId.ZAP, orb_slots=1, orbs=[(OrbId.DARK, 6)])
        state.monsters[0].powers[PowerId.LOCK_ON] = 2
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 1)
        self.see_enemy_lost_hp(play, 9)

    def test_echo_form_duplicates_card_play_when_ready(self):
        state = self.given_state(CardId.ZAP, orb_slots=3,
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1})
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 2)

    def test_echo_form_is_blocked_by_time_warp(self):
        state = self.given_state(CardId.ZAP, orb_slots=3,
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1})
        state.monsters[0].powers[PowerId.TIME_WARP] = 11
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 1)
        self.see_enemy_has_power(play, PowerId.TIME_WARP, 12)

    def test_echo_form_is_blocked_by_choker(self):
        state = self.given_state(CardId.ZAP, orb_slots=3, relics={RelicId.VELVET_CHOKER: 5},
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1})
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 1)

    def test_echo_form_duplication_applies_to_counters(self):
        relics = {RelicId.INK_BOTTLE: 0, RelicId.PEN_NIB: 0, RelicId.LETTER_OPENER: 0}
        state = self.given_state(CardId.ZAP, orb_slots=3, relics=relics,
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1})
        play = self.when_playing_the_first_card(state)
        self.see_orb_count(play, 2)
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.PEN_NIB, 0)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 2)
        self.see_relic_value(play, RelicId.LETTER_OPENER, 2)

    def test_echo_form_duplication_does_not_double_dip_on_vigor(self):
        state = self.given_state(CardId.STRIKE_R, orb_slots=3,
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1,
                                                PowerId.VIGOR: 8})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6 + 8 + 6)
        self.see_player_does_not_have_power(play, PowerId.VIGOR)

    def test_echo_form_duplication_stops_when_enemy_is_dead(self):
        state = self.given_state(CardId.STRIKE_R, orb_slots=3, relics={RelicId.INK_BOTTLE: 0},
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1})
        state.monsters[0].current_hp = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 1)
        self.see_player_has_power(play, PowerId.INTERNAL_ECHO_FORM_READY, 1)

    def test_echo_form_duplication_stops_when_battle_is_over(self):
        state = self.given_state(CardId.SWEEPING_BEAM, orb_slots=3, relics={RelicId.INK_BOTTLE: 0}, targets=2,
                                 player_powers={PowerId.ECHO_FORM: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1})
        state.monsters[0].current_hp = 1
        state.monsters[1].current_hp = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 1)
        self.see_player_has_power(play, PowerId.INTERNAL_ECHO_FORM_READY, 1)

    def test_echo_form_multiple_stacks_with_multiple_cards(self):
        state = self.given_state(CardId.ZAP, orb_slots=5,
                                 player_powers={PowerId.ECHO_FORM: 2, PowerId.INTERNAL_ECHO_FORM_READY: 2})
        state.hand.append(get_card(CardId.ZAP))
        play = self.when_playing_the_whole_hand(state)
        self.see_orb_count(play, 4)
        self.see_player_spent_energy(play, 2)

    def test_echo_form_multiple_stacks_with_single_card(self):
        state = self.given_state(CardId.ZAP, orb_slots=5,
                                 player_powers={PowerId.ECHO_FORM: 2, PowerId.INTERNAL_ECHO_FORM_READY: 2})
        play = self.when_playing_the_whole_hand(state)
        self.see_orb_count(play, 2)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_power(play, PowerId.INTERNAL_ECHO_FORM_READY, 1)

    def test_amplify_doubles_powers(self):
        state = self.given_state(CardId.INFLAME, player_powers={PowerId.AMPLIFY: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 4)

    def test_amplify_doubles_powers_multiple_times(self):
        state = self.given_state(CardId.INFLAME, player_powers={PowerId.AMPLIFY: 2})
        state.hand.append(get_card(CardId.INFLAME))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 8)

    def test_amplify_stops_when_empty(self):
        state = self.given_state(CardId.INFLAME, player_powers={PowerId.AMPLIFY: 1})
        state.hand.append(get_card(CardId.INFLAME))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_has_power(play, PowerId.STRENGTH, 6)

    def test_amplify_only_doubles_powers(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.AMPLIFY: 2})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 5)

    def test_burst_doubles_skills(self):
        state = self.given_state(CardId.DEADLY_POISON, player_powers={PowerId.BURST: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 10)

    def test_burst_only_doubles_skills(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.BURST: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)

    def test_burst_duplication_stops_when_enemy_is_dead_but_still_reduces_counter(self):
        state = self.given_state(CardId.BLIND, orb_slots=3, relics={RelicId.INK_BOTTLE: 0},
                                 player_powers={PowerId.BURST: 1, PowerId.SADISTIC: 1})
        state.monsters[0].current_hp = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 1)
        self.see_player_has_power(play, PowerId.BURST, 0)

    def test_double_tap_doubles_attacks(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.DOUBLE_TAP: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)

    def test_double_tap_only_doubles_attacks(self):
        state = self.given_state(CardId.DEADLY_POISON, player_powers={PowerId.DOUBLE_TAP: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.POISON, 5)

    def test_double_tap_duplication_stops_when_enemy_is_dead_but_still_reduces_counter(self):
        state = self.given_state(CardId.STRIKE_R, orb_slots=3, relics={RelicId.INK_BOTTLE: 0},
                                 player_powers={PowerId.DOUBLE_TAP: 1})
        state.monsters[0].current_hp = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 1)
        self.see_player_has_power(play, PowerId.DOUBLE_TAP, 0)

    def test_duplication_potion_power_doubles_things(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.DUPLICATION_POTION_POWER: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 12)

    def test_doubling_effects_interacting_with_each_other(self):
        state = self.given_state(CardId.INFLAME,
                                 player_powers={PowerId.AMPLIFY: 1, PowerId.INTERNAL_ECHO_FORM_READY: 1},
                                 relics={RelicId.INK_BOTTLE: 0})
        play = self.when_playing_the_first_card(state)
        self.see_relic_value(play, RelicId.INK_BOTTLE, 3)
        self.see_player_has_power(play, PowerId.STRENGTH, 6)

    def test_curiosity_raises_strength_from_power(self):
        state = self.given_state(CardId.CAPACITOR)
        state.monsters[0].powers[PowerId.CURIOSITY] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.CURIOSITY, 1)
        self.see_enemy_has_power(play, PowerId.STRENGTH, 1)

    def test_curiosity_does_not_trigger_with_non_power(self):
        state = self.given_state(CardId.DEFEND_R)
        state.monsters[0].powers[PowerId.CURIOSITY] = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.CURIOSITY, 1)
        self.see_enemy_has_power(play, PowerId.STRENGTH, 0)

    def test_only_the_monster_with_curiosity_gets_strength_up(self):
        state = self.given_state(CardId.ECHO_FORM, targets=2)
        state.monsters[0].powers[PowerId.CURIOSITY] = 3
        state.monsters[0].damage = 5
        state.monsters[0].hits = 1
        state.monsters[1].damage = 5
        state.monsters[1].hits = 1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.STRENGTH, 3, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.STRENGTH, 0, enemy_index=1)

    def test_explosive_increments(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.EXPLOSIVE] = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_has_power(play, PowerId.EXPLOSIVE, 2)

    def test_explosive_increments_only_on_enemy_that_has_it(self):
        state = self.given_state(CardId.STRIKE_R, targets=2)
        state.monsters[0].powers[PowerId.EXPLOSIVE] = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_has_power(play, PowerId.EXPLOSIVE, 2, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.EXPLOSIVE, 0, enemy_index=1)

    def test_explosive_triggers(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.EXPLOSIVE] = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 30)
        self.see_enemy_has_power(play, PowerId.EXPLOSIVE, 0)

    def test_hex(self):
        state = self.given_state(CardId.DEFEND_G, player_powers={PowerId.HEX: 1})
        state.hand.append(get_card(CardId.DEFEND_G))
        play = self.when_playing_the_whole_hand(state)
        self.see_player_draw_pile_count(play, 2)

    def test_regenerate_enemy_heals(self):
        state = self.given_state(CardId.DEFEND_G)
        state.monsters[0].powers[PowerId.REGENERATE_ENEMY] = 1
        state.monsters[0].current_hp = 99
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 0)

    def test_regenerate_enemy_does_not_revive_enemy(self):
        state = self.given_state(CardId.DEFEND_G)
        state.monsters[0].powers[PowerId.REGENERATE_ENEMY] = 1
        state.monsters[0].current_hp = 0
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 100)

    def test_regeneration_player_heals_and_increments(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.REGENERATION_PLAYER: 4})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, -4)
        self.see_player_has_power(play, PowerId.REGENERATION_PLAYER, 3)

    def test_regeneration_player_does_not_revive_player(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.REGENERATION_PLAYER: 4})
        state.player.current_hp = 1
        state.monsters[0].powers[PowerId.THORNS] = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_lost_hp(play, 50)

    def test_equilibrium_holds_onto_hand(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.EQUILIBRIUM: 1})
        state.hand.append(get_card(CardId.DEFEND_G))
        state.hand.append(get_card(CardId.DEFEND_G))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_hand_count(play, 2)

    def test_equilibrium_does_not_retain_ethereals(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.EQUILIBRIUM: 1})
        state.hand.append(get_card(CardId.WOUND))
        state.hand.append(get_card(CardId.VOID))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_exhaust_count(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 0)

    def test_equilibrium_does_not_retain_auto_played_end_of_turn_cards(self):
        state = self.given_state(CardId.REGRET, player_powers={PowerId.EQUILIBRIUM: 1})
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_lost_hp(play, 1)
        self.see_player_exhaust_count(play, 0)
        self.see_player_hand_count(play, 0)
        self.see_player_discard_pile_count(play, 1)

    def test_equilibrium_does_not_duplicate_retained_cards(self):
        state = self.given_state(CardId.FLYING_SLEEVES, player_powers={PowerId.EQUILIBRIUM: 1})
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_cards_played(play, 1)
        self.see_player_hand_count(play, 2)
        self.see_player_discard_pile_count(play, 1)

    def test_feel_no_pain(self):
        state = self.given_state(CardId.VOID, player_powers={PowerId.FEEL_NO_PAIN: 6})
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_exhaust_count(play, 1)
        self.see_player_has_block(play, 6)

    def test_feel_no_pain_multiple(self):
        state = self.given_state(CardId.VOID, player_powers={PowerId.FEEL_NO_PAIN: 6})
        state.hand.append(get_card(CardId.VOID))
        play = self.when_playing_the_whole_hand(state)
        play.end_turn()
        self.see_player_exhaust_count(play, 2)
        self.see_player_has_block(play, 12)

    def test_dark_embrace(self):
        state = self.given_state(CardId.IMPERVIOUS, player_powers={PowerId.DARK_EMBRACE: 1})
        play = self.when_playing_the_first_card(state)
        self.see_player_exhaust_count(play, 1)
        self.see_player_drew_cards(play, 1)

    def test_corruption(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.CORRUPTION: 1})
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        self.assertEqual(0, play.state.hand[0].cost)
        self.assertEqual(True, play.state.hand[0].exhausts)
        self.assertEqual(1, play.state.hand[1].cost)
        self.assertEqual(False, play.state.hand[1].exhausts)

    def test_establishment_reduces_card_cost(self):
        state = self.given_state(CardId.FLYING_SLEEVES, player_powers={PowerId.ESTABLISHMENT: 1})
        state.hand.append(get_card(CardId.FLYING_SLEEVES))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(0, play.state.hand[0].cost)

    def test_equilibrium_makes_card_eligible_for_retain_effects(self):
        state = self.given_state(CardId.STRIKE_R,
                                 player_powers={PowerId.ESTABLISHMENT: 1, PowerId.EQUILIBRIUM: 1})
        state.hand.append(get_card(CardId.STRIKE_R))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(0, play.state.hand[0].cost)

    def test_establishment_does_not_lower_card_cost_passed_0(self):
        state = self.given_state(CardId.SHIV, player_powers={PowerId.ESTABLISHMENT: 1, PowerId.EQUILIBRIUM: 1})
        state.hand.append(get_card(CardId.SHIV))
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(0, play.state.hand[0].cost)

    def test_study_adds_card_to_draw(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STUDY: 1})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(1, len(play.state.draw_pile))

    def test_study_adds_more_card_to_draw(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STUDY: 2})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(2, len(play.state.draw_pile))

    def test_master_reality_upgrades_created_cards_in_hand(self):
        state = self.given_state(CardId.DECEIVE_REALITY, player_powers={PowerId.MASTER_REALITY: 1})
        play = self.when_playing_the_first_card(state)
        self.assertEqual(CardId.SAFETY, play.state.hand[0].id)
        self.assertEqual(1, play.state.hand[0].upgrade)

    def test_master_reality_upgrades_created_cards_in_draw(self):
        state = self.given_state(CardId.DECEIVE_REALITY, player_powers={PowerId.MASTER_REALITY: 1, PowerId.STUDY: 1})
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.assertEqual(CardId.INSIGHT, play.state.draw_pile[0].id)
        self.assertEqual(1, play.state.draw_pile[0].upgrade)

    def test_wave_of_the_hand(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.WAVE_OF_THE_HAND: 3}, targets=2)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 5)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 3, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 3, enemy_index=1)
        self.see_player_has_power(play, PowerId.WAVE_OF_THE_HAND, 0)

    def test_wave_of_the_hand_does_not_trigger(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.WAVE_OF_THE_HAND: 3}, targets=2)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 0, enemy_index=0)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 0, enemy_index=1)
        self.see_player_has_power(play, PowerId.WAVE_OF_THE_HAND, 0)

    def test_wave_of_the_hand_weak_from_block_return(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.WAVE_OF_THE_HAND: 1})
        state.monsters[0].powers[PowerId.BLOCK_RETURN] = 3
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_enemy_has_power(play, PowerId.WEAKENED, 2)

    def test_free_attack_power(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.FREE_ATTACK_POWER: 1})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_power(play, PowerId.FREE_ATTACK_POWER, 0)

    def test_free_attack_power_with_whirlwind(self):
        state = self.given_state(CardId.WHIRLWIND, player_powers={PowerId.FREE_ATTACK_POWER: 2})
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 25)
        self.see_player_spent_energy(play, 0)
        self.see_player_has_power(play, PowerId.FREE_ATTACK_POWER, 1)

    def test_block_return(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers = {PowerId.BLOCK_RETURN: 2}
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 10)
        self.see_player_spent_energy(play, 1)
        self.see_player_has_block(play, 4)

    def test_block_return_multi_target(self):
        state = self.given_state(CardId.WHIRLWIND, targets=2)
        state.monsters[0].powers = {PowerId.BLOCK_RETURN: 2}
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 25)
        self.see_player_spent_energy(play, 5)
        self.see_player_has_block(play, 10)

    def test_foresight_scrys_at_beginning_of_turn(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.FORESIGHT: 3})
        state.is_new_turn()
        play = self.when_playing_the_first_card(state)
        self.see_player_scryed(play, 3)

    def test_nirvana_blocks_on_scry(self):
        state = self.given_state(CardId.CUT_THROUGH_FATE, player_powers={PowerId.NIRVANA: 5})
        play = self.when_playing_the_first_card(state)
        self.see_player_scryed(play, 2)
        self.see_player_has_block(play, 5)

    def test_omega_deals_damage(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.OMEGA: 50}, targets=2)
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 50, enemy_index=0)
        self.see_enemy_lost_hp(play, 50, enemy_index=1)

    def test_fading_counter_goes_down(self):
        state = self.given_state(CardId.DEFEND_R)
        state.monsters[0].powers[PowerId.FADING] = 5
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 0)
        self.see_enemy_has_power(play, PowerId.FADING, 4)

    def test_fading_kills_enemy(self):
        state = self.given_state(CardId.DEFEND_R)
        state.monsters[0].powers[PowerId.FADING] = 1
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_lost_hp(play, 100)
        self.see_enemy_has_power(play, PowerId.FADING, 0)

    def test_killing_enemy_with_stasis_grants_card(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.STASIS] = -1
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_enemy_does_not_have_power(play, PowerId.STASIS)
        self.assertEqual(1, play.state.draw_pay)

    def test_killing_enemy_with_spore_cloud_grants_vulnerable(self):
        amount = 3
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.SPORE_CLOUD] = amount
        state.monsters[0].current_hp = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_hp_is(play, 0)
        self.see_player_has_power(play, PowerId.VULNERABLE, amount)

    def test_slow_not_incremented_when_not_present(self):
        state = self.given_state(CardId.STRIKE_R)
        play = self.when_playing_the_first_card(state)
        self.see_enemy_does_not_have_power(play, PowerId.SLOW)

    def test_slow_incremented_by_card_plays(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.DEFEND_R))
        state.hand.append(get_card(CardId.INFLAME))
        state.monsters[0].powers[PowerId.SLOW] = 0
        play = self.when_making_the_most_plays(state)
        self.see_enemy_has_power(play, PowerId.SLOW, 3)

    def test_slow_increases_damage_taken_by_attack_cards(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.SLOW] = 5
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 9)
        self.see_enemy_has_power(play, PowerId.SLOW, 6)

    def test_slow_plays_nicely_with_pen_nib(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.PEN_NIB: 9})
        state.monsters[0].powers[PowerId.SLOW] = 5
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 18)
        self.see_enemy_has_power(play, PowerId.SLOW, 6)

    def test_strength_applies_before_other_bonuses_like_pen_nib(self):
        state = self.given_state(CardId.STRIKE_R, relics={RelicId.PEN_NIB: 9}, player_powers={PowerId.STRENGTH: 1})
        play = self.when_making_the_most_plays(state)
        self.see_enemy_lost_hp(play, 14)

    def test_barricade_prevents_monster_block_from_disappearing(self):
        state = self.given_state(CardId.WOUND)
        state.monsters[0].block = 3
        state.monsters[0].powers = {PowerId.BARRICADE: 1}
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_enemy_block_is(play, 3)

    def test_barricade_prevents_player_block_from_disappearing(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.BARRICADE: 1})
        state.player.block = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 3)
        self.assertEqual(3, play.state.saved_block_for_next_turn)

    def test_barricade_saves_block_even_though_calipers_wants_to_take_some(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.BARRICADE: 1}, relics={RelicId.CALIPERS: 1})
        state.player.block = 20
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 20)
        self.assertEqual(20, play.state.saved_block_for_next_turn)

    def test_blur_prevents_player_block_from_disappearing(self):
        state = self.given_state(CardId.WOUND, player_powers={PowerId.BLUR: 1})
        state.player.block = 3
        play = self.when_playing_the_first_card(state)
        play.end_turn()
        self.see_player_has_block(play, 3)
        self.assertEqual(3, play.state.saved_block_for_next_turn)

    def test_fake_dexterity_temp_adds_to_block(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.FAKE_DEXTERITY_TEMP: 3})
        play = self.when_playing_the_first_card(state)
        self.see_player_has_block(play, 8)

    def test_beat_of_death_damages_when_playing_cards(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.monsters[0].powers[PowerId.BEAT_OF_DEATH] = 3
        play = self.when_playing_the_whole_hand(state)
        self.see_player_lost_hp(play, 6)

    def test_invincible_decreases_when_damage_taken(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.INVINCIBLE] = 12
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_has_power(play, PowerId.INVINCIBLE, 6)

    def test_invincible_caps_damage_taken(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.INVINCIBLE] = 5
        play = self.when_playing_the_first_card(state)
        self.see_enemy_has_power(play, PowerId.INVINCIBLE, 0)
        self.see_enemy_lost_hp(play, 5)

    def test_invincible_caps_healing_from_damage(self):
        state = self.given_state(CardId.REAPER)
        state.monsters[0].powers[PowerId.INVINCIBLE] = 2
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 2)
        self.see_player_lost_hp(play, -2)
        self.see_enemy_has_power(play, PowerId.INVINCIBLE, 0)

    def test_invincible_blocks_damage_even_when_it_is_already_at_0(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.INVINCIBLE] = 0
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_enemy_has_power(play, PowerId.INVINCIBLE, 0)

    def test_back_attack_deals_more_damage(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].damage = 10
        state.monsters[0].hits = 1
        state.monsters[0].powers[PowerId.BACK_ATTACK] = -1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 15)

    def test_back_attack_combos_with_strength_correctly(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].damage = 12
        state.monsters[0].hits = 1
        state.monsters[0].powers[PowerId.BACK_ATTACK] = -1
        state.monsters[0].powers[PowerId.STRENGTH] = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_player_lost_hp(play, 19)

    # Back Attack doesn't currently correctly get updated in the game when we attack a different monster.
    # So commenting it out for now @todo
    # def test_back_attack_moves_depending_on_target(self):
    #     state = self.given_state(CardId.STRIKE_R, targets=2, player_powers={PowerId.SURROUNDED: -1})
    #     state.monsters[0].powers[PowerId.BACK_ATTACK] = -1
    #     play = self.when_playing_the_first_card(state)
    #     self.see_enemy_lost_hp(play, 6, 0)
    #     self.see_enemy_has_power(play, PowerId.BACK_ATTACK, 0, 0)
    #     self.see_enemy_has_power(play, PowerId.BACK_ATTACK, -1, 1)

    def test_back_attack_does_not_move_if_targeting_same(self):
        state = self.given_state(CardId.STRIKE_R, targets=2, player_powers={PowerId.SURROUNDED: 1})
        state.monsters[1].powers[PowerId.BACK_ATTACK] = -1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 6, 0)
        self.see_enemy_has_power(play, PowerId.BACK_ATTACK, 0, 0)
        self.see_enemy_has_power(play, PowerId.BACK_ATTACK, -1, 1)

    def test_back_attack_disappears_if_only_1_target(self):
        state = self.given_state(CardId.STRIKE_R, targets=2, player_powers={PowerId.SURROUNDED: -1})
        state.monsters[0].current_hp = 1
        state.monsters[1].powers[PowerId.BACK_ATTACK] = -1
        play = self.when_playing_the_first_card(state)
        self.see_enemy_lost_hp(play, 100, 0)
        self.see_player_has_power(play, PowerId.SURROUNDED, 0)
        self.see_enemy_has_power(play, PowerId.BACK_ATTACK, 0, 0)
        self.see_enemy_has_power(play, PowerId.BACK_ATTACK, 0, 1)

    def test_back_attack_disappears_if_a_monster_dies_during_their_turn(self):
        state = self.given_state(CardId.WOUND, targets=2, player_powers={PowerId.SURROUNDED: -1, PowerId.THORNS: 1})
        state.monsters[0].current_hp = 1
        state.monsters[0].damage = 0
        state.monsters[0].hits = 1
        state.monsters[1].powers[PowerId.BACK_ATTACK] = -1
        state.monsters[1].damage = 2
        state.monsters[1].hits = 1
        play = self.when_playing_the_first_card(state)
        play.state.end_turn()
        self.see_enemy_lost_hp(play, 100, 0)
        self.see_player_lost_hp(play, 2)
        self.see_player_has_power(play, PowerId.SURROUNDED, 0)
        self.see_enemy_has_power(play, PowerId.BACK_ATTACK, 0, 0)
        self.see_enemy_has_power(play, PowerId.BACK_ATTACK, 0, 1)
