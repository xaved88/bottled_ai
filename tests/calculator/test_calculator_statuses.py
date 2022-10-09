from calculator.calculator_test_fixture import CalculatorTestFixture
from rs.calculator.cards import CardId, get_card
from rs.calculator.powers import PowerId


class CalculatorCardsTest(CalculatorTestFixture):

    def test_correct_statuses_lose_stacks_after_turn_end(self):
        pass

    def test_strength_adds_to_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STRENGTH: 4})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 10)

    def test_strength_adds_to_multi_attack(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.STRENGTH: 3})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 16)

    def test_strength_when_negative(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STRENGTH: -1})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 5)

    def test_strength_when_damage_below_zero(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.STRENGTH: -100})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 0)
        self.see_cards_played(play, 1)

    def test_strength_does_not_add_to_self_damage(self):
        state = self.given_state(CardId.BLOODLETTING, player_powers={PowerId.STRENGTH: 3})
        play = self.when_calculating_state_play(state)
        self.see_player_lost_hp(play, 3)

    def test_dexterity_adds_to_block(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.DEXTERITY: 3})
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 8)

    def test_dexterity_when_negative(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.DEXTERITY: -3})
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 2)

    def test_dexterity_when_block_would_be_below_zero(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.DEXTERITY: -13})
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 0)
        self.see_cards_played(play, 1)

    def test_vulnerable_when_attacking(self):
        state = self.given_state(CardId.STRIKE_R)
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 9)

    def test_vulnerable_with_multi_attack_when_attacking(self):
        state = self.given_state(CardId.TWIN_STRIKE)
        state.monsters[0].powers[PowerId.VULNERABLE] = 1
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 14)

    def test_vulnerable_when_defending(self):
        pass

    def test_vulnerable_with_multi_attack_when_defending(self):
        pass

    def test_weak_when_attacking(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.WEAK: 1})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 4)

    def test_weak_with_multi_attack_when_attacking(self):
        state = self.given_state(CardId.TWIN_STRIKE, player_powers={PowerId.WEAK: 1})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 6)

    def test_weak_when_defending(self):
        pass

    def test_weak_with_multi_attack_when_defending(self):
        pass

    def test_frail(self):
        state = self.given_state(CardId.DEFEND_R, player_powers={PowerId.FRAIL: 1})
        play = self.when_calculating_state_play(state)
        self.see_player_gained_block(play, 3)

    def test_entangled_no_attacks_played(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.ENTANGLED: 1})
        play = self.when_calculating_state_play(state)
        self.see_cards_played(play, 0)

    def test_vigor(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.VIGOR: 8})
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 14)
        self.player_does_not_have_power(play, PowerId.VIGOR)

    def test_curl_up(self):
        state = self.given_state(CardId.STRIKE_R)
        state.hand.append(get_card(CardId.STRIKE_R))
        state.monsters[0].powers[PowerId.CURL_UP] = 8
        play = self.when_calculating_state_play(state)
        self.see_cards_played(play, 2)
        self.see_enemy_lost_hp(play, 6)
        self.see_enemy_block_is(play, 2)

    def test_artifact_blocks_debuff(self):
        state = self.given_state(CardId.BASH)
        state.monsters[0].powers[PowerId.ARTIFACT] = 1
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 8)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 0)
        self.see_enemy_has_status(play, PowerId.ARTIFACT, 0)

    def test_artifact_does_not_block_buff(self):
        pass

    def test_artifact_multiple_debuffs(self):
        state = self.given_state(CardId.UPPERCUT)
        state.monsters[0].powers[PowerId.ARTIFACT] = 1
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 1)
        self.see_enemy_has_status(play, PowerId.WEAK, 0)
        self.see_enemy_has_status(play, PowerId.ARTIFACT, 0)

    def test_artifact_multiple_stacks(self):
        state = self.given_state(CardId.UPPERCUT)
        state.monsters[0].powers[PowerId.ARTIFACT] = 3
        play = self.when_calculating_state_play(state)
        self.see_enemy_lost_hp(play, 13)
        self.see_enemy_has_status(play, PowerId.VULNERABLE, 0)
        self.see_enemy_has_status(play, PowerId.WEAK, 0)
        self.see_enemy_has_status(play, PowerId.ARTIFACT, 1)

    def test_plated_armor_adds_block(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.PLATED_ARMOR: 4})
        play = self.when_calculating_state_play(state)
        play.end_turn()
        self.see_player_gained_block(play, 4)

    def test_plated_armor_gets_reduced_by_damage(self):
        state = self.given_state(CardId.STRIKE_R, player_powers={PowerId.PLATED_ARMOR: 4})
        state.player.block = 0
        state.monsters[0].damage = 5
        state.monsters[0].hits = 2
        play = self.when_calculating_state_play(state)
        play.end_turn()
        self.see_player_lost_hp(play, 6)
        self.see_player_has_status(play, PowerId.PLATED_ARMOR, 2)
