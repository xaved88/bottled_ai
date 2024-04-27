import math

from rs.calculator.card_cost import Cost
from rs.calculator.cards import get_card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.battle_state_interface import BattleStateInterface
from rs.calculator.interfaces.card_effects_interface import CardEffectsInterface
from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.interfaces.memory_items import MemoryItem
from rs.calculator.util import get_x_trigger_amount
from rs.game.card import CardType


def dropkick_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.VULNERABLE):
            state.player.energy += 1
            state.draw_cards(1)


def entrench_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.add_player_block(state.player.block)


def feed_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                   target_index: int = -1):
    __feed_post_hook(state, target_index, 3)


def feed_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    __feed_post_hook(state, target_index, 4)


def __feed_post_hook(state: BattleStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].current_hp <= 0:
        state.player.max_hp += amount
        state.player.current_hp += amount


def fiend_fire_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    effect.hits = len(state.hand) - 1


def fiend_fire_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    for _ in range(len(state.hand)):
        state.exhaust_card(state.hand[0])


def immolate_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.discard_pile.append(get_card(CardId.BURN))


def limit_break_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] *= 2


def wild_strike_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    state.draw_pile.append(get_card(CardId.WOUND))


def reckless_charge_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                              target_index: int = -1):
    state.draw_pile.append(get_card(CardId.DAZED))


def power_through_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    state.add_cards_to_hand(get_card(CardId.WOUND), 2)


def spot_weakness_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 3)


def spot_weakness_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                     target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 4)


def __spot_weakness_post_hook(state: BattleStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].hits:
        state.player.add_powers({PowerId.STRENGTH: amount}, state.player.relics, state.player.powers)


def reaper_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                     target_index: int = -1):
    if hasattr(effect, 'hp_damage'):
        state.player.heal(effect.hp_damage, True, state.relics)


def apotheosis_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    for i in range(len(state.draw_pile)):
        c = state.draw_pile[i]
        state.draw_pile[i] = get_card(c.id, upgrade=c.upgrade + 1)


def heel_hook_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.WEAKENED):
            state.player.energy += 1
            state.draw_cards(1)


def storm_of_steel_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.add_cards_to_hand(get_card(CardId.SHIV), amount)


def storm_of_steel_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                      target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.add_cards_to_hand(get_card(CardId.SHIV, upgrade=1), amount)


def eviscerate_post_others_discarded_hook(card: CardInterface):
    card.cost = max(0, card.cost - 1)


def sneaky_strike_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    if state.cards_discarded_this_turn:
        state.player.energy += 2


def unload_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                     target_index: int = -1):
    for idx in reversed(range(len(state.hand))):
        if state.hand[idx].type != CardType.ATTACK:
            state.discard_card(state.hand[idx])


def tactician_post_self_discarded_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                       target_index: int = -1):
    state.player.energy += 1


def tactician_upgraded_post_self_discarded_hook(state: BattleStateInterface, effect: CardEffectsInterface,
                                                card: CardInterface, target_index: int = -1):
    state.player.energy += 2


def reflex_post_self_discarded_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                    target_index: int = -1):
    state.draw_cards(2)


def reflex_upgraded_post_self_discarded_hook(state: BattleStateInterface, effect: CardEffectsInterface,
                                             card: CardInterface, target_index: int = -1):
    state.draw_cards(3)


def bane_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                  target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.POISON):
            effect.hits = 2


def bullet_time_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    for card in state.hand:
        if card.cost != Cost.unplayable:
            card.cost = 0


def catalyst_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.POISON):
            base_poison = state.monsters[target_index].powers.get(PowerId.POISON)
            state.monsters[target_index].add_powers({PowerId.POISON: base_poison}, state.player.relics,
                                                    state.player.powers)


def catalyst_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.POISON):
            base_poison = state.monsters[target_index].powers.get(PowerId.POISON)
            state.monsters[target_index].add_powers({PowerId.POISON: base_poison * 2}, state.player.relics,
                                                    state.player.powers)


def sword_boomerang_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                              target_index: int = -1):
    __sword_boomerang_post_hook(state, 3)


def sword_boomerang_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                       target_index: int = -1):
    __sword_boomerang_post_hook(state, 4)


def __sword_boomerang_post_hook(state: BattleStateInterface, hits: int):
    state.inflict_random_target_damage(3, hits)


def bouncing_flask_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    __bouncing_flask_post_hook(state, 3)


def bouncing_flask_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                      target_index: int = -1):
    __bouncing_flask_post_hook(state, 4)


def __bouncing_flask_post_hook(state: BattleStateInterface, hits: int):
    state.add_random_poison(3, hits)


def deep_breath_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    state.draw_pile.extend(state.discard_pile)
    state.discard_pile.clear()


def enlightenment_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    for card in state.hand:
        if card.cost >= 2:
            card.cost = 1


def impatience_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    attacks_in_hand = len([True for c in state.hand if c.type == CardType.ATTACK])
    if attacks_in_hand == 0:
        state.draw_cards(2)


def impatience_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                  target_index: int = -1):
    attacks_in_hand = len([True for c in state.hand if c.type == CardType.ATTACK])
    if attacks_in_hand == 0:
        state.draw_cards(3)


