import math
from typing import List

from rs.game.room import Room, RoomType
from rs.machine.state import GameState


class Path:
    def __init__(self, rooms: List[Room]):
        self.reward_survivability: float = -100.0
        self.rooms = rooms
        self.room_count: dict[RoomType, int] = {RoomType.MONSTER: 0, RoomType.QUESTION: 0, RoomType.ELITE: 0,
                                                RoomType.CAMPFIRE: 0, RoomType.TREASURE: 0, RoomType.SHOP: 0,
                                                RoomType.BOSS: 0}
        for room in self.rooms:
            self.room_count[room.type] += 1

    def calculate_reward_survivability(self, state: GameState):
        self.reward_survivability: float = -100.0

        # These don't need to be member vars, but making it so for easier debugging and viewing later
        self.reward: float = 0.0
        self.survivability: float = 1.0
        self.gold: int = state.game_state()['gold']
        self.hp: int = state.game_state()["current_hp"]
        max_hp: int = state.game_state()["max_hp"]
        act: int = state.game_state()['act']
        floor: int = state.game_state()['floor']

        for room in self.rooms:
            # MONSTERS
            if room.type == RoomType.MONSTER:
                # reward
                self.reward += 1
                if state.has_relic("Prayer Wheel"):
                    self.reward += 0.3
                if state.has_relic("Question Card"):
                    self.reward += 0.15
                # gold
                self.gold += 15
                # health
                self.hp -= 5 * act
                if state.has_relic("Meat on the Bone") and self.hp / max_hp < 0.5:
                    self.hp += 12
                if state.has_relic("Blood Vial"):
                    self.hp += 2
                if state.has_relic("Black Blood"):
                    self.hp += 6
            # ELITE FIGHTS
            elif room.type == RoomType.ELITE:
                # reward
                self.reward += 2.5
                if state.has_relic("Question Card"):
                    self.reward += 0.15
                if state.has_relic("Black Star"):
                    self.reward += 1.5
                # gold
                self.gold += 30
                # health
                # TODO -> make the first 15 based on the floor number... because early elites = harder and we can't compensate for that yet
                # TODO -> figure out burning elite with green key -> doesn't seem like that data is in the map/gamestate?!?!
                self.hp -= 15 + 15 * act
                if state.has_relic("Meat on the Bone") and self.hp / max_hp < 0.5:
                    self.hp += 12
                if state.has_relic("Blood Vial"):
                    self.hp += 2
                if state.has_relic("Black Blood"):
                    self.hp += 6
            elif room.type == RoomType.TREASURE:
                self.reward += 1.5
                if state.has_relic("Matroshka"):  # TODO -> charges?
                    self.reward += 1
                if state.has_relic("Cursed Key"):
                    self.reward -= 1
            # CAMPFIRES
            elif room.type == RoomType.CAMPFIRE:
                if state.has_relic("Eternal Feather"):
                    self.hp += math.floor(len(state.get_deck_card_list()) / 5) * 3
                fusion_hammer = state.has_relic("Fusion Hammer")
                coffee_dripper = state.has_relic("Coffee Dripper")
                if not fusion_hammer and (coffee_dripper or self.hp / max_hp >= 0.6):
                    self.reward += 1
                if not coffee_dripper and (fusion_hammer or self.hp / max_hp < 0.6):
                    self.hp += max_hp * 0.3
                    if state.has_relic("Regal Pillow"):
                        self.hp += 15
                    if state.has_relic("Dreamcatcher"):
                        self.reward += 0.5
            # QUESTION MARKS
            elif room.type == RoomType.QUESTION:
                self.reward += 1 if act == 1 else 1.5
            # SHOPS
            elif room.type == RoomType.SHOP:
                if state.has_relic("Membership Card"):
                    gold_to_spend = min(self.gold, 300)
                    self.gold -= gold_to_spend
                else:
                    gold_to_spend = min(self.gold, 200) * 2
                    self.gold -= gold_to_spend / 2
                self.reward += gold_to_spend / 100
            # DONE WITH ROOM CALCULATIONS
            survive_barrier = max_hp / 4
            if self.hp < survive_barrier:
                self.survivability *= max((self.hp + survive_barrier * 2) / (survive_barrier * 3), 0)
            self.hp = min(max(self.hp,0), max_hp)

        if act != 3:
            self.reward += self.gold / 200

        # ALL PATHS HAVE THEIR REWARD + SURVIVABILITY NOW, CALCULATE REWARD/SURVIVABILITY Value
        if self.survivability != 0:
            self.reward_survivability = self.reward + (self.survivability - 1) * 15
