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
from rs.calculator.interfaces.memory_items import MemoryItem, StanceType
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
    amount = 3 if not card.upgrade else 4
    alive_monsters = len([True for m in state.monsters if m.current_hp > 0])
    life_link_more_alive = state.monsters[target_index].powers.get(PowerId.LIFE_LINK) and alive_monsters > 0

    if state.monsters[target_index].current_hp <= 0 and not \
            state.monsters[target_index].powers.get(PowerId.MINION) and not \
            life_link_more_alive:
        state.player.max_hp += amount
        state.player.current_hp += amount


def fiend_fire_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    effect.hits = len(state.hand) - 1


def fiend_fire_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    for _ in range(len(state.hand)):
        state.exhaust_card(state.hand[0])


def limit_break_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] *= 2


def spot_weakness_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    amount = 3 if not card.upgrade else 4
    if state.monsters[target_index].hits and state.monsters[target_index].damage != -1:
        state.player.add_powers({PowerId.STRENGTH: amount}, state.player.relics, state.player.powers)


def apotheosis_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                         target_index: int = -1):
    for pile in [state.hand, state.draw_pile, state.discard_pile, state.exhaust_pile]:
        for c in pile:
            if not c.id == CardId.BURN:
                c.upgrade += 1


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
    state.spawn_in_hand(get_card(CardId.SHIV), amount)


def storm_of_steel_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                      target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.spawn_in_hand(get_card(CardId.SHIV, upgrade=1), amount)


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


def bouncing_flask_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    hits = 3 if not card.upgrade else 4
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
    draw = 2 if not card.upgrade else 3
    if attacks_in_hand == 0:
        state.draw_cards(draw)


def stack_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                   target_index: int = -1):
    basic_block = 0 if not card.upgrade else 3
    block = len(state.discard_pile) + basic_block
    effect.block = block


def mind_blast_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    effect.damage = len(state.draw_pile)


def auto_shields_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    block = 11 if not card.upgrade else 15
    if state.player.block == 0:
        effect.block = block


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
    amount_to_draw = 4 if not card.upgrade else 6

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
    amount = 1 if not card.upgrade else 2
    if state.monsters[target_index].hits and state.monsters[target_index].damage != -1:
        state.monsters[target_index].add_powers({PowerId.WEAKENED: amount}, state.player.relics,
                                                state.player.powers)


def darkness_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.channel_orb(OrbId.DARK)


def darkness_upgraded_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                                target_index: int = -1):
    state.channel_orb(OrbId.DARK, triggered_by_darkness_upgraded=True)


def all_for_one_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    hand_space = 10 - len(state.hand)
    retrieval_list = []
    irrelevant_list = []

    for c in state.discard_pile:
        if c.cost == 0 and not len(retrieval_list) == hand_space:
            retrieval_list.append(c)
        else:
            irrelevant_list.append(c)

    state.hand.extend(retrieval_list)
    state.discard_pile = irrelevant_list.copy()


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
    state.player.inflict_damage(state.player, len(state.hand), 1, blockable=False, vulnerable_modifier=1,
                                is_attack=False)
    # this will probably be off by 1 if there are 2 regrets since ingame they'd be handled one by one


def bowling_bash_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    effect.hits = len([True for m in state.monsters if m.current_hp > 0])


def conclude_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    state.end_turn()


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
    cards_to_exhaust = []
    cards_to_keep = []
    block = 5 if not card.upgrade else 7

    for c in state.hand:
        if c.type != CardType.ATTACK:
            cards_to_exhaust.append(c)
        else:
            cards_to_keep.append(c)

    times_to_gain_block = len(cards_to_exhaust)

    for c in cards_to_exhaust:
        state.exhaust_card(c, handle_remove=False)
    for i in range(times_to_gain_block):
        state.add_player_block(block + state.player.powers.get(PowerId.DEXTERITY, 0))

    state.hand = cards_to_keep.copy()


def ritual_dagger_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    effect.damage = 15 + state.get_memory_by_card(card.id, card.uuid)


def ritual_dagger_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                            target_index: int = -1):
    alive_monsters = len([True for m in state.monsters if m.current_hp > 0])
    life_link_more_alive = state.monsters[target_index].powers.get(PowerId.LIFE_LINK) and alive_monsters > 0

    if state.monsters[target_index].current_hp <= 0 and not \
            state.monsters[target_index].powers.get(PowerId.MINION) and not \
            life_link_more_alive:
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
    cracked_core_relic = 0 if RelicId.CRACKED_CORE not in state.relics else 1
    effect.hits = state.get_memory_value(MemoryItem.LIGHTNING_THIS_BATTLE) + cracked_core_relic