def rip_and_tear_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    __rip_and_tear_post_hook(state, 7)


def rip_and_tear_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                    target_index: int = -1):
    __rip_and_tear_post_hook(state, 9)


def __rip_and_tear_post_hook(state: BattleStateInterface, damage: int):
    state.inflict_random_target_damage(damage, 2)


def stack_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                   target_index: int = -1):
    block = len(state.discard_pile)
    state.add_player_block(block)


def stack_upgraded_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    block = len(state.discard_pile) + 3
    state.add_player_block(block)


def mind_blast_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    effect.damage = len(state.draw_pile)


def auto_shields_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    __auto_shields_post_hook(state, 11)


def auto_shields_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                    target_index: int = -1):
    __auto_shields_post_hook(state, 15)


def __auto_shields_post_hook(state: BattleStateInterface, block: int):
    if state.player.block == 0:
        state.add_player_block(block)


def turbo_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                    target_index: int = -1):
    state.discard_pile.append(get_card(CardId.VOID))


def aggregate_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    __aggregate_post_hook(state, 4)


def aggregate_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                 target_index: int = -1):
    __aggregate_post_hook(state, 3)


def __aggregate_post_hook(state: BattleStateInterface, divide_by_this: int):
    energy_gain = math.floor(len(state.draw_pile) / divide_by_this)
    state.player.energy += energy_gain


def double_energy_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    state.player.energy *= 2


def overclock_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    state.discard_pile.append(get_card(CardId.BURN))


def electrodynamics_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    state.player.add_powers({PowerId.ELECTRO: 1}, state.player.relics, state.player.powers)


def dualcast_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.evoke_orbs(1, 2)


def multicast_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    state.evoke_orbs(1, get_x_trigger_amount(state.player) + min(card.upgrade, 1))


def capacitor_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    state.orb_slots += 2
    state.orb_slots = min(state.orb_slots, 10)


def capacitor_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                 target_index: int = -1):
    state.orb_slots += 3
    state.orb_slots = min(state.orb_slots, 10)


def consume_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    amount_of_orbs = len(state.orbs)
    state.orb_slots -= 1
    if amount_of_orbs > state.orb_slots:
        state.orbs.pop()


def chill_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                    target_index: int = -1):
    for i in range(len(state.monsters)):
        state.channel_orb(OrbId.FROST)


def barrage_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                     target_index: int = -1):
    effect.hits = len(state.orbs)


def fission_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    amount = len(state.orbs)
    state.orbs.clear()
    state.player.energy += amount
    state.draw_cards(amount)


def fission_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                               target_index: int = -1):
    amount = len(state.orbs)
    state.evoke_orbs(amount, 1)
    state.player.energy += amount
    state.draw_cards(amount)


def reboot_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                     target_index: int = -1):
    __reboot_post_hook(state, 4)


def reboot_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                              target_index: int = -1):
    __reboot_post_hook(state, 6)


def __reboot_post_hook(state: BattleStateInterface, amount_to_draw: int):
    # Shuffling into the opposite pile as what the card says to use existing functionality around reshuffling the draw pile
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.discard_pile.extend(state.draw_pile)
    state.draw_pile.clear()
    state.draw_cards(amount_to_draw)


def sunder_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                     target_index: int = -1):
    if state.monsters[target_index].current_hp <= 0:
        state.player.energy += 3


def recursion_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    orb = state.orbs[0][0]
    state.evoke_orbs(1, 1)
    state.channel_orb(orb)


def melter_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                    target_index: int = -1):
    state.monsters[target_index].block = 0


def calculated_gamble_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.draw_cards(amount)


def compile_driver_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    unique_orbs = set()
    for (orb_id, v) in state.orbs:
        unique_orbs.add(orb_id)
    amount = len(unique_orbs)
    state.draw_cards(amount)


def go_for_the_eyes_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                              target_index: int = -1):
    __go_for_the_eyes_post_hook(state, target_index, 1)


def go_for_the_eyes_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                       target_index: int = -1):
    __go_for_the_eyes_post_hook(state, target_index, 2)


def __go_for_the_eyes_post_hook(state: BattleStateInterface, target_index: int, weak_counts: int):
    if state.monsters[target_index].hits:
        state.monsters[target_index].add_powers({PowerId.WEAKENED: weak_counts}, state.player.relics,
                                                state.player.powers)


def darkness_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.channel_orb(OrbId.DARK)


def darkness_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    state.channel_orb(OrbId.DARK, triggered_by_darkness_upgraded=True)


def all_for_one_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    hand_space = 10 - len(state.hand) + 1  # +1 because we didn't dispose of All For One yet
    discard_length = len(state.discard_pile)
    discard_index = 0

    discard_pile_working_copy = state.discard_pile.copy()
    discard_pile_working_copy.reverse()

    for _ in range(discard_length):
        if hand_space < 1:
            break
        card = discard_pile_working_copy[discard_index]
        if card.cost == 0:
            del discard_pile_working_copy[discard_index]
            state.hand.append(get_card(card.id))
            hand_space -= 1
        else:
            discard_index += 1

    discard_pile_working_copy.reverse()
    state.discard_pile = discard_pile_working_copy.copy()


