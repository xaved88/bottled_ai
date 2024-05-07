import math
from typing import List, Tuple

from rs.calculator.card_cost import Cost
from rs.calculator.card_effects import get_card_effects
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.helper import pickle_deepcopy
from rs.calculator.interfaces.battle_state_interface import BattleStateInterface
from rs.calculator.interfaces.card_effects_interface import TargetType
from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.interfaces.memory_items import MemoryItem, ResetSchedule, StanceType
from rs.calculator.interfaces.monster_interface import MonsterInterface, find_lowest_hp_monster
from rs.calculator.interfaces.player import PlayerInterface
from rs.calculator.interfaces.relics import Relics
from rs.calculator.powers import DEBUFFS
from rs.game.card import CardType

Play = tuple[int, int]  # card index, target index (-1 for none/all, -2 for discard)
PLAY_DISCARD = -2


class BattleState(BattleStateInterface):

    def __init__(self, player: PlayerInterface, hand: List[CardInterface] = None,
                 discard_pile: List[CardInterface] = None, exhaust_pile: List[CardInterface] = None,
                 draw_pile: List[CardInterface] = None, monsters: List[MonsterInterface] = None, relics: Relics = None,
                 must_discard: bool = False, amount_to_discard: int = 0, cards_discarded_this_turn: int = 0,
                 total_random_damage_dealt: int = 0, total_random_poison_added: int = 0,
                 orbs: List[Tuple[OrbId, int]] = None, orb_slots: int = 0, memory_general: dict = None,
                 memory_by_card: dict[CardId, dict[ResetSchedule, dict[str, int]]] = None):
        self.player: PlayerInterface = player
        self.hand: List[CardInterface] = [] if hand is None else hand
        self.discard_pile: List[CardInterface] = [] if discard_pile is None else discard_pile
        self.exhaust_pile: List[CardInterface] = [] if exhaust_pile is None else exhaust_pile
        self.draw_pile: List[CardInterface] = [] if draw_pile is None else draw_pile
        self.monsters: List[MonsterInterface] = [] if monsters is None else monsters
        self.relics: Relics = {} if relics is None else relics
        self.must_discard: bool = must_discard
        self.amount_to_discard: int = amount_to_discard
        self.cards_discarded_this_turn: int = cards_discarded_this_turn
        self.total_random_damage_dealt: int = total_random_damage_dealt
        self.total_random_poison_added: int = total_random_poison_added
        self.__is_first_play: bool = False  # transient and used only internally
        self.__starting_energy: int = 0  # transient and used only internally
        self.orbs: List[(OrbId, int)] = [] if orbs is None else orbs
        self.orb_slots: int = orb_slots
        self.memory_general: dict = {} if memory_general is None else memory_general
        self.memory_by_card: dict[
            CardId, dict[ResetSchedule, dict[str, int]]] = {} if memory_by_card is None else memory_by_card

    def get_plays(self) -> List[Play]:
        plays: List[Play] = []

        if self.is_turn_forced_to_be_over():
            return plays

        for card_idx, card in enumerate(self.hand):
            if not is_card_playable(card, self.player, self.hand, len(self.draw_pile)):
                continue
            if card.needs_target:
                for monster_idx, monster in enumerate(self.monsters):
                    if can_card_target_monster(card, monster):
                        plays.append((card_idx, monster_idx))
            else:
                plays.append((card_idx, -1))

        return plays

    def get_discards(self) -> List[Play]:
        return [(i, PLAY_DISCARD) for i, c in enumerate(self.hand)]

    def transform_from_play(self, play: Play, is_first_play: bool):
        self.__is_first_play = is_first_play
        self.__starting_energy = self.player.energy

        if RelicId.DAMARU in self.relics and self.is_new_turn():
            self.add_memory_value(MemoryItem.MANTRA_THIS_BATTLE, 1)

        if RelicId.TEARDROP_LOCKET in self.relics and \
                self.is_new_turn() and \
                self.get_memory_value(MemoryItem.LAST_KNOWN_TURN) == 1:
            self.change_stance(StanceType.CALM)

        if PowerId.DEVOTION in self.player.powers and self.is_new_turn():
            self.add_memory_value(MemoryItem.MANTRA_THIS_BATTLE, self.player.powers.get(PowerId.DEVOTION, 0))

        (card_index, target_index) = play
        card = self.hand[card_index]

        if target_index == PLAY_DISCARD:
            self.transform_from_discard(card, card_index)
            return

        # some stuff needs to happen early
        if self.player.powers.get(PowerId.CORRUPTION):
            for c in self.hand:
                if c.type == CardType.SKILL:
                    c.exhausts = True
                    if card.cost != Cost.unplayable:
                        c.cost = 0

        if self.relics.get(RelicId.MEDICAL_KIT):
            for c in self.hand:
                if c.type == CardType.STATUS:
                    c.exhausts = True
                    c.cost = 0

        # play the card
        is_free_bc_power = (self.player.powers.get(PowerId.FREE_ATTACK_POWER) and card.type == CardType.ATTACK)

        if card.cost != Cost.x_cost:
            if not is_free_bc_power:
                self.player.energy -= card.cost
        self.resolve_card_play(card, target_index)
        if card.cost == Cost.x_cost:
            if not is_free_bc_power:
                self.player.energy = 0

        # repeats
        if self.player.powers.get(PowerId.INTERNAL_ECHO_FORM_READY):
            self.repeat_card(card, target_index, PowerId.INTERNAL_ECHO_FORM_READY, lose_repeat_even_if_incomplete=False)
        if self.player.powers.get(PowerId.DUPLICATION_POTION_POWER):
            self.repeat_card(card, target_index, PowerId.DUPLICATION_POTION_POWER, lose_repeat_even_if_incomplete=False)
        if self.player.powers.get(PowerId.AMPLIFY) and card.type == CardType.POWER:
            self.repeat_card(card, target_index, PowerId.AMPLIFY)
        if self.player.powers.get(PowerId.BURST) and card.type == CardType.SKILL:
            self.repeat_card(card, target_index, PowerId.BURST)
        if self.player.powers.get(PowerId.DOUBLE_TAP) and card.type == CardType.ATTACK:
            self.repeat_card(card, target_index, PowerId.DOUBLE_TAP)
        if self.relics.get(RelicId.NECRONOMICON) and self.get_memory_value(
                MemoryItem.NECRONOMICON_READY) and card.type == CardType.ATTACK and card.cost >= 2:
            self.repeat_card(card, target_index, RelicId.NECRONOMICON)

    def repeat_card(self, card: CardInterface, target_index: int, reason_to_repeat,
                    lose_repeat_even_if_incomplete: bool = True):
        if lose_repeat_even_if_incomplete:
            if type(reason_to_repeat) == PowerId:
                self.player.powers[reason_to_repeat] -= 1
            if reason_to_repeat == RelicId.NECRONOMICON:
                self.add_memory_value(MemoryItem.NECRONOMICON_READY, -1)

        if self.is_turn_forced_to_be_over():
            return
        if target_index > -1 and self.monsters[target_index].is_gone:
            return
        # todo -> battle is over
        self.resolve_card_play(card, target_index)

        if not lose_repeat_even_if_incomplete:
            if type(reason_to_repeat) == PowerId:
                self.player.powers[reason_to_repeat] -= 1

    def resolve_card_play(self, card: CardInterface, target_index: int):
        effects = get_card_effects(card, self.player, self.draw_pile, self.discard_pile, self.hand)

        # pain
        pain_count = len([1 for c in self.hand if c.id == CardId.PAIN])
        if pain_count:
            self.player.inflict_damage(self.player, pain_count, 1, False, vulnerable_modifier=1, is_attack=False)

        # damage bonuses:
        damage_additive_bonus = 0
        if RelicId.STRIKE_DUMMY in self.relics and "strike" in card.id.value:
            damage_additive_bonus += 3
        if self.player.powers.get(PowerId.VIGOR) and card.type == CardType.ATTACK:
            damage_additive_bonus += self.player.powers.get(PowerId.VIGOR, 0)
            del self.player.powers[PowerId.VIGOR]
        if self.player.powers.get(PowerId.ACCURACY) and card.id == CardId.SHIV:
            damage_additive_bonus += self.player.powers.get(PowerId.ACCURACY, 0)
        if RelicId.WRIST_BLADE in self.relics and card.cost == 0 and card.type == CardType.ATTACK:
            damage_additive_bonus += 4

        if damage_additive_bonus:
            for effect in effects:
                effect.damage += damage_additive_bonus
        if self.player.powers.get(PowerId.DOUBLE_DAMAGE, 0) and card.type == CardType.ATTACK:
            for effect in effects:
                effect.damage *= 2
        if self.relics.get(RelicId.PEN_NIB, 0) >= 9 and card.type == CardType.ATTACK:
            for effect in effects:
                effect.damage *= 2
        if self.get_memory_value(MemoryItem.STANCE) == StanceType.WRATH:
            for effect in effects:
                effect.damage *= 2
        if self.get_memory_value(MemoryItem.STANCE) == StanceType.DIVINITY:
            for effect in effects:
                effect.damage *= 3
        player_min_attack_hp_damage = 1 if not self.relics.get(RelicId.THE_BOOT) else 5

        player_weak_modifier = 1 if not self.player.powers.get(PowerId.WEAKENED) else 0.75
        player_strength_modifier = self.player.powers.get(PowerId.STRENGTH, 0)
        monster_vulnerable_modifier = 1.5 if not self.relics.get(RelicId.PAPER_PHROG) else 1.75

        # pre play stuff
        if self.player.powers.get(PowerId.RAGE) and card.type == CardType.ATTACK:
            self.add_player_block(self.player.powers[PowerId.RAGE])

        for effect in effects:
            # custom pre hooks
            for hook in effect.pre_hooks:
                hook(self, effect, card, target_index)

            # heal
            if effect.heal:
                self.player.heal(effect.heal, True, self.relics)

            # deal damage to target
            if effect.hits:
                if effect.target == TargetType.SELF:
                    self.player.inflict_damage(base_damage=effect.damage, source=self.player, hits=1,
                                               blockable=effect.blockable,
                                               vulnerable_modifier=1, is_attack=False)
                else:
                    damage = math.floor((effect.damage + player_strength_modifier) * player_weak_modifier)
                    if effect.target == TargetType.MONSTER:
                        (hp_damage) = self.monsters[target_index].inflict_damage(
                            source=self.player, base_damage=damage,
                            hits=effect.hits,
                            blockable=effect.blockable,
                            vulnerable_modifier=monster_vulnerable_modifier,
                            min_hp_damage=player_min_attack_hp_damage)
                        effect.hp_damage = hp_damage

                        if PowerId.BLOCK_RETURN in self.monsters[target_index].powers:
                            for hits in range(effect.hits):
                                self.add_player_block(self.monsters[target_index].powers[PowerId.BLOCK_RETURN])

                    elif effect.target == TargetType.ALL_MONSTERS:
                        effect.hp_damage = 0
                        for target in self.monsters:
                            (hp_damage) = target.inflict_damage(self.player, damage, effect.hits, effect.blockable,
                                                                monster_vulnerable_modifier,
                                                                min_hp_damage=player_min_attack_hp_damage)
                            effect.hp_damage += hp_damage

                            if PowerId.BLOCK_RETURN in target.powers:
                                for hits in range(effect.hits):
                                    self.add_player_block(target.powers[PowerId.BLOCK_RETURN])

            # block (always applies to player right?)
            if effect.block:
                block = max(effect.block + self.player.powers.get(PowerId.DEXTERITY, 0), 0)
                frail_mod = 0.75 if self.player.powers.get(PowerId.FRAIL, 0) else 1
                self.add_player_block(math.floor(block * frail_mod) * max(1, effect.block_times))

            # orbs
            if effect.channel_orbs:
                for orb in effect.channel_orbs:
                    self.channel_orb(orb)

            # energy gain
            self.player.energy += effect.energy_gain

            # card draw
            if effect.draw:
                self.draw_cards(effect.draw)

            # discard
            if effect.amount_to_discard:
                self.amount_to_discard += effect.amount_to_discard

        # memory stuff
        last_played = MemoryItem.TYPE_LAST_PLAYED
        orange_pellets = True if RelicId.ORANGE_PELLETS in self.relics else False

        if card.type == CardType.ATTACK:
            self.add_memory_value(MemoryItem.ATTACKS_THIS_TURN, 1)
            self.add_memory_value(last_played, CardType.ATTACK)
            if orange_pellets:
                self.add_memory_value(MemoryItem.ORANGE_PELLETS_ATTACK, 1)
        elif card.type == CardType.SKILL:
            self.add_memory_value(last_played, CardType.SKILL)
            if orange_pellets:
                self.add_memory_value(MemoryItem.ORANGE_PELLETS_SKILL, 1)
        elif card.type == CardType.POWER:
            self.add_memory_value(last_played, CardType.POWER)
            if orange_pellets:
                self.add_memory_value(MemoryItem.ORANGE_PELLETS_POWER, 1)
        else:
            self.add_memory_value(last_played, CardType.OTHER)

        self.add_memory_value(MemoryItem.CARDS_THIS_TURN, 1)

        # dispose of cards being played
        if card in self.hand:  # b/c some cards like fiend fire, will destroy themselves before they follow this route
            idx = self.hand.index(card)
            if card.exhausts:
                self.exhaust_card(card)
            elif card.type == CardType.POWER:
                del self.hand[idx]
            elif card.id == CardId.TANTRUM:
                del self.hand[idx]
            else:
                self.discard_pile.append(card)
                del self.hand[idx]

        # post card play PLAYER power checks
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
                self.add_player_block(after_image_block)

        if self.player.powers.get(PowerId.PANACHE):
            self.player.powers[PowerId.PANACHE] -= 1
            if self.player.powers.get(PowerId.PANACHE) == 0:
                for monster in self.monsters:
                    if monster.current_hp > 0:
                        monster.inflict_damage(self.player, 10, 1, vulnerable_modifier=1, is_attack=False)
                self.player.powers[PowerId.PANACHE] = 5

        if self.player.powers.get(PowerId.HEATSINK) and card.type == CardType.POWER:
            self.draw_cards(self.player.powers.get(PowerId.HEATSINK))

        if self.player.powers.get(PowerId.STORM) and card.type == CardType.POWER:
            for i in range(self.player.powers.get(PowerId.STORM)):
                self.channel_orb(OrbId.LIGHTNING)

        if self.player.powers.get(PowerId.FREE_ATTACK_POWER) and card.type == CardType.ATTACK:
            self.player.powers[PowerId.FREE_ATTACK_POWER] -= 1

        # post card play MONSTER power checks
        for monster in self.monsters:
            if monster.powers.get(PowerId.TIME_WARP) is not None:
                monster.add_powers({PowerId.TIME_WARP: 1}, self.player.relics, self.player.powers)
            if monster.powers.get(PowerId.CHOKED):
                monster.inflict_damage(self.player, monster.powers.get(PowerId.CHOKED), 1, vulnerable_modifier=1,
                                       is_attack=False)
            if monster.powers.get(PowerId.ANGER_NOB):
                if card.type == CardType.SKILL:
                    monster.add_powers({PowerId.STRENGTH: monster.powers.get(PowerId.ANGER_NOB)}, self.player.relics,
                                       self.player.powers)
            if monster.powers.get(PowerId.CURIOSITY):
                if card.type == CardType.POWER:
                    monster.add_powers({PowerId.STRENGTH: monster.powers.get(PowerId.CURIOSITY)}, self.player.relics,
                                       self.player.powers)
            if monster.powers.get(PowerId.HEX):
                if card.type != CardType.ATTACK:
                    for i in range(monster.powers.get(PowerId.HEX)):
                        self.spawn_in_draw(get_card(CardId.DAZED))

        for effect in effects:
            # apply any powers from the card
            if effect.applies_powers:
                if effect.target == TargetType.SELF:
                    self.player.add_powers(effect.applies_powers, self.player.relics, self.player.powers)
                else:
                    targets = [self.monsters[target_index]] if effect.target == TargetType.MONSTER else self.monsters
                    for target in targets:
                        target.add_powers(pickle_deepcopy(effect.applies_powers), self.player.relics,
                                          self.player.powers)

                if PowerId.MANTRA in effect.applies_powers:
                    for power in effect.applies_powers:
                        if power is PowerId.MANTRA:
                            self.add_memory_value(MemoryItem.MANTRA_THIS_BATTLE, effect.applies_powers[power])

            # custom post hooks
            for hook in effect.post_hooks:
                hook(self, effect, card, target_index)

            # stance
            if effect.sets_stance:
                self.change_stance(effect.sets_stance)

            # add cards to hand
            if effect.spawn_cards_in_hand:
                self.spawn_in_hand(effect.spawn_cards_in_hand[0], effect.spawn_cards_in_hand[1])
            if effect.spawn_cards_in_draw:
                self.spawn_in_draw(effect.spawn_cards_in_draw[0], effect.spawn_cards_in_draw[1])
            if effect.spawn_cards_in_discard:
                self.spawn_in_discard(effect.spawn_cards_in_discard[0], effect.spawn_cards_in_discard[1])

        # post card play relic checks
        if RelicId.VELVET_CHOKER in self.relics:
            self.relics[RelicId.VELVET_CHOKER] += 1

        if RelicId.INK_BOTTLE in self.relics:
            self.relics[RelicId.INK_BOTTLE] += 1
            if self.relics[RelicId.INK_BOTTLE] >= 10:
                self.draw_cards(1)
                self.relics[RelicId.INK_BOTTLE] -= 10

        if RelicId.SHURIKEN in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.SHURIKEN] += 1
            if self.relics[RelicId.SHURIKEN] >= 3:
                self.player.add_powers({PowerId.STRENGTH: 1}, self.player.relics, self.player.powers)
                self.relics[RelicId.SHURIKEN] -= 3

        if RelicId.KUNAI in self.relics and card.type == CardType.ATTACK:
            self.relics[RelicId.KUNAI] += 1
            if self.relics[RelicId.KUNAI] >= 3:
                self.player.add_powers({PowerId.DEXTERITY: 1}, self.player.relics, self.player.powers)
                self.relics[RelicId.KUNAI] -= 3

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
                self.add_player_block(4)

        if RelicId.LETTER_OPENER in self.relics and card.type == CardType.SKILL:
            self.relics[RelicId.LETTER_OPENER] += 1
            if self.relics[RelicId.LETTER_OPENER] >= 3:
                self.relics[RelicId.LETTER_OPENER] -= 3
                for monster in self.monsters:
                    if monster.current_hp > 0:
                        monster.inflict_damage(self.player, 5, 1, vulnerable_modifier=1, is_attack=False)

        if RelicId.BIRD_FACED_URN in self.relics and card.type == CardType.POWER:
            self.player.heal(2, True, self.relics)

        if RelicId.UNCEASING_TOP in self.relics and len(self.hand) == 0:
            self.draw_cards(1)

        if RelicId.ORANGE_PELLETS in self.relics \
                and self.get_memory_value(MemoryItem.ORANGE_PELLETS_ATTACK) \
                and self.get_memory_value(MemoryItem.ORANGE_PELLETS_SKILL) \
                and self.get_memory_value(MemoryItem.ORANGE_PELLETS_POWER):
            for power in self.player.powers:
                if power in DEBUFFS:
                    self.player.powers[power] = 0

        # special late case for Mantra
        if self.player.powers.get(PowerId.MANTRA):
            if self.player.powers[PowerId.MANTRA] >= 10:
                self.player.powers[PowerId.MANTRA] -= 10
                self.change_stance(StanceType.DIVINITY)

        self.kill_monsters()

    def transform_from_discard(self, card: CardInterface, index: int):
        self.discard_card(card)
        self.amount_to_discard -= 1
        pass

    def end_turn(self):

        if RelicId.ORICHALCUM in self.relics and self.player.block == 0:
            self.add_player_block(6)

        if RelicId.FROZEN_CORE in self.relics and len(self.orbs) < self.orb_slots:
            self.channel_orb(OrbId.FROST)

        self.trigger_orbs_passives()

        if RelicId.CLOAK_CLASP in self.relics:
            self.add_player_block(len(self.hand))

        if self.player.powers.get(PowerId.LIKE_WATER) and self.get_memory_value(MemoryItem.STANCE) == StanceType.CALM:
            self.add_player_block(self.player.powers.get(PowerId.LIKE_WATER, 0))

        if RelicId.STONE_CALENDAR in self.relics and self.relics[RelicId.STONE_CALENDAR] == 7:
            for monster in self.monsters:
                if monster.current_hp > 0:
                    monster.inflict_damage(self.player, 52, 1, vulnerable_modifier=1, is_attack=False)

        self.add_player_block(self.player.powers.get(PowerId.PLATED_ARMOR, 0))
        self.add_player_block(self.player.powers.get(PowerId.METALLICIZE, 0))

        if self.player.powers.get(PowerId.WRAITH_FORM_POWER):
            self.player.add_powers({PowerId.DEXTERITY: -self.player.powers.get(PowerId.WRAITH_FORM_POWER)},
                                   self.player.relics, self.player.powers)

        if self.player.powers.get(PowerId.CONSTRICTED, 0):
            self.player.inflict_damage(self.player, self.player.powers.get(PowerId.CONSTRICTED, 0), 1,
                                       vulnerable_modifier=1, is_attack=False)

        if self.player.powers.get(PowerId.REGENERATION_PLAYER, 0) and self.player.current_hp > 0:
            self.player.heal(self.player.powers.get(PowerId.REGENERATION_PLAYER, 0), True, self.relics)
            self.player.powers[PowerId.REGENERATION_PLAYER] -= 1

        if self.player.powers.get(PowerId.STUDY, 0):
            for i in range(self.player.powers.get(PowerId.STUDY, 0)):
                self.spawn_in_draw(get_card(CardId.INSIGHT))

        # single-turn power removal
        if self.player.powers.get(PowerId.WAVE_OF_THE_HAND, 0):
            self.player.powers[PowerId.WAVE_OF_THE_HAND] = 0

        # deal with the remaining cards in hand
        cards_to_keep: list[CardInterface] = []

        for c in self.hand:
            was_auto_played = None
            might_stay_retain = None
            might_stay_pyramid = None

            for effect in get_card_effects(c, self.player, self.draw_pile, self.discard_pile, self.hand):
                # for various curses and burns
                for hook in effect.end_turn_hooks:
                    hook(self, effect, None, None)
                    was_auto_played = c
                if effect.retains or self.player.powers.get(PowerId.EQUILIBRIUM, 0):
                    might_stay_retain = c
                elif self.player.relics.get(RelicId.RUNIC_PYRAMID):
                    might_stay_pyramid = c

            if c.ethereal:
                self.exhaust_card(c, handle_remove=False)
            elif c is was_auto_played:
                self.discard_pile.append(c)
            elif c is might_stay_retain:
                if self.player.powers.get(PowerId.ESTABLISHMENT):
                    c.cost -= 1
                    if c.cost <= 0:
                        c.cost = 0
                if c.id is CardId.PERSEVERANCE:
                    self.add_memory_by_card(c.id, c.uuid, 2 if not c.upgrade else 3)
                if c.id is CardId.WINDMILL_STRIKE:
                    self.add_memory_by_card(c.id, c.uuid, 4 if not c.upgrade else 5)
                if c.id is CardId.SANDS_OF_TIME:
                    c.cost -= 1
                    if c.cost <= 0:
                        c.cost = 0
                cards_to_keep.append(c)
            elif c is might_stay_pyramid:
                cards_to_keep.append(c)
            else:
                self.discard_pile.append(c)

        self.hand = cards_to_keep.copy()

        # this is getting into the enemy's turn now
        # enemy powers
        for monster in self.monsters:
            poison = monster.powers.get(PowerId.POISON, 0)
            if poison > 0:
                monster.powers[PowerId.POISON] -= 1
                monster.inflict_damage(monster, poison, 1, blockable=False, vulnerable_modifier=1, is_attack=False)
            if monster.powers.get(PowerId.REGENERATE_ENEMY) and monster.current_hp > 0:
                monster.heal(monster.powers.get(PowerId.REGENERATE_ENEMY), False, self.relics)

        # last check in case there were some more monsters that should die
        self.kill_monsters()

        # apply enemy damage
        player_vulnerable_mod = 1.5 if not self.relics.get(RelicId.ODD_MUSHROOM) else 1.25
        for monster in self.monsters:
            if monster.current_hp > 0 and monster.hits and monster.damage != -1:
                monster_weak_modifier = 1 if not monster.powers.get(PowerId.WEAKENED) else 0.75 if not self.relics.get(
                    RelicId.PAPER_KRANE) else 0.6
                monster_strength = monster.powers.get(PowerId.STRENGTH, 0)
                damage = max(math.floor((monster.damage + monster_strength) * monster_weak_modifier), 0)
                if self.get_stance() is StanceType.WRATH:
                    damage *= 2
                self.player.inflict_damage(monster, damage, monster.hits, vulnerable_modifier=player_vulnerable_mod)

            if monster.powers.get(PowerId.EXPLOSIVE):
                monster.powers[PowerId.EXPLOSIVE] -= 1
                if monster.powers[PowerId.EXPLOSIVE] < 1:
                    self.player.inflict_damage(monster, 30, 1, vulnerable_modifier=1, is_attack=False)

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

        # memory book
        state_string += "m"
        for card_id in self.memory_by_card.keys():
            for reset_schedule in self.memory_by_card[card_id].keys():
                for uuid in self.memory_by_card[card_id][reset_schedule].keys():
                    state_string += card_id.value + uuid + str(self.memory_by_card[card_id][reset_schedule][uuid])

        # relics
        state_string += "r"
        for relic in self.relics.keys():
            state_string += f"{relic.value}.{self.relics[relic]},"

        # orbs
        if self.orb_slots:
            state_string += "o"
            for (orb, amount) in self.orbs:
                state_string += orb.name[0]
                if orb.name[0] == "D":
                    state_string += str(amount)
                state_string += str(self.orb_slots)

        return state_string

    def draw_cards(self, amount: int):
        if PowerId.NO_DRAW in self.player.powers:
            return

        early = self.__is_first_play
        free = self.__starting_energy <= self.player.energy

        # determine which type of card to draw with based on energy
        card_type = CardId.DRAW_FREE_EARLY if free and early \
            else CardId.DRAW_FREE if free and not early \
            else CardId.DRAW_PAY_EARLY if not free and early \
            else CardId.DRAW_PAY

        # can't draw more than 10 cards, will discard the played card tho
        amount = min(amount, 11 - len(self.hand))
        self.hand += [get_card(card_type) for _ in range(amount)]

        # mainly just making some numbers work here, not looking into the piles yet for real
        for i in range(amount):
            if len(self.draw_pile) <= 0:
                self.draw_pile = self.discard_pile.copy()
                self.discard_pile.clear()

                if RelicId.THE_ABACUS in self.relics:
                    self.add_player_block(6)
                if RelicId.SUNDIAL in self.relics:
                    self.relics[RelicId.SUNDIAL] += 1
                    if self.relics[RelicId.SUNDIAL] >= 3:
                        self.relics[RelicId.SUNDIAL] -= 3
                        self.player.energy += 2

            # note: we're still allowing draws even if draw pile is empty because that's how a bunch of tests are set up
            # currently, and we're not complete functionality-wise for draws anyway
            if len(self.draw_pile) > 0:
                del self.draw_pile[0]

    def spawn_in_hand(self, card_to_spawn: CardInterface, amount: int = 1):
        amount_that_fits = min(amount, 10 - len(self.hand))
        amount_that_does_not_fit = amount - amount_that_fits

        if self.player.powers.get(PowerId.MASTER_REALITY):
            card_to_spawn.upgrade = 1

        for i in range(amount_that_fits):
            self.hand.append(card_to_spawn)
        for i in range(amount_that_does_not_fit):
            self.discard_pile.append(card_to_spawn)

    def spawn_in_draw(self, card_to_spawn: CardInterface, amount: int = 1):

        if self.player.powers.get(PowerId.MASTER_REALITY):
            card_to_spawn.upgrade = 1

        for i in range(amount):
            self.draw_pile.append(card_to_spawn)

    def spawn_in_discard(self, card_to_spawn: CardInterface, amount: int = 1):

        if self.player.powers.get(PowerId.MASTER_REALITY):
            card_to_spawn.upgrade = 1

        for i in range(amount):
            self.discard_pile.append(card_to_spawn)

    def discard_card(self, card: CardInterface):
        self.hand.remove(card)
        self.discard_pile.append(card)
        # self_discarded hook
        for effect in get_card_effects(card, self.player, self.draw_pile, self.discard_pile, self.hand):
            for hook in effect.post_self_discarded_hooks:
                hook(self, effect, card, None)
        # others_discarded hook
        for hand_card in self.hand:
            for effect in get_card_effects(hand_card, self.player, self.draw_pile, self.discard_pile, self.hand):
                for hook in effect.post_others_discarded_hooks:
                    hook(hand_card)
        self.cards_discarded_this_turn += 1

        # post discard stuff
        if RelicId.TOUGH_BANDAGES in self.relics:
            self.add_player_block(3)

        if RelicId.HOVERING_KITE in self.relics and self.cards_discarded_this_turn == 1:
            self.player.energy += 1

        if RelicId.TINGSHA in self.relics:
            self.inflict_random_target_damage(3, 1, affected_by_vulnerable=False, is_attack=False)

    def exhaust_card(self, card: CardInterface, handle_remove: bool = True):
        self.exhaust_pile.append(card)
        if handle_remove:
            self.hand.remove(card)

        # post exhaust stuff
        if self.player.powers.get(PowerId.DARK_EMBRACE):
            self.draw_cards(self.player.powers.get(PowerId.DARK_EMBRACE, 0))

        if self.player.powers.get(PowerId.FEEL_NO_PAIN):
            self.add_player_block(self.player.powers.get(PowerId.FEEL_NO_PAIN, 0))

        if self.relics.get(RelicId.CHARONS_ASHES):
            for m in self.monsters:
                m.inflict_damage(self.player, 3, 1, vulnerable_modifier=1, is_attack=False)

        # would theoretically go in a post-exhaust hook but at least for now this is the only card that needs it
        if card.id == CardId.SENTINEL:
            if not card.upgrade:
                self.player.energy += 2
            else:
                self.player.energy += 3

    def inflict_random_target_damage(self, base_damage: int, hits: int, blockable: bool = True,
                                     affected_by_vulnerable: bool = True, is_attack: bool = True,
                                     min_hp_damage: int = 1, is_orbs: bool = False):
        alive_monsters = len([True for m in self.monsters if m.current_hp > 0])

        vulnerable_modifier = 1.5 if not self.relics.get(RelicId.PAPER_PHROG) else 1.75
        if not affected_by_vulnerable:
            vulnerable_modifier = 1

        if alive_monsters == 1:
            for monster in self.monsters:
                if monster.current_hp > 0:
                    monster.inflict_damage(self.player, base_damage, hits, blockable, vulnerable_modifier, is_attack,
                                           min_hp_damage, is_orbs)
        else:
            self.total_random_damage_dealt += base_damage * hits

    def add_random_poison(self, poison_amount: int, hits: int):
        alive_monsters = len([True for m in self.monsters if m.current_hp > 0])
        if alive_monsters == 1:
            for monster in self.monsters:
                if monster.current_hp > 0:
                    for i in range(hits):
                        monster.add_powers({PowerId.POISON: poison_amount}, self.player.relics, self.player.powers)
        else:
            self.total_random_poison_added += poison_amount * hits

    def add_player_block(self, amount: int):
        self.player.block += amount
        if amount > 0:
            if self.player.powers.get(PowerId.JUGGERNAUT, 0):
                self.inflict_random_target_damage(self.player.powers.get(PowerId.JUGGERNAUT, 0), 1,
                                                  affected_by_vulnerable=False, is_attack=False)
            if self.player.powers.get(PowerId.WAVE_OF_THE_HAND, 0):
                for monster in self.monsters:
                    monster.add_powers({PowerId.WEAKENED: self.player.powers.get(PowerId.WAVE_OF_THE_HAND, 0)},
                                       self.player.relics,
                                       self.player.powers)

    def kill_monsters(self):
        # minion battles -> make sure a non-minion is alive, otherwise kill them all.
        if [m for m in self.monsters if m.powers.get(PowerId.MINION)]:
            if not [m for m in self.monsters if not m.powers.get(PowerId.MINION) and m.current_hp > 0]:
                for m in self.monsters:
                    m.current_hp = 0

        # normal killing
        for m in self.monsters:
            if m.current_hp <= 0 and not m.is_gone:
                m.damage = 0
                m.hits = 0
                m.is_gone = True
                if RelicId.GREMLIN_HORN in self.relics:
                    self.player.energy += 1
                    self.draw_cards(1)
                if m.powers.get(PowerId.CORPSE_EXPLOSION, 0):
                    corpse_explosion_damage = m.max_hp
                    corpse_explosion_hits = m.powers.get(PowerId.CORPSE_EXPLOSION)
                    for monster in self.monsters:
                        if monster.current_hp > 0:
                            monster.inflict_damage(self.player, corpse_explosion_damage, corpse_explosion_hits,
                                                   vulnerable_modifier=1,
                                                   is_attack=False)

    def trigger_orbs_passives(self):
        focus = self.player.powers.get(PowerId.FOCUS, 0)
        for index, (orb, amount) in enumerate(self.orbs):
            for _ in range(1 + (index == 0 and RelicId.GOLD_PLATED_CABLES in self.relics)):
                if orb == OrbId.LIGHTNING:
                    if self.player.powers.get(PowerId.ELECTRO):
                        for m in self.monsters:
                            m.inflict_damage(self.player, 3 + focus, 1, vulnerable_modifier=1, is_attack=False,
                                             is_orbs=True)
                    else:
                        self.inflict_random_target_damage(base_damage=3 + focus, hits=1, affected_by_vulnerable=False,
                                                          is_attack=False, is_orbs=True)
                elif orb == OrbId.FROST:
                    self.add_player_block(2 + focus)
                elif orb == OrbId.DARK:
                    self.orbs[index] = (OrbId.DARK, amount + 6 + focus)

    def evoke_orbs(self, amount: int = 1, times: int = 1):
        focus = self.player.powers.get(PowerId.FOCUS, 0)
        for i in range(amount):
            if len(self.orbs) == 0:
                break
            (orb, orb_value) = self.orbs.pop(0)
            for j in range(times):
                if not [True for m in self.monsters if m.current_hp > 0]:
                    break
                if orb == OrbId.LIGHTNING:
                    if self.player.powers.get(PowerId.ELECTRO):
                        for m in self.monsters:
                            m.inflict_damage(self.player, 8 + focus, 1, vulnerable_modifier=1, is_attack=False,
                                             is_orbs=True)
                    else:
                        self.inflict_random_target_damage(base_damage=8 + focus, hits=1, affected_by_vulnerable=False,
                                                          is_attack=False, is_orbs=True)
                elif orb == OrbId.FROST:
                    self.add_player_block(5 + focus)
                elif orb == OrbId.DARK:
                    target = find_lowest_hp_monster(self.monsters)
                    target.inflict_damage(source=self.player, base_damage=orb_value, hits=1, vulnerable_modifier=1,
                                          is_attack=False, is_orbs=True)
                elif orb == OrbId.PLASMA:
                    self.player.energy += 2
                elif orb == OrbId.INTERNAL_RANDOM_ORB:
                    pass

    def channel_orb(self, orb_id: OrbId, triggered_by_darkness_upgraded: bool = False):

        if orb_id == OrbId.LIGHTNING:
            self.add_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE, 1)
        if orb_id == OrbId.FROST:
            self.add_memory_value(MemoryItem.FROST_THIS_BATTLE, 1)

        focus = self.player.powers.get(PowerId.FOCUS, 0)
        amount = 1 if orb_id is not OrbId.DARK else 6 + focus
        if self.orb_slots > 0:
            self.orbs.append((orb_id, amount))

        if triggered_by_darkness_upgraded:
            for index, (orb, current_amount) in enumerate(self.orbs):
                if orb == OrbId.DARK:
                    self.orbs[index] = (OrbId.DARK, current_amount + 6 + focus)

        while len(self.orbs) > self.orb_slots:
            self.evoke_orbs()

    def add_memory_by_card(self, card_id: CardId, uuid: str, value_to_add: int):
        reset_schedule = next(iter(self.memory_by_card[card_id].keys()))

        if uuid not in self.memory_by_card[card_id][reset_schedule]:
            self.memory_by_card[card_id][reset_schedule] = {uuid: 0}

        self.memory_by_card[card_id][reset_schedule][uuid] += value_to_add

    def get_memory_by_card(self, card_id: CardId, uuid: str) -> int:
        reset_schedule = next(iter(self.memory_by_card[card_id].keys()))

        if uuid not in self.memory_by_card[card_id][reset_schedule]:
            self.memory_by_card[card_id][reset_schedule][uuid] = 0

        return self.memory_by_card[card_id][reset_schedule][uuid]

    def add_memory_value(self, item: MemoryItem, value):
        if item not in self.memory_general:
            self.memory_general[item] = 0

        if item is MemoryItem.TYPE_LAST_PLAYED or \
                item is MemoryItem.STANCE:
            self.memory_general[item] = value
        else:
            self.memory_general[item] += value
            if self.memory_general[item] < 0:
                self.memory_general[item] = 0

    def get_memory_value(self, item: MemoryItem):
        return self.memory_general[item]

    def change_stance(self, new_stance: StanceType):
        current_stance = self.get_stance()

        if current_stance != new_stance:

            # exiting calm
            if current_stance is StanceType.CALM:
                extra_energy = 2 if RelicId.VIOLET_LOTUS not in self.relics else 3
                self.player.energy += extra_energy

            # entering divinity
            if new_stance is StanceType.DIVINITY:
                self.player.energy += 3

            # entering wrath
            if new_stance is StanceType.WRATH:
                if self.player.powers.get(PowerId.RUSHDOWN):
                    self.draw_cards(self.player.powers.get(PowerId.RUSHDOWN, 0))

            # exiting any stance
            self.retrieve_from_discard(CardId.FLURRY_OF_BLOWS, just_one=False)

            if self.player.powers.get(PowerId.MENTAL_FORTRESS):
                self.add_player_block(self.player.powers.get(PowerId.MENTAL_FORTRESS, 0))

            self.add_memory_value(MemoryItem.STANCE, new_stance)

    def get_stance(self) -> StanceType:
        current_stance = self.get_memory_value(MemoryItem.STANCE)
        return current_stance

    def retrieve_from_discard(self, retrieval_target: CardId, just_one=True):
        hand_space = 10 - len(self.hand)
        enough_found = False
        retrieval_list = []
        irrelevant_list = []

        for c in self.discard_pile:
            if c.id == retrieval_target and not len(retrieval_list) == hand_space and not enough_found:
                retrieval_list.append(c)
                if just_one:
                    enough_found = True
            else:
                irrelevant_list.append(c)

        self.hand.extend(retrieval_list)
        self.discard_pile = irrelevant_list.copy()

    def is_new_turn(self) -> bool:
        if self.get_memory_value(MemoryItem.CARDS_THIS_TURN) == 0:
            return True
        else:
            return False

    def is_turn_forced_to_be_over(self) -> bool:
        if len([True for m in self.monsters if m.current_hp > 0]) == 0:
            return True  # all monsters are dead

        # Prep time warp
        time_warp_full = False
        for idx, monster in enumerate(self.monsters):
            if monster.powers.get(PowerId.TIME_WARP, 0) >= 12:
                time_warp_full = True
        return self.relics.get(RelicId.VELVET_CHOKER, 0) >= 6 or time_warp_full or self.player.current_hp <= 0


def is_card_playable(card: CardInterface, player: PlayerInterface, hand: List[CardInterface],
                     draw_pile_count: int) -> bool:
    # unplayable cards like burn, wound, and reflex
    if card.cost == Cost.unplayable:
        return False
    # in general, has enough energy
    if player.energy < card.cost != Cost.x_cost:
        return False
    # entangled case
    if card.type == CardType.ATTACK and player.powers.get(PowerId.ENTANGLED):
        return False
    # special card-specific logic, like clash
    if card.id == CardId.CLASH and len([1 for c in hand if c.type != CardType.ATTACK]):
        return False
    if card.id == CardId.SIGNATURE_MOVE and len(
            [1 for c in hand if c.type is CardType.ATTACK and c.id != CardId.SIGNATURE_MOVE]):
        return False
    if card.id == CardId.GRAND_FINALE and draw_pile_count != 0:
        return False

    return True


def can_card_target_monster(card: CardInterface, monster: MonsterInterface) -> bool:
    if not card.needs_target:
        return False  # should never be reached, but still :shrug:

    if monster.current_hp <= 0:
        return False

    if monster.is_gone:
        return False

    return True
