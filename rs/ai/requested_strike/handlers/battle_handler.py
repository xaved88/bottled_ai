import math
from typing import List

from rs.game.card import Card, CardType
from rs.game.deck import Deck
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState, get_stacks_of_power


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
        self.always_1v: List[str] = [
            'offering',
            'battle trance',
            'seeing red',
            'bloodletting',
            'apotheosis',
            'ghostly',
        ]
        self.always_3v: List[str] = self.always_1v

        self.attack_preferences: List[str] = [
            'bash',
            'thunderclap',
            'perfected strike',
            'reaper',
            'bludgeon',
            'pommel strike',
            'twin strike',
        ]
        self.attack_preferences_1v: List[str] = [
            'perfected strike',
            'bash',
            'thunderclap',
            'reaper',
            'bludgeon',
            'pommel strike',
            'twin strike',
        ]
        self.attack_preferences_3v: List[str] = [
            'perfected strike',
            'reaper',
            'bludgeon',
            'pommel strike',
            'twin strike',
        ]

        self.attack_shuns: List[str] = [
            'strike_r'
        ]
        self.attack_shuns_1v: List[str] = [
            'strike_r'
        ]
        self.attack_shuns_3v: List[str] = [
            'bludgeon',
            'thunderclap'
        ]

        self.defend_preferences: List[str] = [
            'impervious',
            'flame barrier',
            'shrug it off',
            'true grit',
            'defend_r',
        ]
        self.defend_preferences_1v: List[str] = [
            'shockwave'
            'impervious',
            'flame barrier',
            'shrug it off',
            'true grit',
            'defend_r',
        ]
        self.defend_preferences_3v: List[str] = [
            'impervious',
            'flame barrier',
            'shrug it off',
            'true grit',
            'defend_r',
            'shockwave'
        ]

    def can_handle(self, state: GameState) -> bool:
        return state.has_command(Command.PLAY)

    def handle(self, state: GameState) -> List[str]:
        # Determine target (lowest effective hp)
        target_index = self.get_target_from_monster_list(state.get_monsters())
        target = state.get_monsters()[target_index]

        # Get damage in hand, enemy damage, and knowledge of if we can kill the target
        vulnerable_count = get_stacks_of_power(target['powers'], "Vulnerable")
        damage = self.get_damage_in_hand(state.hand, state, state.get_player_combat(), target)
        incoming_damage = self.get_incoming_damage(state.get_monsters())
        can_kill = damage >= (target['current_hp'] + target['block'])

        # If damage can kill, attack mode.
        # If incoming damage >= 10, defend mode.
        mode = 'attack' if can_kill or incoming_damage < 10 else 'defend'

        always_priorities = self.get_always_priorities(vulnerable_count)
        defend_priorities = self.get_defend_priorities(vulnerable_count)
        attack_priorities = self.get_attack_priorities(vulnerable_count)
        shuns = self.get_attack_shuns(vulnerable_count)
        # Play always preferred cards
        energy_remaining = state.get_player_combat()['energy']
        (energy_remaining, plays) = self.get_plays_from_list(always_priorities, energy_remaining, state)

        # Play prioritized defensive cards only if in defensive mode
        if mode == 'defend':
            (energy_remaining, add_plays) = self.get_plays_from_list(defend_priorities, energy_remaining, state)
            plays += add_plays

        if not state.player_entangled():
            # Play preferred attacks
            (energy_remaining, add_plays) = self.get_plays_from_list(attack_priorities, energy_remaining, state)
            plays += add_plays

            # Play neutral attacks
            for i, cih in enumerate(state.hand.cards):
                if i not in plays \
                        and cih.type == CardType.ATTACK \
                        and cih.id.lower() not in shuns \
                        and energy_remaining >= cih.cost \
                        and cih.is_playable:
                    energy_remaining -= cih.cost
                    plays.append(i)

            # Play shunned attacks
            (energy_remaining, add_plays) = self.get_plays_from_list(shuns, energy_remaining, state)
            plays += add_plays

        # Play deprioritized def cards only if in attack mode
        if mode == 'attack':
            (energy_remaining, add_plays) = self.get_plays_from_list(defend_priorities, energy_remaining, state)
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
        highest_health = 999
        target = 0
        for i, m in enumerate(monsters):
            effective_health = m['current_hp'] + m['block']
            if effective_health < highest_health and not m['is_gone']:
                highest_health = effective_health
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
                base_damage = m['move_adjusted_damage']
                if base_damage == -1:
                    base_damage = m['move_base_damage']
                if base_damage == -1:
                    base_damage = 0
                damage += base_damage * m['move_hits']
        return damage

    def get_plays_from_list(self, card_list: List[str], energy_remaining: int, state: GameState) -> (int, List[int]):
        plays = []
        for card in card_list:
            for i, cih in enumerate(state.hand.cards):
                if card == cih.id.lower() and energy_remaining >= cih.cost and cih.is_playable:
                    energy_remaining -= cih.cost
                    plays.append(i)
        return energy_remaining, plays

    def get_always_priorities(self, vulnerable: int) -> List[str]:
        if vulnerable < 1:
            return self.always
        elif vulnerable < 3:
            return self.always_1v
        return self.always_3v

    def get_attack_priorities(self, vulnerable: int) -> List[str]:
        if vulnerable < 1:
            return self.attack_preferences
        elif vulnerable < 3:
            return self.attack_preferences_1v
        return self.attack_preferences_3v

    def get_attack_shuns(self, vulnerable: int) -> List[str]:
        if vulnerable < 1:
            return self.attack_shuns
        elif vulnerable < 3:
            return self.attack_shuns_1v
        return self.attack_shuns_3v

    def get_defend_priorities(self, vulnerable: int) -> List[str]:
        if vulnerable < 1:
            return self.defend_preferences
        elif vulnerable < 3:
            return self.defend_preferences_1v
        return self.defend_preferences_3v
