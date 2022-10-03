import json
from typing import List

from rs.game.deck import Deck
from rs.machine.command import Command


class GameState:
    def __init__(self, json_state: json):
        self.json = json_state
        if "game_state" in json_state:
            if "combat_state" in json_state["game_state"]:
                self.hand: Deck = Deck(json_state["game_state"]["combat_state"]["hand"])
                self.draw_pile: Deck = Deck(json_state["game_state"]["combat_state"]["draw_pile"])
                self.discard_pile: Deck = Deck(json_state["game_state"]["combat_state"]["discard_pile"])
                self.exhaust_pile: Deck = Deck(json_state["game_state"]["combat_state"]["exhaust_pile"])
            self.deck: Deck = Deck(json_state["game_state"]["deck"])

    def is_game_running(self) -> bool:
        return self.json["in_game"]

    def game_state(self):
        return self.json["game_state"]

    def combat_state(self):
        if 'combat_state' in self.game_state():
            return self.game_state()["combat_state"]
        else:
            return None

    def has_command(self, command: Command) -> bool:
        return command.value in self.json.get("available_commands")

    def get_player_combat(self):
        return self.game_state()["combat_state"]["player"]

    def get_player_health_percentage(self) -> float:
        return self.game_state()["current_hp"] / self.game_state()["max_hp"]

    def get_monsters(self):
        if "combat_state" not in self.game_state():
            return []
        return self.game_state()["combat_state"]["monsters"]

    def get_choice_list(self):
        return self.game_state()["choice_list"]

    def get_relics(self):
        return self.game_state()["relics"]

    def has_relic(self, relic_name: str) -> bool:
        for relic in self.get_relics():
            if relic['name'] == relic_name:
                return True
        return False

    def get_potions(self):
        return self.game_state()["potions"]

    def are_potions_full(self) -> bool:
        for pot in self.get_potions():
            if pot['id'] == "Potion Slot":
                return False
        return True

    def screen_type(self):
        return self.game_state()["screen_type"]

    def floor(self) -> int:
        return self.game_state()["floor"]

    def player_entangled(self):
        return bool(next((p for p in self.get_player_combat()["powers"] if p["id"] == "Entangled"), None))

    def get_deck_card_list(self) -> dict[str, int]:
        cards = {}
        for card in self.deck.cards:
            name = card.name.lower()
            if name in cards:
                cards[name] += 1
            else:
                cards[name] = 1
        return cards

    def get_map(self) -> List[dict]:
        return self.game_state()["map"]

    def has_monster(self, name: str) -> bool:
        for monster in self.get_monsters():
            if monster['name'] == name:
                return True
        return False

    def get_player_block(self) -> int:
        return self.get_player_combat()['block']


def get_stacks_of_power(powers: List[dict], power_id: str):
    for power in powers:
        if power['id'] == power_id:
            return power['amount']
    return 0