def judgement_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    hp_threshold = 30 if not card.upgrade else 40
    if state.monsters[target_index].current_hp <= hp_threshold:
        state.monsters[target_index].current_hp = 0


def crush_joints_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    amount = 1 if not card.upgrade else 2
    if state.get_memory_value(MemoryItem.TYPE_LAST_PLAYED) is CardType.SKILL:
        effect.applies_powers.update({PowerId.VULNERABLE: amount})


def sash_whip_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    amount = 1 if not card.upgrade else 2
    if state.get_memory_value(MemoryItem.TYPE_LAST_PLAYED) is CardType.ATTACK:
        effect.applies_powers.update({PowerId.WEAKENED: amount})


def follow_up_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                       target_index: int = -1):
    if state.get_memory_value(MemoryItem.TYPE_LAST_PLAYED) is CardType.ATTACK:
        state.player.energy += 1


def sanctity_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    if state.get_memory_value(MemoryItem.TYPE_LAST_PLAYED) is CardType.SKILL:
        effect.draw = 2


def tantrum_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    card_to_add = get_card(CardId.TANTRUM)
    card_to_add.upgrade = card.upgrade
    state.draw_pile.append(card_to_add)
    # the special removal of this card is handled in battle_state


def inner_peace_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    if state.get_stance() == StanceType.CALM:
        amount_to_draw = 3 if not card.upgrade else 4
        state.draw_cards(amount_to_draw)
    else:
        effect.sets_stance = StanceType.CALM


def indignation_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    if state.get_stance() == StanceType.WRATH:
        amount_to_add = 3 if not card.upgrade else 5
        for m in state.monsters:
            m.add_powers({PowerId.VULNERABLE: amount_to_add}, state.relics, state.player.powers)
    else:
        effect.sets_stance = StanceType.WRATH


def fear_no_evil_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    if state.monsters[target_index].hits and state.monsters[target_index].damage != -1:
        state.change_stance(StanceType.CALM)


def halt_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                  target_index: int = -1):
    if state.get_stance() is StanceType.WRATH:
        amount = 9 if not card.upgrade else 14
        effect.block += amount


def perseverance_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                          target_index: int = -1):
    base_block = 5 if not card.upgrade else 7
    effect.block = base_block + state.get_memory_by_card(card.id, card.uuid)


def spirit_shield_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                           target_index: int = -1):
    multiplier = 3 if not card.upgrade else 4
    amount_of_block = (len(state.hand) - 1) * multiplier  # -1 because spirit shield is currently still in hand
    effect.block = amount_of_block


def windmill_strike_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    base_damage = 7 if not card.upgrade else 10
    effect.damage = base_damage + state.get_memory_by_card(card.id, card.uuid)


def pressure_points_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                              target_index: int = -1):
    for monster in state.monsters:
        if PowerId.MARK in monster.powers:
            monster.inflict_damage(monster, monster.powers.get(PowerId.MARK, 0), 1, blockable=False,
                                   vulnerable_modifier=1,
                                   is_attack=False)


def brilliance_pre_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                        target_index: int = -1):
    base_damage = 12 if not card.upgrade else 16
    effect.damage = base_damage + state.get_memory_value(MemoryItem.MANTRA_THIS_BATTLE)


def lesson_learned_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                             target_index: int = -1):
    alive_monsters = len([True for m in state.monsters if m.current_hp > 0])
    life_link_more_alive = state.monsters[target_index].powers.get(PowerId.LIFE_LINK) and alive_monsters > 0

    if state.monsters[target_index].current_hp <= 0 and not \
            state.monsters[target_index].powers.get(PowerId.MINION) and not \
            life_link_more_alive:
        state.add_memory_value(MemoryItem.KILLED_WITH_LESSON_LEARNED, 1)


def panache_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    power_amount = 10 if not card.upgrade else 14
    state.add_memory_value(MemoryItem.PANACHE_DAMAGE, power_amount)

def recycle_post_hook(state: BattleStateInterface, effect: CardEffectsInterface, card: CardInterface,
                      target_index: int = -1):
    state.add_memory_value(MemoryItem.RECYCLE, 1)
