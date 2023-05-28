from typing import List

from rs.ai.requested_strike.handlers.battle_handler import LegacyBattleHandler
from rs.machine.state import GameState, get_stacks_of_power


class LagavulinHandler(LegacyBattleHandler):

    def __init__(self):
        self.aggro_prefs = [
            'Perfected Strike',
            'Bludgeon',
            'Bash',
            'Uppercut',
            'Clothesline'
        ]

    def can_handle(self, state: GameState) -> bool:
        return super().can_handle(state) and state.has_monster("Lagavulin")

    def handle(self, state: GameState) -> List[str]:
        turn = state.combat_state()["turn"]
        laggy = state.get_monsters()[0]
        vulnerable = bool(get_stacks_of_power(laggy['powers'], "Vulnerable"))


        # If it's turn 1 or two, and he's not vulnerable, allow only bash / shockwave (shockwave preferred)
        if turn < 3 and not vulnerable:
            if cmd := self.get_play_command_if_can_play("Shockwave", state):
                return cmd
            if cmd := self.get_play_command_if_can_play("Bash", state):
                return cmd
            return ["end"]

        # if not vulnerable AND have 3 energy, AND have thunderclap, play that first
        if not vulnerable and state.get_player_combat()['energy'] >= 3:
            if cmd := self.get_play_command_if_can_play("Thunderclap", state):
                return cmd

        # Otherwise, try and play heavy damage cards if you can
        for pref in self.aggro_prefs:
            if cmd := self.get_play_command_if_can_play(pref, state):
                return cmd

        # Otherwise, let the next handler pick it up
        return []

    def get_play_command_if_can_play(self, card_id: str, state: GameState):
        idx = state.hand.get_card_index(card_id)
        if idx > -1 and state.hand.cards[idx].is_playable:
            return [f"play {str(idx + 1)} 0"]
        return []