import json
from typing import List

from rs.game.deck import Deck
from rs.machine.command import Command


class GameState:
    def __init__(self, json_state: json):
        self.json = json_state
        if "combat_state" in json_state["game_state"]:
            self.hand: Deck = Deck(json_state["game_state"]["combat_state"]["hand"])
            self.draw_pile: Deck = Deck(json_state["game_state"]["combat_state"]["draw_pile"])
            self.discard_pile: Deck = Deck(json_state["game_state"]["combat_state"]["discard_pile"])
            self.exhaust_pile: Deck = Deck(json_state["game_state"]["combat_state"]["exhaust_pile"])
        self.deck: Deck = Deck(json_state["game_state"]["deck"])

    def game_state(self):
        return self.json["game_state"]

    def has_command(self, command: Command) -> bool:
        return command.value in self.json.get("available_commands")

    def get_player_combat(self):
        return self.game_state()["combat_state"]["player"]

    def get_monsters(self):
        return self.game_state()["combat_state"]["monsters"]

    def get_choice_list(self):
        return self.game_state()["choice_list"]

    def get_relics(self):
        return self.game_state()["relics"]

    def get_potions(self):
        return self.game_state()["potions"]

    def are_potions_full(self) -> bool:
        for pot in self.get_potions():
            if pot['id'] == "Potion Slot":
                return False
        return True

    def screen_type(self):
        return self.game_state()["screen_type"]

    def floor(self):
        return self.game_state()["floor"]

    def player_entangled(self):
        return bool(next((p for p in self.get_player_combat()["powers"] if p["id"] == "Entangled"), None))
