import copy
import math
from typing import List

from rs.calculator.card_effects import get_card_effects, TargetType
from rs.calculator.cards import Card
from rs.calculator.powers import PowerId
from rs.calculator.relics import Relics
from rs.calculator.targets import Target, Player

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

        ## TODO -> here early return if we have 6 stacks of choker, or maybe time eater's turn popper. Also, dead

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

        player_weak_modifier = 1 if not self.player.powers.get(PowerId.WEAK) else 0.75
        player_strength_modifier = self.player.powers.get(PowerId.STRENGTH, 0)

        for effect in effects:
            # deal damage to target
            if effect.hits:
                if effect.target == TargetType.SELF:
                    self.player.inflict_damage(base_damage=effect.damage, hits=1, blockable=effect.blockable,
                                               vulnerable_modifier=1)
                else:
                    damage = math.floor((effect.damage + player_strength_modifier) * player_weak_modifier)
                    if effect.target == TargetType.MONSTER:
                        self.targets[target_index].inflict_damage(damage, effect.hits, effect.blockable)
                    elif effect.target == TargetType.ALL_MONSTERS:
                        for target in self.targets:
                            target.inflict_damage(damage, effect.hits, effect.blockable)

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

            # TODO -> anything more?

        self.player.energy -= card.cost
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
