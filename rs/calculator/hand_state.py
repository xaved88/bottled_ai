import math
import copy
from typing import List

from rs.calculator.card_effects import get_card_effects, TargetType
from rs.calculator.cards import Card, CardId, get_card
from rs.calculator.helper import pickle_deepcopy
from rs.calculator.powers import PowerId
from rs.calculator.relics import Relics, RelicId
from rs.calculator.targets import Target, Player, Monster
from rs.game.card import CardType

Play = tuple[int, int]  # card index, target index (-1 for none/all), (-2 for discard)
PLAY_DISCARD = -2


class HandState:

    def __init__(self, player: Player, hand: List[Card] = None, discard_pile: List[Card] = None,
                 exhaust_pile: List[Card] = None, draw_pile: List[Card] = None,
                 monsters: List[Monster] = None, relics: Relics = None, amount_to_discard: int = 0):

        self.player: Player = player
        self.hand: List[Card] = [] if hand is None else hand
        self.discard_pile: List[Card] = [] if discard_pile is None else discard_pile
        self.exhaust_pile: List[Card] = [] if exhaust_pile is None else exhaust_pile
        self.draw_pile: List[Card] = [] if draw_pile is None else draw_pile
        self.monsters: List[Monster] = [] if monsters is None else monsters
        self.relics: Relics = {} if relics is None else relics
        self.amount_to_discard: int = amount_to_discard
        self.__is_first_play: bool = False  # transient and used only internally
        self.__starting_energy: int = 0  # transient and used only internally

    def get_plays(self) -> List[Play]:
        plays: List[Play] = []

        # Prep time warp
        time_warp_full = False
        for idx, monster in enumerate(self.monsters):
            if monster.powers.get(PowerId.TIME_WARP, 0) >= 12:
                time_warp_full = True

        # Turn over conditions
        if self.relics.get(RelicId.VELVET_CHOKER, 0) >= 6 or time_warp_full or self.player.current_hp <= 0:
            return plays

        for card_idx, card in enumerate(self.hand):
            if not is_card_playable(card, self.player, self.hand):
                continue
            if card.needs_target:
                for target_idx, target in enumerate(self.monsters):
                    if can_card_target_target(card, target):
                        plays.append((card_idx, target_idx))
            else:
                plays.append((card_idx, -1))

        return plays

    def get_discards(self) -> List[Play]:
        return [(i, PLAY_DISCARD) for i, c in enumerate(self.hand)]

    def transform_from_play(self, play: Play, is_first_play: bool):
        self.__is_first_play = is_first_play
        self.__starting_energy = self.player.energy

        (card_index, target_index) = play
        card = self.hand[card_index]

        if target_index == PLAY_DISCARD:
            self.transform_from_discard(card, card_index)
            return

        # play the card
        self.player.energy -= card.cost
        effects = get_card_effects(card, self.player, self.draw_pile, self.discard_pile, self.hand)

        # pain
        pain_count = len([1 for c in self.hand if c.id == CardId.PAIN])
        if pain_count:
            self.player.inflict_damage(self.player, pain_count, 1, False, vulnerable_modifier=1, is_attack=False)

        # damage bonuses:
        damage_additive_bonus = 0
        if RelicId.STRIKE_DUMMY in self.relics and "strike" in card.id.value:
            damage_additive_bonus += 3
        if card.type == CardType.ATTACK and self.player.powers.get(PowerId.VIGOR):
            damage_additive_bonus += self.player.powers.get(PowerId.VIGOR, 0)
            del self.player.powers[PowerId.VIGOR]
        # Added accuracy as additive damage bonus only for shivs
        if card.id == CardId.SHIV and self.player.powers.get(PowerId.ACCURACY):
            damage_additive_bonus += self.player.powers.get(PowerId.ACCURACY, 0)
        if RelicId.WRIST_BLADE in self.relics and card.cost == 0 and card.type == CardType.ATTACK:
            damage_additive_bonus += 4

        if damage_additive_bonus:
            for effect in effects:
                effect.damage += damage_additive_bonus
        if self.relics.get(RelicId.PEN_NIB, 0) >= 9 and card.type == CardType.ATTACK:
            for effect in effects:
                effect.damage *= 2
        player_min_attack_hp_damage = 1 if not self.relics.get(RelicId.THE_BOOT) else 5

        player_weak_modifier = 1 if not self.player.powers.get(PowerId.WEAKENED) else 0.75
        player_strength_modifier = self.player.powers.get(PowerId.STRENGTH, 0)
        monster_vulnerable_modifier = 1.5 if not self.relics.get(RelicId.PAPER_PHROG) else 1.75

        # pre play stuff
        if self.player.powers.get(PowerId.RAGE) and card.type == CardType.ATTACK:
            self.player.block += self.player.powers[PowerId.RAGE]

        for effect in effects:
            # custom post hooks
            for hook in effect.pre_hooks:
                hook(self, effect, target_index)

            # heal
            if effect.heal:
                self.player.heal(effect.heal)

            # deal damage to target
            if effect.hits:
                if effect.target == TargetType.SELF:
                    self.player.inflict_damage(base_damage=effect.damage, source=self.player, hits=1,
                                               blockable=effect.blockable,
                                               vulnerable_modifier=1, is_attack=False)
                else:
                    damage = math.floor((effect.damage + player_strength_modifier) * player_weak_modifier)
                    if effect.target == TargetType.MONSTER:
                        (hp_damage) = self.monsters[target_index].inflict_damage(source=self.player, base_damage=damage,
                                                                                 hits=effect.hits,
                                                                                 blockable=effect.blockable,
                                                                                 vulnerable_modifier=monster_vulnerable_modifier,
                                                                                 min_hp_damage=player_min_attack_hp_damage)
                        effect.hp_damage = hp_damage
                    elif effect.target == TargetType.ALL_MONSTERS:
                        effect.hp_damage = 0
                        for target in self.monsters:
                            (hp_damage) = target.inflict_damage(self.player, damage, effect.hits, effect.blockable,
                                                                monster_vulnerable_modifier,
                                                                min_hp_damage=player_min_attack_hp_damage)
                            effect.hp_damage += hp_damage

            # block (always applies to player right?)
            if effect.block:
                block = max(effect.block + self.player.powers.get(PowerId.DEXTERITY, 0), 0)
                frail_mod = 0.75 if self.player.powers.get(PowerId.FRAIL, 0) else 1
                self.player.block += math.floor(block * frail_mod)

            # Apply any powers from the card
            if effect.applies_powers:
                if effect.target == TargetType.SELF:
                    self.player.add_powers(effect.applies_powers)
                else:
                    targets = [self.monsters[target_index]] if effect.target == TargetType.MONSTER else self.monsters
                    for target in targets:
                        applied_powers = target.add_powers(pickle_deepcopy(effect.applies_powers))
                        if self.relics.get(RelicId.CHAMPION_BELT) and PowerId.VULNERABLE in applied_powers:
                            target.add_powers({PowerId.WEAKENED: 1})

            # energy gain
            self.player.energy += effect.energy_gain

            # card draw
            if effect.draw:
                self.draw_cards(effect.draw)

            # discard
            if effect.amount_to_discard:
                self.amount_to_discard += effect.amount_to_discard

        if card in self.hand:  # because some cards like fiend fire, will destroy themselves before they can follow this route
            idx = self.hand.index(card)
            if card.exhausts:
                self.exhaust_pile.append(card)
            elif card.type != CardType.POWER:
                self.discard_pile.append(card)
            del self.hand[idx]

        for effect in effects:
            # custom post hooks
            for hook in effect.post_hooks:
                hook(self, effect, target_index)  # TODO - would be nice to find a way to resolve this circular dep

        # post card play counter increments (we can make this more dynamic/clean as we get more of them)
        if RelicId.VELVET_CHOKER in self.relics:
            self.relics[RelicId.VELVET_CHOKER] += 1

        for idx, monster in enumerate(self.monsters):
            if monster.powers.get(PowerId.TIME_WARP) is not None:
                self.monsters[idx].powers[PowerId.TIME_WARP] += 1

        if RelicId.NUNCHAKU in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.NUNCHAKU] += 1
            if self.relics[RelicId.NUNCHAKU] >= 10:
                self.player.energy += 1
                self.relics[RelicId.NUNCHAKU] -= 10

        if RelicId.PEN_NIB in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.PEN_NIB] += 1
            if self.relics[RelicId.PEN_NIB] >= 10:
                self.relics[RelicId.PEN_NIB] -= 10

        if RelicId.ORNAMENTAL_FAN in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.ORNAMENTAL_FAN] += 1
            if self.relics[RelicId.ORNAMENTAL_FAN] >= 3:
                self.relics[RelicId.ORNAMENTAL_FAN] -= 3
                self.player.block += 4

        if RelicId.LETTER_OPENER in self.relics and card.type == CardType.SKILL:
            self.relics[RelicId.LETTER_OPENER] += 1
            if self.relics[RelicId.LETTER_OPENER] >= 3:
                self.relics[RelicId.LETTER_OPENER] -= 3
                for monster in self.monsters:
                    if monster.current_hp > 0:
                        monster.inflict_damage(self.player, 5, 1, vulnerable_modifier=1, is_attack=False)

        # Check if order is correct
        if self.player.powers.get(PowerId.THOUSAND_CUTS):
            thousand_cuts_damage = self.player.powers.get(PowerId.THOUSAND_CUTS, 0)
            if thousand_cuts_damage > 0:
                for monster in self.monsters:
                    if monster.current_hp > 0:
                        monster.inflict_damage(self.player, thousand_cuts_damage, 1, vulnerable_modifier=1,
                                               is_attack=False)

        if self.player.powers.get(PowerId.AFTER_IMAGE):
            after_image_block = self.player.powers.get(PowerId.AFTER_IMAGE, 0)
            if after_image_block > 0:
                self.player.block += after_image_block

        # minion battles -> make sure a non-minion is alive, otherwise kill them all.
        if [m for m in self.monsters if m.powers.get(PowerId.MINION)]:
            if not [m for m in self.monsters if not m.powers.get(PowerId.MINION) and m.current_hp > 0]:
                for m in self.monsters:
                    m.current_hp = 0

    def transform_from_discard(self, card: Card, index: int):
        self.discard_pile.append(card)
        del self.hand[index]
        self.amount_to_discard -= 1
        # any discard synergies/handlers -> To implement later
        pass

    def end_turn(self):
        if RelicId.ORICHALCUM in self.relics and self.player.block == 0:
            self.player.block += 6

        # special end of turn
        self.player.block += self.player.powers.get(PowerId.PLATED_ARMOR, 0)
        self.player.block += self.player.powers.get(PowerId.METALLICIZE, 0)

        # regret
        regret_count = len([1 for c in self.hand if c.id == CardId.REGRET])
        if regret_count:
            self.player.inflict_damage(self.player, regret_count * len(self.hand), 1, False, vulnerable_modifier=1,
                                       is_attack=False)
        # poison
        for monster in self.monsters:
            poison = monster.powers.get(PowerId.POISON, 0)
            if poison > 0:
                monster.powers[PowerId.POISON] -= 1
                monster.inflict_damage(monster, poison, 1, blockable=False, is_attack=False)

        # todo - decrement buffs that should be counted down?
        # todo - increment relics that should be counted up

        # apply enemy damage
        player_vulnerable_mod = 1.5 if not self.relics.get(RelicId.ODD_MUSHROOM) else 1.25
        for monster in self.monsters:
            if monster.current_hp > 0 and monster.hits:
                monster_weak_modifier = 1 if not monster.powers.get(PowerId.WEAKENED) else 0.75 if not self.relics.get(
                    RelicId.PAPER_KRANE) else 0.6
                monster_strength = monster.powers.get(PowerId.STRENGTH, 0)
                damage = max(math.floor((monster.damage + monster_strength) * monster_weak_modifier), 0)
                self.player.inflict_damage(monster, damage, monster.hits, vulnerable_modifier=player_vulnerable_mod)

    def get_state_hash(self) -> str:  # designed to get the meaningful state and hash it.
        state_string = self.player.get_state_string()
        for m in self.monsters:
            state_string += m.get_state_string()

        # cards
        state_string += "h"
        shand = sorted(self.hand, key=lambda c: c.id.value + str(c.upgrade), )
        for card in shand:
            state_string += card.get_state_string()
        state_string += "d"
        dishand = sorted(self.discard_pile, key=lambda c: c.id.value + str(c.upgrade), )
        for card in dishand:
            state_string += card.get_state_string()
        state_string += "w"
        drawhand = sorted(self.draw_pile, key=lambda c: c.id.value + str(c.upgrade), )
        for card in drawhand:
            state_string += card.get_state_string()

        # relics
        state_string += "r"
        for relic in self.relics.keys():
            state_string += f"{relic.value}.{self.relics[relic]},"
        return state_string

    def draw_cards(self, amount: int):
        if PowerId.NO_DRAW in self.player.powers:
            return

        early = self.__is_first_play
        free = self.__starting_energy <= self.player.energy

        # determine which type of card to draw based on energy
        card_type = CardId.DRAW_FREE_EARLY if free and early \
            else CardId.DRAW_FREE if free and not early \
            else CardId.DRAW_PAY_EARLY if not free and early \
            else CardId.DRAW_PAY

        # can't draw more than 10 cards, will discard the played card tho
        amount = min(amount, 11 - len(self.draw_pile))
        self.hand += [get_card(card_type) for i in range(amount)]


def is_card_playable(card: Card, player: Player, hand: List[Card]) -> bool:
    # unplayable cards like burn, wound, and reflex
    if card.cost == -1:
        return False
    # in general, has enough energy
    if player.energy < card.cost:
        return False
    # entangled case
    if card.type == CardType.ATTACK and player.powers.get(PowerId.ENTANGLED):
        return False

    # special card-specific logic, like clash
    if card.id == CardId.CLASH and len([1 for c in hand if c.type != CardType.ATTACK]):
        return False

    return True


def can_card_target_target(card: Card, target: Target) -> bool:
    if not card.needs_target:
        return False  # should never be reached, but still :shrug:

    if target.current_hp <= 0:
        return False

    return True
