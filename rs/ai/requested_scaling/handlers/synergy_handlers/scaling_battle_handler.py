from typing import List

from rs.calculator.cards import CardId
from rs.calculator.synergies.synergy_calculator import getSynergy
from rs.calculator.synergies.synergy_providers import SynergyProviders, synergyProviderCardIdStrings
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
        for card in state.hand.cards:
            if card.id.lower() in stuff:
                scaling_cards.append(card.id.lower())
        return scaling_cards

    def get_synergy_cards_in_hand(self, state: GameState) -> (List[str]):
        synergy_deck = state.hand.cards + state.draw_pile.cards + state.discard_pile.cards
        scaling_cards = self.get_scaling_cards(state)
        synergies: [str, float] = {}
        for scaler_as_string in scaling_cards:
            synergies[scaler_as_string] = getSynergy(CardId(scaler_as_string), [CardId(c.id.lower()) for c in synergy_deck])
        # Remember to sort this so the highest synergy is the one we take in the end.
        synergies_to_play = [key for key in synergies.keys() if synergies[key] >= 0.3]
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

    def handle(self, state: GameState) -> List[str]:
        energy_remaining = state.get_player_combat()['energy']

        # Determine target (the lowest effective hp) in case target is needed. We need to modify this
        target_index = self.get_target(state.get_monsters())
        if target_index == -1:
            return 0

        synergy_card_ids: List[str] = self.get_synergy_cards_in_hand(state)
        if not synergy_card_ids:
            return None

        card_id_to_play = synergy_card_ids[0]
        # this doesn't take into account upgraded cards, so you'd want to prefer that. Probably :D
        index_to_play = [c.id.lower() for c in state.hand.cards].index(card_id_to_play)

        command = "play " + str(index_to_play + 1)
        if state.hand.cards[index_to_play].has_target:
            command += " " + str(target_index)
        return [command]
