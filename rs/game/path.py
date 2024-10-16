import math
from typing import List, Callable

from rs.game.room import Room, RoomType
from rs.machine.state import GameState

GameStateCalculation = Callable[[GameState], float]
GameStateAndNumberCalculation = Callable[[GameState, float], float]
SurvivabilityRewardCalculation = Callable[[float, float], float]

default_hallway_fight_health_loss: GameStateCalculation = lambda state: state.game_state()['act'] * 5
default_elite_fight_health_loss: GameStateCalculation = lambda state: (state.game_state()['act'] + 1) * 15
default_event_value_reward: GameStateCalculation = lambda state: 1 if state.game_state()['act'] == 1 else 1.5
default_gold_at_shop_reward: GameStateAndNumberCalculation = lambda state, gold_to_spend: gold_to_spend / 100
default_gold_after_boss_reward: GameStateCalculation = lambda state: state.game_state()['gold'] / 200
default_survivability_reward: SurvivabilityRewardCalculation = lambda reward, survivability: reward + (
            survivability - 1) * 15


class PathHandlerConfig:
    def __init__(
            self,
            hallway_fight_base_reward: float = 1,
            hallway_fight_prayer_wheel: float = 0.3,
            hallway_question_card_reward: float = 0.15,
            hallway_fight_gold: int = 15,
            hallway_fight_health_loss: GameStateCalculation = default_hallway_fight_health_loss,
            elite_base_reward: float = 1,  # this does not include the relic, that's added separately
            elite_question_card_reward: float = 0.15,
            elite_emerald_key_reward: float = 0,
            elite_fight_gold: int = 30,
            elite_fight_health_loss: GameStateCalculation = default_elite_fight_health_loss,
            elite_fight_emerald_key_extra_health_loss: int = 5,
            relic_reward: float = 1.5,
            curse_reward_loss: float = 1.5,
            upgrade_reward: float = 1.1,
            event_value_reward: GameStateCalculation = default_event_value_reward,
            gold_at_shop_reward: GameStateAndNumberCalculation = default_gold_at_shop_reward,
            gold_after_boss_reward: GameStateCalculation = default_gold_after_boss_reward,
            survivability_reward_calculation: SurvivabilityRewardCalculation = default_survivability_reward,
    ):
        self.hallway_fight_base_reward: float = hallway_fight_base_reward
        self.hallway_fight_prayer_wheel: float = hallway_fight_prayer_wheel
        self.hallway_question_card_reward: float = hallway_question_card_reward
        self.hallway_fight_gold: float = hallway_fight_gold
        self.hallway_fight_health_loss: GameStateCalculation = hallway_fight_health_loss
        self.elite_question_card_reward: float = elite_question_card_reward
        self.elite_base_reward: float = elite_base_reward
        self.elite_emerald_key_reward: float = elite_emerald_key_reward
        self.elite_fight_gold: int = elite_fight_gold
        self.elite_fight_health_loss: GameStateCalculation = elite_fight_health_loss
        self.elite_fight_emerald_key_extra_health_loss: int = elite_fight_emerald_key_extra_health_loss
        self.relic_reward: float = relic_reward
        self.curse_reward_loss: float = curse_reward_loss
        self.upgrade_reward: float = upgrade_reward
        self.event_value_reward: GameStateCalculation = event_value_reward
        self.gold_at_shop_reward: GameStateAndNumberCalculation = gold_at_shop_reward
        self.gold_after_boss_reward: GameStateCalculation = gold_after_boss_reward
        self.survivability_reward_calculation: SurvivabilityRewardCalculation = survivability_reward_calculation


