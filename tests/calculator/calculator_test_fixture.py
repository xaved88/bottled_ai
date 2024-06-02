import unittest
from typing import List, Tuple

from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.battle_state import BattleState
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.memory_items import StanceType, MemoryItem
from rs.calculator.interfaces.potions import Potions
from rs.calculator.play_path import PlayPath, get_paths
from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.relics import Relics
from rs.calculator.player import Player
from rs.calculator.monster import Monster
from rs.machine.the_bots_memory_book import TheBotsMemoryBook


class CalculatorTestFixture(unittest.TestCase):

    def given_state(self, card_id: CardId, upgrade: int = 0, targets: int = 1, player_powers=None,
                    relics: Relics = None, potions: Potions = None, cards_discarded_this_turn: int = 0, amount_to_discard: int = 0,
                    orbs: List[Tuple[OrbId, int]] = None, orb_slots: int = 0,
                    memory_book: TheBotsMemoryBook = None) -> BattleState:

        if memory_book is None:
            memory_book = TheBotsMemoryBook.new_default()

        return BattleState(
            player=Player(True, 50, 100, 0, {} if player_powers is None else player_powers, energy=5, relics=relics, potions=potions),
            hand=[get_card(card_id, None, upgrade)],
            monsters=[Monster(False, 100, 100, 0, {}) for i in range(targets)],
            relics=relics,
            potions=potions,
            cards_discarded_this_turn=cards_discarded_this_turn,
            amount_to_discard=amount_to_discard,
            orbs=orbs,
            orb_slots=orb_slots,
            memory_by_card=memory_book.memory_by_card.copy(),
            memory_general=memory_book.memory_general.copy(),
        )

    def when_playing_the_first_card(self, hand_state: BattleState) -> PlayPath:
        paths = {}
        get_paths(PlayPath([], hand_state), paths)
        plays = list(paths.values())
        if len(plays) > 1:
            return plays[1]
        else:
            return plays[0]

    def when_playing_the_whole_hand(self, hand_state: BattleState) -> PlayPath:
        paths = {}
        get_paths(PlayPath([], hand_state), paths)
        return list(paths.values())[-1]

    def when_making_the_most_plays(self, hand_state: BattleState) -> PlayPath:
        paths = self.when_getting_all_paths(hand_state)
        largest = max(paths, key=lambda path: len(path.plays))
        return largest

    def when_getting_all_paths(self, hand_state: BattleState) -> list[PlayPath]:
        paths = {}
        get_paths(PlayPath([], hand_state), paths)
        return list(paths.values())

    def see_enemy_lost_hp(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, 100 - play.state.monsters[enemy_index].current_hp)

    def see_enemy_hp_is(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.monsters[enemy_index].current_hp)

    def see_enemy_block_is(self, play: PlayPath, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.monsters[enemy_index].block)

    def see_enemy_has_power(self, play: PlayPath, power_id: PowerId, amount: int, enemy_index: int = 0):
        self.assertEqual(amount, play.state.monsters[enemy_index].powers.get(power_id, 0))

    def see_enemy_does_not_have_power(self, play: PlayPath, power_id: PowerId, enemy_index: int = 0):
        self.assertEqual(None, play.state.monsters[enemy_index].powers.get(power_id, None))

    def see_random_damage_dealt(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.total_random_damage_dealt)

    def see_player_lost_hp(self, play: PlayPath, amount: int):
        self.assertEqual(amount, 50 - play.state.player.current_hp)

    def see_player_spent_energy(self, play: PlayPath, amount: int):
        self.assertEqual(amount, 5 - play.state.player.energy)

    def see_player_has_energy(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.player.energy)

    def see_player_has_block(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.player.block)

    def see_player_has_power(self, play: PlayPath, power_id: PowerId, amount: int):
        self.assertEqual(amount, play.state.player.powers.get(power_id, 0))

    def see_cards_played(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.plays))

    def see_player_discard_pile_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.discard_pile))

    def see_player_draw_pile_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.draw_pile))

    def see_player_exhaust_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.exhaust_pile))

    def see_player_hand_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.hand))

    def see_player_drew_cards(self, play: PlayPath, amount: int):
        actual = len([1 for c in play.state.hand if " draw" in c.id.value])
        self.assertEqual(amount, actual)

    def see_player_scryed(self, play: PlayPath, amount: int):
        actual = len([1 for c in play.state.hand if "draw " in c.id.value])
        self.assertEqual(amount, play.state.amount_scryed)

    def see_player_does_not_have_power(self, play: PlayPath, power_id: PowerId):
        self.assertEqual(None, play.state.player.powers.get(power_id))

    def see_hand_card_is(self, play: PlayPath, card_id: CardId, index: int = 0):
        self.assertEqual(card_id, play.state.hand[index].id)

    def see_hand_card_upgrade(self, play: PlayPath, upgrade: int, index: int = 0):
        self.assertEqual(upgrade, play.state.hand[index].upgrade)

    def see_hand_card_cost(self, play: PlayPath, cost: int, index: int = 0):
        self.assertEqual(cost, play.state.hand[index].cost)

    def see_orb_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.orbs))

    def see_orb_type_count(self, play: PlayPath, amount: int, orb_id: OrbId):
        orbs = [o for (o, a) in play.state.orbs if o == orb_id]
        self.assertEqual(amount, len(orbs))

    def see_orb_slots_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, play.state.orb_slots)

    def see_relic_value(self, play: PlayPath, relic_id: RelicId, value: int):
        self.assertEqual(value, play.state.relics.get(relic_id))

    def see_stance(self, play: PlayPath, expected_stance: StanceType):
        self.assertEqual(expected_stance, play.state.get_memory_value(MemoryItem.STANCE))

    def see_potion_count(self, play: PlayPath, amount: int):
        self.assertEqual(amount, len(play.state.potions))

    def see_potions(self, play: PlayPath, potion_ids: dict):
        self.assertEqual(potion_ids, play.state.potions)
