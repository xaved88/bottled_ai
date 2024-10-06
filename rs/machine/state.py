import json
from typing import List

from rs.calculator.interfaces.memory_items import MemoryItem
from rs.game.deck import Deck
from rs.machine.command import Command
from rs.machine.orb import Orb
from rs.machine.the_bots_memory_book import TheBotsMemoryBook


class GameState:
    def __init__(self, json_state: json, the_bots_memory_book: TheBotsMemoryBook):
        self.the_bots_memory_book: TheBotsMemoryBook = the_bots_memory_book
        self.json = json_state
        if "game_state" in json_state:
            if "combat_state" in json_state["game_state"]:
                self.hand: Deck = Deck(json_state["game_state"]["combat_state"]["hand"])
                self.draw_pile: Deck = Deck(json_state["game_state"]["combat_state"]["draw_pile"])
                self.discard_pile: Deck = Deck(json_state["game_state"]["combat_state"]["discard_pile"])
                self.exhaust_pile: Deck = Deck(json_state["game_state"]["combat_state"]["exhaust_pile"])

                current_turn = json_state["game_state"]["combat_state"]["turn"]
                if self.the_bots_memory_book.memory_general[MemoryItem.LAST_KNOWN_TURN] != current_turn:
                    self.the_bots_memory_book.set_new_turn_state()
                self.the_bots_memory_book.memory_general[MemoryItem.LAST_KNOWN_TURN] = current_turn

            else:
                self.the_bots_memory_book.set_new_battle_state()

            self.deck: Deck = Deck(json_state["game_state"]["deck"])
            self.memory_by_card = self.the_bots_memory_book.memory_by_card.copy()
            self.memory_general = self.the_bots_memory_book.memory_general.copy()

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

    def get_choice_list_upgrade_stripped_from_choice(self):
        choice_list_modified = self.get_choice_list()
        for idx, choice in enumerate(choice_list_modified):
            choice_list_modified[idx] = choice.replace("+", "")
        return choice_list_modified

    def get_relics(self):
        return self.game_state()["relics"]

    def has_relic(self, relic_name: str) -> bool:
        for relic in self.get_relics():
            if relic['name'].lower() == relic_name.lower():
                return True
        return False

    def get_relic_counter(self, relic_name: str) -> int:
        for relic in self.get_relics():
            if relic['name'] == relic_name:
                return relic['counter']
        return False

    def get_potions(self):
        return self.game_state()["potions"]

    def get_held_potion_names(self):
        potion_names = []
        for pot in self.game_state()["potions"]:
            potion_names.append(pot["name"])
        potion_names = [potion_name.lower() for potion_name in potion_names]
        return potion_names

    def get_reward_potion_names(self):
        potion_names = []
        for reward in self.game_state()["screen_state"]["rewards"]:
            if reward["reward_type"] == "POTION":
                potion_names.append(reward["potion"]["name"])
        potion_names = [potion_name.lower() for potion_name in potion_names]
        return potion_names

    def are_potions_full(self) -> bool:
        for pot in self.get_potions():
            if pot['id'] == "Potion Slot":
                return False
        return True

    def screen_type(self):
        return self.game_state()["screen_type"]

    def screen_state(self):
        return self.game_state()["screen_state"]

    def screen_state_max_cards(self):
        state = self.screen_state()
        return 0 if not state else state["max_cards"]

    def screen_state_must_pick_card(self):
        state = self.screen_state()
        return 1 if not state else state["can_pick_zero"]

    def screen_state_exhaust_cards(self):
        return 0 if not self.current_action() == "ExhaustAction" else self.screen_state_max_cards()

    def screen_state_discard_cards(self):
        return 0 if not self.current_action() == "DiscardAction" else self.screen_state_max_cards()

    def current_action(self):
        if self.game_state()["screen_type"] == "HAND_SELECT" or \
                (self.combat_state() is not None and self.game_state()["screen_type"] == "GRID"):
            return self.game_state()["current_action"]

    def get_cards_discarded_this_turn(self):
        state = self.combat_state()
        return 0 if not state else state["cards_discarded_this_turn"]

    def floor(self) -> int:
        return self.game_state()["floor"]

    def player_entangled(self):
        return bool(next((p for p in self.get_player_combat()["powers"] if p["id"] == "Entangled"), None))

    def get_deck_card_list_by_id(self) -> dict[str, int]:
        cards = {}
        for card in self.deck.cards:
            card_id = card.id.lower()
            if card_id in cards:
                cards[card_id] += 1
            else:
                cards[card_id] = 1
        return cards

    def get_deck_card_list_by_name_with_upgrade_stripped(self) -> dict[str, int]:
        cards = {}
        for card in self.deck.cards:
            name = card.name.replace("+", "")
            name = name.lower()
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

    def get_player_orbs(self) -> list[(Orb, int)]:
        orbs = self.get_player_combat()['orbs']
        if not orbs:
            return []
        return [(Orb(o['id']), o['evoke_amount']) for o in orbs if 'id' in o and o['id'] != 'Empty' and 'evoke_amount' in o]

    def get_player_orb_slots(self) -> int:
        orbs = self.get_player_combat()['orbs']
        if not orbs:
            return 0
        return len(orbs)

    def get_falling_event_options(self) -> list:
        options = []

        def extract_card_from_text(text):
            keyword = "Lose"
            if keyword in text:
                return text.split(keyword, 1)[1].strip()

        for option in self.screen_state()["options"]:
            if not option["disabled"]:
                text = option["text"]
                options.append(extract_card_from_text(text).lower())
        for idx, choice in enumerate(options):
            options[idx] = choice.replace("+", "")
        return options

    def get_act_4_keys(self):
        # just the first letter of the key is enough
        keys = []
        if "keys" not in self.game_state():
            return ['Communication Mod out of date']
        for key in self.game_state()["keys"]:
            if self.game_state()["keys"].get(key):
                keys.append(key[0])
        return keys

    def get_burning_elite_position(self):
        burning_elite_position = 0
        if 'emerald_key_node' in self.game_state()["screen_state"]:
            be = self.game_state()["screen_state"]["emerald_key_node"]
            burning_elite_position = str(be["x"]) + "_" + str(be["y"])
        return burning_elite_position