class Path:
    def __init__(self, rooms: List[Room]):
        self.reward_survivability: float = -100.0
        self.rooms = rooms
        self.room_count: dict[RoomType, int] = {RoomType.MONSTER: 0, RoomType.QUESTION: 0, RoomType.ELITE: 0,
                                                RoomType.CAMPFIRE: 0, RoomType.TREASURE: 0, RoomType.SHOP: 0,
                                                RoomType.BOSS: 0}
        for room in self.rooms:
            self.room_count[room.type] += 1

    def calculate_reward_survivability(self, state: GameState, config: PathHandlerConfig):
        self.reward_survivability: float = -100.0

        # These don't need to be member vars, but making it so for easier debugging and viewing later
        self.reward: float = 0.0
        self.survivability: float = 1.0
        self.gold: int = state.game_state()['gold']
        self.hp: int = state.game_state()["current_hp"]
        max_hp: int = state.game_state()["max_hp"]
        act: int = state.game_state()['act']
        floor: int = state.game_state()['floor']

        emerald_key_available = state.get_burning_elite_position()

        for room in self.rooms:
            # MONSTERS
            if room.type == RoomType.MONSTER:
                # reward
                self.reward += config.hallway_fight_base_reward
                if state.has_relic("Prayer Wheel"):
                    self.reward += config.hallway_fight_prayer_wheel
                if state.has_relic("Question Card"):
                    self.reward += config.hallway_question_card_reward
                # gold
                self.gold += config.hallway_fight_gold
                # health
                self.hp -= config.hallway_fight_health_loss(state)
                if state.has_relic("Meat on the Bone") and self.hp / max_hp < 0.5:
                    self.hp += 12
                if state.has_relic("Blood Vial"):
                    self.hp += 2
                if state.has_relic("Black Blood"):
                    self.hp += 12
                if state.has_relic("Burning Blood"):
                    self.hp += 6
            # ELITE FIGHTS
            elif room.type == RoomType.ELITE:
                # reward
                self.reward += config.elite_base_reward + config.relic_reward
                if state.has_relic("Question Card"):
                    self.reward += config.elite_question_card_reward
                if state.has_relic("Black Star"):
                    self.reward += config.relic_reward
                # gold
                self.gold += 30
                # health
                self.hp -= config.elite_fight_health_loss(state)
                if state.has_relic("Meat on the Bone") and self.hp / max_hp < 0.5:
                    self.hp += 12
                if state.has_relic("Blood Vial"):
                    self.hp += 2
                if state.has_relic("Black Blood"):
                    self.hp += 12
                if state.has_relic("Burning Blood"):
                    self.hp += 6
                # burning elite
                if emerald_key_available and room.id == state.get_burning_elite_position():
                    self.reward += config.elite_emerald_key_reward
                    self.hp -= config.elite_fight_emerald_key_extra_health_loss
            elif room.type == RoomType.TREASURE:
                self.reward += config.relic_reward
                if state.has_relic("Matryoshka") and state.get_relic_counter("Matryoshka") >= 1:
                    self.reward += 1
                if state.has_relic("Cursed Key"):
                    self.reward -= config.curse_reward_loss
            # CAMPFIRES
            elif room.type == RoomType.CAMPFIRE:
                if state.has_relic("Eternal Feather"):
                    self.hp += math.floor(len(state.get_deck_card_list_by_id()) / 5) * 3
                fusion_hammer = state.has_relic("Fusion Hammer")
                coffee_dripper = state.has_relic("Coffee Dripper")
                if not fusion_hammer and (coffee_dripper or self.hp / max_hp >= 0.6):
                    self.reward += config.upgrade_reward
                if not coffee_dripper and (fusion_hammer or self.hp / max_hp < 0.6):
                    self.hp += max_hp * 0.3
                    if state.has_relic("Regal Pillow"):
                        self.hp += 15
                    if state.has_relic("Dreamcatcher"):
                        self.reward += 0.5
            # QUESTION MARKS
            elif room.type == RoomType.QUESTION:
                self.reward += config.event_value_reward(state)
            # SHOPS
            elif room.type == RoomType.SHOP:
                if state.has_relic("Membership Card"):
                    gold_to_spend = min(self.gold, 300)
                    self.gold -= gold_to_spend
                else:
                    gold_to_spend = min(self.gold, 200) * 2
                    self.gold -= gold_to_spend / 2
                self.reward += config.gold_at_shop_reward(state, gold_to_spend)
            # DONE WITH ROOM CALCULATIONS
            survive_barrier = max_hp / 4
            if self.hp < survive_barrier:
                self.survivability *= max((self.hp + survive_barrier * 2) / (survive_barrier * 3), 0)
            self.hp = min(max(self.hp, 0), max_hp)

        if act != 3:
            self.reward += config.gold_after_boss_reward(state)

        # ALL PATHS HAVE THEIR REWARD + SURVIVABILITY NOW, CALCULATE REWARD/SURVIVABILITY Value
        if self.survivability != 0:
            self.reward_survivability = config.survivability_reward_calculation(self.reward, self.survivability)
