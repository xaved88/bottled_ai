from typing import List

from rs.calculator.synergies.synergy_calculator import getSynergy
from rs.calculator.synergies.synergy_providers import SynergyProviders
from rs.machine.command import Command
from rs.machine.handlers.handler import Handler
from rs.machine.state import GameState


class ScalingBattleHandler(Handler):

    def can_handle(self, state: GameState) -> bool:
        scaling_cards = []
        for card in self.hand:
            if card in SynergyProviders:
                scaling_cards.append(card)

        if state.has_command(Command.PLAY) and len(scaling_cards) > 0:
            return True

    def handle(self, energy_remaining: int, state: GameState, monsters: List[dict]) -> List[str]:

        target_index = self.get_target(self, monsters)
        plays = self.get_plays_from_list(energy_remaining, state)

        if plays:
            command = "play " + str(plays[0] + 1)
            if state.hand.cards[plays[0]].has_target:
                command += " " + str(target_index)
            return [command]

        return ["end"]




    def get_synergy_cards_in_hand(self, state: GameState) -> (List[int]):

        synergy_deck = state.hand.cards + self.state.draw_pile.cards + self.state.discard_pile.cards
        scaling_cards = []
        for card in self.hand:
            if card in SynergyProviders:
                scaling_cards.append(card)

        keys = []
        values = []

        for scaler in scaling_cards:
            keys.append(scaler)

            synergy_meter = getSynergy(scaler, synergy_deck)
            values.append(synergy_meter)

        synergies_to_play = {k: v for k, v in zip(keys, values) if v >= 0.3}
        return synergies_to_play.keys()

    def get_plays_from_list(self, energy_remaining: int, state: GameState) -> (int, List[int]):
        plays = []
        card_list = self.get_synergy_cards_in_hand(self, state)
        for card in card_list:
            for i, cih in enumerate(state.hand.cards):
                if card == cih.id.lower() and energy_remaining >= cih.cost and cih.is_playable:
                    energy_remaining -= cih.cost
                    plays.append(i)
        return energy_remaining, plays

    def get_target(self, monsters: List[dict]) -> int:
        highest_health = None
        target = -1
        for i, m in enumerate(monsters):
            effective_health = m['current_hp'] + m['block']
            if (highest_health is None or effective_health < highest_health) and not m['is_gone']:
                highest_health = effective_health
                target = i
        return target
