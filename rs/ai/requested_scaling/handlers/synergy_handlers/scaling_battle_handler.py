from typing import List

from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_calculator import getSynergy
from rs.calculator.synergies.synergy_providers import synergyProviderCardIdStrings
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class ScalingBattleHandler(Handler):
    def can_handle(self, state: GameState) -> bool:
        if not state.has_command(Command.PLAY):
            return False
        scaling_cards = self.get_scaling_cards(state)
        return len(scaling_cards) > 0

    def get_scaling_cards(self, state: GameState) -> List[str]:
        scaling_cards = []
        stuff = synergyProviderCardIdStrings()
        allowed_stuff = [e.value for e in CardId]

        for card in state.hand.cards:
            if card.id.lower() in stuff and card.id.lower() in allowed_stuff:
                scaling_cards.append(card.id.lower())
        return scaling_cards

    def get_synergy_cards_in_hand(self, state: GameState) -> (List[str]):
        synergy_deck = state.hand.cards + state.draw_pile.cards + state.discard_pile.cards
        allowed_stuff = [e.value for e in CardId]
        allowed_synergy_deck = []
        for card in synergy_deck:
            if card.id.lower() in allowed_stuff:
                allowed_synergy_deck.append(card)
        scaling_cards = self.get_scaling_cards(state)
        synergies: [str, float] = {}
        for scaler_as_string in scaling_cards:
            synergies[scaler_as_string] = getSynergy(CardId(scaler_as_string), [CardId(c.id.lower())
                                                                                for c in allowed_synergy_deck])
        # Remember to sort this so the highest synergy is the one we take in the end.
        synergies_to_play = sorted([key for key in synergies.keys() if synergies[key] >= 0.2],
                                   key=lambda x: synergies[x], reverse=True)
        return synergies_to_play

    def get_target(self, monsters: List[dict]) -> int:
        highest_health = None
        target = -1
        for i, m in enumerate(monsters):
            effective_health = m['current_hp'] + m['block']
            if (highest_health is None or effective_health < highest_health) and not m['is_gone']:
                highest_health = effective_health
                target = i
        return target

    def get_incoming_effective_damage(self, monsters: List[dict], block: int):
        damage = 0
        for m in monsters:
            if not m['is_gone'] and 'move_adjusted_damage' in m:
                base_damage = m['move_adjusted_damage']
                if base_damage == -1:
                    base_damage = m['move_base_damage']
                if base_damage == -1:
                    base_damage = 0
                damage += base_damage * m['move_hits']
        return damage - block

    def get_player_current_hp(self, state: GameState) -> float:
        return state.game_state()["current_hp"]

    def handle(self, state: GameState) -> List[str]:
        energy_remaining = state.get_player_combat()['energy']

        """Measuring current threat level"""
        incoming_effective_damage = self.get_incoming_effective_damage(state.get_monsters(), state.get_player_block())
        current_hp = self.get_player_current_hp(state)
        if incoming_effective_damage / current_hp > 0.4:
            return []  # Let next handler handle

        """Determine target (the lowest effective hp) in case target is needed"""
        target_index = self.get_target(state.get_monsters())
        if target_index == -1:
            return []

        synergy_card_ids: List[str] = self.get_synergy_cards_in_hand(state)
        if not synergy_card_ids:
            return []  # Let next handler handle

        card_id_to_play = synergy_card_ids[0]
        energy_remaining = state.get_player_combat()['energy']

        specific = 'not specific'

        specific, specific_index = self.handle_specific_scaling_cards(state, card_id_to_play)
        if specific == 'ok':
            target_index = specific_index

        if specific == 'not ok':
            return []

        # this doesn't take into account upgraded cards, so you'd want to prefer that. Probably :D
        index_to_play = [c.id.lower() for c in state.hand.cards].index(card_id_to_play)

        command = "play " + str(index_to_play + 1)

        # Have to make sure we have enough energy to play the card, or else...
        if state.hand.cards[index_to_play].cost <= energy_remaining:
            if state.hand.cards[index_to_play].has_target:
                command += " " + str(target_index)

        else:
            return []

        return [command]

    def handle_specific_scaling_cards(self, state: GameState, card_id_to_play):
        index = 0
        card = card_id_to_play.lower()
        if card == 'limit break':
            current_power_list = state.get_player_combat()['powers']
            if len(current_power_list) == 0:
                return "not ok", index

            for power in current_power_list:
                power_id_as_a_string = power['id'].lower()
                if power_id_as_a_string == 'strength':
                    total_strength = power['amount']
                    if total_strength > 0:
                        return "ok", index
                    else:
                        return "not ok", index
                else:
                    return "not ok", index

        elif card == 'spot weakness':
            monster_list = state.game_state()['combat_state']['monsters']
            for i, monster in enumerate(monster_list):
                specific_index = i
                is_dead = monster['is_gone']
                intent = monster['intent']
                if not is_dead:
                    enemy_not_dead = True
                    if "ATTACK" in intent:
                        return "ok", specific_index
                    else:
                        continue
                else:
                    continue

            return "not ok", index

        else:
            return "not specific", index