def decay_end_turn_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    state.player.inflict_damage(state.player, 2, 1, vulnerable_modifier=1, is_attack=False)


def doubt_end_turn_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    state.player.add_powers({PowerId.WEAKENED: 1}, state.player.relics, state.player.powers)


def shame_end_turn_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    state.player.add_powers({PowerId.FRAIL: 1}, state.player.relics, state.player.powers)


def burn_end_turn_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.player.inflict_damage(state.player, 2, 1, vulnerable_modifier=1, is_attack=False)


def burn_upgraded_end_turn_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    state.player.inflict_damage(state.player, 4, 1, vulnerable_modifier=1, is_attack=False)


def regret_end_turn_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    state.player.inflict_damage(state.player, len(state.hand), 1, vulnerable_modifier=1, is_attack=False)
    # this will probably be off by 1 if there are 2 regrets since ingame they'd be handled one by one


def bowling_bash_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    effect.hits = len(state.monsters)


def conclude_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.end_turn()


def ragnarok_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    __ragnarok_post_hook(state, 5)


def ragnarok_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    __ragnarok_post_hook(state, 6)


def __ragnarok_post_hook(state: BattleStateInterface, damage_and_hits: int):
    state.inflict_random_target_damage(damage_and_hits, damage_and_hits)


def sever_soul_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    cards_to_exhaust = []
    cards_to_keep = []

    for c in state.hand:
        if c.type != CardType.ATTACK:
            cards_to_exhaust.append(c)
        else:
            cards_to_keep.append(c)

    for c in cards_to_exhaust:
        state.exhaust_card(c, handle_remove=False)

    state.hand = cards_to_keep.copy()


def second_wind_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    __second_wind_post_hook(state, 5)


def second_wind_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                   target_index: int = -1):
    __second_wind_post_hook(state, 7)


def __second_wind_post_hook(state: BattleStateInterface, block: int):
    cards_to_exhaust = []
    cards_to_keep = []

    for c in state.hand:
        if c.type != CardType.ATTACK:
            cards_to_exhaust.append(c)
        else:
            cards_to_keep.append(c)

    times_to_gain_block = len(cards_to_exhaust)

    for c in cards_to_exhaust:
        state.exhaust_card(c, handle_remove=False)
    for i in range(times_to_gain_block):
        state.add_player_block(block)

    state.hand = cards_to_keep.copy()


def ritual_dagger_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    effect.damage = 15 + state.get_memory_by_card(card.id, card.uuid)


def ritual_dagger_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    if state.monsters[target_index].current_hp <= 0 and not state.monsters[target_index].powers.get(PowerId.MINION):
        extra_damage = 3 if not card.upgrade else 5
        state.add_memory_by_card(card.id, card.uuid, extra_damage)


def finisher_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    effect.hits = state.get_memory_value(MemoryItem.ATTACKS_THIS_TURN)


def claw_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                  target_index: int = -1):
    base_damage = 3 if not card.upgrade else 5
    effect.damage = base_damage + (2 * state.get_memory_value(MemoryItem.CLAWS_THIS_BATTLE))


def claw_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                   target_index: int = -1):
    state.add_memory_value(MemoryItem.CLAWS_THIS_BATTLE, 1)


def genetic_algorithm_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                               target_index: int = -1):
    effect.block = 1 + state.get_memory_by_card(card.id, card.uuid)


def genetic_algorithm_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    extra_block = 2 if not card.upgrade else 3
    state.add_memory_by_card(card.id, card.uuid, extra_block)


def steam_barrier_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    base_block = 6 if not card.upgrade else 8
    effect.block = base_block - state.get_memory_by_card(card.id, card.uuid)


def steam_barrier_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    state.add_memory_by_card(card.id, card.uuid, 1)


def glass_knife_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    base_damage = 8 if not card.upgrade else 12
    effect.damage = base_damage - state.get_memory_by_card(card.id, card.uuid)


def glass_knife_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    state.add_memory_by_card(card.id, card.uuid, 2)


def streamline_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    card.cost -= 1
    if card.cost < 0:
        card.cost = 0


def ftl_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                 target_index: int = -1):
    threshold = 3 if not card.upgrade else 4
    if state.get_memory_value(MemoryItem.CARDS_THIS_TURN) < threshold:
        state.draw_cards(1)


def rampage_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                     target_index: int = -1):
    effect.damage = 8 + state.get_memory_by_card(card.id, card.uuid)


def rampage_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    extra_damage = 5 if not card.upgrade else 8
    state.add_memory_by_card(card.id, card.uuid, extra_damage)


def blizzard_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    effect.damage = 2 * state.get_memory_value(MemoryItem.FROST_THIS_BATTLE)


def thunder_strike_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    damage = 7 if not card.upgrade else 9

    cracked_core_relic = 0 if RelicId.CRACKED_CORE not in state.relics else 1
    hits = state.get_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE) + cracked_core_relic

    state.inflict_random_target_damage(damage, hits)
