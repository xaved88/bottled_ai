from typing import List

from rs.calculator.cards import CardId
from rs.ai.requested_scaling.synergies.synergy_calculator import get_synergy
from rs.ai.requested_scaling.synergies.synergy_providers import synergyProviderCardIdStrings
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class ScalingBattleHandler(Handler):
    def can_handle(self, state: GameState) -> bool:
        if not state.has_command(Command.PLAY):
            return False
        scaling_cards = self.get_scaling_cards(state)
        return len(scaling_cards) > 0

    def handle(self, state: GameState) -> List[str]:
        energy_remaining = state.get_player_combat()['energy']

        # Measuring current threat level
        incoming_effective_damage = self.get_incoming_effective_damage(state.get_monsters(), state.get_player_block())
        current_hp = self.get_player_current_hp(state)
        if incoming_effective_damage / current_hp > 0.3:
            return []  # Let next handler handle
            # Since this effect will be triggering after every card is played, if enough block is achieved
            # we will continue the scaling plan

        """Determine target (the lowest effective hp) in case target is needed"""
        target_index = self.get_target(state.get_monsters())
        if target_index == -1:
            return []

        synergy_card_ids: List[str] = self.get_synergy_cards_in_hand(state)
        if not synergy_card_ids:
            return []  # Let next handler handle

        card_id_to_play = synergy_card_ids[0]

        # Handler is behaving funny with snecko eye. Playing an inflame for 3 cost if not assuming damage, and so on
        # Need to solve next
        energy_remaining = state.get_player_combat()['energy']

        # check if this card is in the specific list:
        # cards that need specific knowledge to play (like limit break) are in this category
        # if the scaling card that's gonna be played is in this list; then check at the specific conditions.
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

    def get_scaling_cards(self, state: GameState) -> List[str]:
        scaling_cards = []
        synergy_providers_list_as_strings = synergyProviderCardIdStrings()
        allowed_stuff = [e.value for e in CardId]

        for card in state.hand.cards:
            if card.id.lower() in synergy_providers_list_as_strings and card.id.lower() in allowed_stuff:
                scaling_cards.append(card.id.lower())
        return scaling_cards

    def get_synergy_cards_in_hand(self, state: GameState) -> (List[str]):
        synergy_deck = state.hand.cards + state.draw_pile.cards + state.discard_pile.cards
        allowed_cards_in_our_card_pool = [e.value for e in CardId]
        allowed_synergy_deck = []
        for card in synergy_deck:
            if card.id.lower() in allowed_cards_in_our_card_pool:
                allowed_synergy_deck.append(card)
        scaling_cards = self.get_scaling_cards(state)
        synergies: [str, float] = {}
        for scaler_as_string in scaling_cards:
            synergies[scaler_as_string] = get_synergy(CardId(scaler_as_string), [CardId(c.id.lower())
                                                                                for c in allowed_synergy_deck])
        # Sorting and giving out the most synergistic cards first:
        synergies_to_play = sorted([key for key in synergies.keys() if synergies[key] >= 0],
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

    def handle_specific_scaling_cards(self, state: GameState, card_id_to_play):
        index = 0
        card = card_id_to_play.lower()

        if card == 'limit break':
            # Check if there is a strength power active
            current_power_list = state.get_player_combat()['powers']
            if len(current_power_list) == 0:
                return "not ok", index
            for power in current_power_list:
                if power['id'].lower() == 'strength':
                    total_strength = power['amount']
                    if total_strength > 0:
                        return "ok", index
                    else:
                        return "not ok", index
            return "not ok", index

        elif card == 'spot weakness':
            # Check if there is a monster with the 'ATTACK' intent
            monster_list = state.game_state()['combat_state']['monsters']
            for i, monster in enumerate(monster_list):
                if monster['is_gone']:
                    continue
                intent = monster['intent']
                if "ATTACK" in intent:
                    return "ok", i
            return "not ok", index

        else:
            return "not specific", index

