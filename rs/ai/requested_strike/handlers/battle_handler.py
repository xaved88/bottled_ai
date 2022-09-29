import math
from typing import List

from rs.game.card import Card, CardType
from rs.game.deck import Deck
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


# https://alexdriedger.github.io/SlayTheSpireModding/docs/id-cards

class BattleHandler(Handler):

    def __init__(self):
        self.always: List[str] = [
            'offering',
            'battle trance',
            'seeing red',
            'bloodletting',
            'apotheosis',
            'ghostly',
            'shockwave',
        ]

        self.attack_preferences: List[str] = [
            'bash',
            'thunderclap',
            'perfected strike',
            'reaper',
            'bludgeon',
            'pommel strike',
            'twin strike',
        ]

        self.attack_shuns: List[str] = [
            'strike_r'
        ]

        self.defend_preferences: List[str] = [
            'impervious',
            'flame barrier',
            'shrug it off',
            'true grit',
            'defend_r',
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY)

    def handle(self, state: GameState) -> List[str]:
        # Determine target (lowest effective hp)
        target_index = self.get_target_from_monster_list(state.get_monsters())
        target = state.get_monsters()[target_index]

        # Get damage in hand, enemy damage, and knowledge of if we can kill the target
        damage = self.get_damage_in_hand(state.hand, state, state.get_player_combat(), target)
        incoming_damage = self.get_incoming_damage(state.get_monsters())
        can_kill = damage >= (target['current_hp'] + target['block'])

        # If damage can kill, attack mode.
        # If incoming damage >= 10, defend mode.
        mode = 'attack' if can_kill or incoming_damage < 10 else 'defend'

        # Play always preferred cards
        energy_remaining = state.get_player_combat()['energy']
        (energy_remaining, plays) = self.get_plays_from_list(self.always, energy_remaining, state)

        # Play prioritized defensive cards only if in defensive mode
        if mode == 'defend':
            (energy_remaining, add_plays) = self.get_plays_from_list(self.defend_preferences, energy_remaining, state)
            plays += add_plays

        if not state.player_entangled():
            # Play preferred attacks
            (energy_remaining, add_plays) = self.get_plays_from_list(self.attack_preferences, energy_remaining, state)
            plays += add_plays

            # Play neutral attacks
            for i, cih in enumerate(state.hand.cards):
                if i not in plays \
                        and cih.type == CardType.ATTACK \
                        and cih.id.lower() not in self.attack_shuns \
                        and energy_remaining >= cih.cost\
                        and cih.is_playable:
                    energy_remaining -= cih.cost
                    plays.append(i)

            # Play shunned attacks
            (energy_remaining, add_plays) = self.get_plays_from_list(self.attack_shuns, energy_remaining, state)
            plays += add_plays

        # Play deprioritized def cards only if in attack mode
        if mode == 'attack':
            (energy_remaining, add_plays) = self.get_plays_from_list(self.defend_preferences, energy_remaining, state)
            plays += add_plays

        # Play any non-played non-attack cards
        for i, cih in enumerate(state.hand.cards):
            if i not in plays and energy_remaining >= cih.cost and cih.type != CardType.ATTACK and cih.is_playable:
                energy_remaining -= cih.cost
                plays.append(i)

        if plays:
            command = "play " + str(plays[0] + 1)
            if state.hand.cards[plays[0]].has_target:
                command += " " + str(target_index)
            return [command]
        return ["end"]

    def get_target_from_monster_list(self, monsters: List[dict]) -> int:
        max_health = 999
        target = 0
        for i, m in enumerate(monsters):
            health = m['current_hp'] + m['block']
            if health < max_health and not m['is_gone']:
                max_health = health
                target = i
        return target

    def get_damage_in_hand(self, hand: Deck, state: GameState, player: dict, target: dict, ) -> int:
        vulnerable = bool(next((power for power in target['powers'] if power['id'] == 'Vulnerable'), None))
        weak = bool(next((power for power in player['powers'] if power['id'] == 'Weak'), None))

        attacks = self.attack_preferences + self.attack_shuns

        energy_remaining = player['energy']
        damage = 0
        for attack in attacks:
            attacks_in_hand = list(filter(lambda card: attack in card.id.lower(), hand.cards))
            for aih in attacks_in_hand:
                if energy_remaining >= aih.cost:
                    energy_remaining -= aih.cost
                    damage += self.get_card_damage(aih, state, vulnerable, weak)
        return damage

    def get_card_damage(self, card: Card, state: GameState, vulnerable: bool, weak: bool):
        base = [0]
        name = card.id.lower()
        if name == 'bash':
            base = [10] if card.upgrades else [8]
        if name == 'thunderclap':
            base = [7] if card.upgrades else [4]
        if name == 'perfected strike':
            strike_count = len(list(filter(lambda strike: "strike" in strike.name.lower(), state.deck.cards)))
            base = [6 + 3 * strike_count] if card.upgrades else [6 + 2 * strike_count]
        if name == 'reaper':
            base = [5] if card.upgrades else [4]
        if name == 'bludgeon':
            base = [42] if card.upgrades else [32]
        if name == 'pommel strike':
            base = [10] if card.upgrades else [9]
        if name == 'twin strike':
            base = [7, 7] if card.upgrades else [5, 5]
        if name == 'strike_r':
            base = [9] if card.upgrades else [6]

        if weak:
            for i, v in enumerate(base):
                base[i] = math.floor(v * 0.75)
        if vulnerable:
            for i, v in enumerate(base):
                base[i] = math.floor(v * 1.5)

        return sum(base)

    def get_incoming_damage(self, monsters: List[dict]):
        damage = 0
        for m in monsters:
            if not m['is_gone']:
                damage += m['move_adjusted_damage'] * m['move_hits']
        return damage

    def get_plays_from_list(self, card_list: List[str], energy_remaining: int, state: GameState) -> (int, List[int]):
        plays = []
        for card in card_list:
            for i, cih in enumerate(state.hand.cards):
                if card == cih.id.lower() and energy_remaining >= cih.cost and cih.is_playable:
                    energy_remaining -= cih.cost
                    plays.append(i)
        return energy_remaining, plays
