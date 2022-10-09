import copy
import math
from typing import List

from rs.calculator.card_effects import get_card_effects, TargetType
from rs.calculator.cards import Card
from rs.calculator.powers import PowerId
from rs.calculator.relics import Relics, RelicId
from rs.calculator.targets import Target, Player
from rs.game.card import CardType

Play = tuple[int, int]  # card index, target index (-1 for none/all)


class HandState:

    def __init__(self, player: Player, hand: List[Card] = None, discard_pile: List[Card] = None,
                 draw_pile: List[Card] = None,
                 targets: List[Target] = None, relics: Relics = None):

        self.player: Player = player
        self.hand: List[Card] = [] if hand is None else hand
        self.discard_pile: List[Card] = [] if discard_pile is None else discard_pile
        self.draw_pile: List[Card] = [] if draw_pile is None else draw_pile
        self.targets: List[Target] = [] if targets is None else targets
        self.relics: Relics = {} if relics is None else relics

    def get_plays(self) -> List[Play]:
        plays: List[Play] = []

        # Turn-over conditions
        if self.relics.get(RelicId.VELVET_CHOKER, 0) >= 6 or self.player.current_hp <= 0:
            return plays

        for card_idx, card in enumerate(self.hand):
            if not is_card_playable(card, self.player):
                continue
            if card.needs_target:
                for target_idx, target in enumerate(self.targets):
                    if can_card_target_target(card, target):
                        plays.append((card_idx, target_idx))
            else:
                plays.append((card_idx, -1))

        return plays

    def transform_from_play(self, play: Play):
        (card_index, target_index) = play
        card = self.hand[card_index]
        effects = get_card_effects(card, self.player.powers, self.draw_pile, self.discard_pile, self.hand)

        # relic mods:
        if RelicId.STRIKE_DUMMY in self.relics and "strike" in card.id.value:
            for effect in effects:
                effect.damage += 3

        if self.relics.get(RelicId.PEN_NIB, 0) >= 9 and card.type == CardType.ATTACK:
            for effect in effects:
                effect.damage *= 2

        player_weak_modifier = 1 if not self.player.powers.get(PowerId.WEAK) else 0.75
        player_strength_modifier = self.player.powers.get(PowerId.STRENGTH, 0)
        monster_vulnerable_modifier = 1.5 if not self.relics.get(RelicId.PAPER_PHROG) else 1.75

        # play the card
        self.player.energy -= card.cost
        for effect in effects:
            # deal damage to target
            if effect.hits:
                if effect.target == TargetType.SELF:
                    self.player.inflict_damage(base_damage=effect.damage, hits=1, blockable=effect.blockable,
                                               vulnerable_modifier=1)
                else:
                    damage = math.floor((effect.damage + player_strength_modifier) * player_weak_modifier)
                    if effect.target == TargetType.MONSTER:
                        self.targets[target_index].inflict_damage(damage, effect.hits, effect.blockable,
                                                                  vulnerable_modifier=monster_vulnerable_modifier)
                    elif effect.target == TargetType.ALL_MONSTERS:
                        for target in self.targets:
                            target.inflict_damage(damage, effect.hits, effect.blockable, monster_vulnerable_modifier)

            # block (always applies to player right?)
            if effect.block:
                self.player.block += effect.block

            # Apply any powers from the card
            if effect.applies_powers:
                if effect.target == TargetType.SELF:
                    self.player.add_powers(effect.applies_powers)
                elif effect.target == TargetType.MONSTER:
                    self.targets[target_index].add_powers(effect.applies_powers)
                elif effect.target == TargetType.ALL_MONSTERS:
                    for target in self.targets:
                        target.add_powers(copy.deepcopy(effect.applies_powers))
            # energy gain
            self.player.energy += effect.energy_gain

        # post turn counter increments (we can make this more dynamic/clean as we get more of them)
        if RelicId.VELVET_CHOKER in self.relics:
            self.relics[RelicId.VELVET_CHOKER] += 1

        if RelicId.NUNCHAKU in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.NUNCHAKU] += 1
            if self.relics[RelicId.NUNCHAKU] >= 10:
                self.player.energy += 1
                self.relics[RelicId.NUNCHAKU] -= 10

        if RelicId.PEN_NIB in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.PEN_NIB] += 1
            if self.relics[RelicId.PEN_NIB] >= 10:
                self.relics[RelicId.PEN_NIB] -= 10

        # TODO -> exhaust here
        self.discard_pile.append(card)
        del self.hand[card_index]


def is_card_playable(card: Card, player: Player) -> bool:
    # unplayable cards like burn, wound, and reflex
    if card.cost == -1:
        return False

    # in general, has enough energy
    if player.energy < card.cost:
        return False

    # todo -> special card-specific logic, like clash

    return True


def can_card_target_target(card: Card, target: Target) -> bool:
    if not card.needs_target:
        return False  # should never be reached, but still :shrug:

    if target.current_hp <= 0:
        return False

    # TODO -> any other cases? Maybe a check on if the target is targetable, who knows.

    return True
