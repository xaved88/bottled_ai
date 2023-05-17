from typing import Callable

from rs.calculator.cards import get_card, CardId, Card
from rs.calculator.interfaces_for_hooks import CardEffectsInterface, HandStateInterface
from rs.calculator.powers import PowerId
from rs.game.card import CardType

CardEffectCustomHook = Callable[[HandStateInterface, CardEffectsInterface, int], None]
CardEffectCustomHookWithCard = Callable[[Card], None]


def dropkick_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.VULNERABLE):
            state.player.energy += 1
            state.draw_cards(1)


def entrench_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.player.block *= 2


def feed_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __feed_post_hook(state, target_index, 3)


def feed_upgraded_post_hook(state: HandStateInterface, target_index: int = -1):
    __feed_post_hook(state, target_index, 4)


def __feed_post_hook(state: HandStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].current_hp <= 0:
        state.player.max_hp += amount
        state.player.current_hp += amount


def fiend_fire_pre_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    effect.hits = len(state.hand) - 1


def fiend_fire_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    while state.hand:
        state.exhaust_pile.append(state.hand.pop())


def immolate_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.discard_pile.append(get_card(CardId.BURN))


def jax_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] += 2
    else:
        state.player.powers[PowerId.STRENGTH] = 2


def jax_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] += 3
    else:
        state.player.powers[PowerId.STRENGTH] = 3


def limit_break_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] *= 2


def wild_strike_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_pile.append(get_card(CardId.WOUND))


def reckless_charge_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_pile.append(get_card(CardId.DAZED))


def power_through_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    # this is hacky, we should actually have a way of drawing specific cards and overflowing...
    hand_amount = min(2, 10 - len(state.hand))
    discard_amount = 2 - hand_amount
    for i in range(hand_amount):
        state.hand.append(get_card(CardId.WOUND))
    for i in range(discard_amount):
        state.discard_pile.append(get_card(CardId.WOUND))


def spot_weakness_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 3)


def spot_weakness_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 4)


def __spot_weakness_post_hook(state: HandStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].hits:
        if not state.player.powers.get(PowerId.STRENGTH):
            state.player.powers[PowerId.STRENGTH] = 0
        state.player.powers[PowerId.STRENGTH] += amount


def reaper_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if hasattr(effect, 'hp_damage'):
        state.player.heal(effect.hp_damage)


def apotheosis_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    for i in range(len(state.draw_pile)):
        c = state.draw_pile[i]
        state.draw_pile[i] = get_card(c.id, upgrade=c.upgrade + 1)


def blade_dance_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    # this is hacky, we should actually have a way of drawing specific cards and overflowing...
    shiv_amount = 3
    available_shivs = min(shiv_amount, 10 - len(state.hand))
    discarded_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(discarded_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))


def blade_dance_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    # this is hacky, we should actually have a way of drawing specific cards and overflowing...
    shiv_amount = 4
    available_shivs = min(shiv_amount, 10 - len(state.hand))
    discarded_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(discarded_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))


def cloak_and_dagger_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    shiv_amount = 1
    available_shivs = min(shiv_amount, 10 - len(state.hand))
    discarded_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(discarded_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))


def cloak_and_dagger_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface,
                                        target_index: int = -1):
    shiv_amount = 2
    available_shivs = min(shiv_amount, 10 - len(state.hand))
    discarded_shivs = shiv_amount - available_shivs
    for i in range(available_shivs):
        state.hand.append(get_card(CardId.SHIV))
    for i in range(discarded_shivs):
        state.discard_pile.append(get_card(CardId.SHIV))


def heel_hook_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.WEAKENED):
            state.player.energy += 1
            state.draw_cards(1)


def storm_of_steel_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.hand = [get_card(CardId.SHIV) for _ in range(amount)]


def storm_of_steel_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.hand = [get_card(CardId.SHIV, upgrade=1) for _ in range(amount)]


def eviscerate_post_others_discarded_hook(card: Card):
    card.cost = max(0, card.cost - 1)


def sneaky_strike_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.cards_discarded_this_turn:
        state.player.energy += 2


def unload_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    for idx in reversed(range(len(state.hand))):
        if state.hand[idx].type != CardType.ATTACK:
            state.discard_card(state.hand[idx])


def tactician_post_self_discarded_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.player.energy += 1


def tactician_upgraded_post_self_discarded_hook(state: HandStateInterface, effect: CardEffectsInterface,
                                                target_index: int = -1):
    state.player.energy += 2


def reflex_post_self_discarded_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_cards(2)


def reflex_upgraded_post_self_discarded_hook(state: HandStateInterface, effect: CardEffectsInterface,
                                             target_index: int = -1):
    state.draw_cards(3)


def bane_pre_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.POISON):
            effect.hits = 2


def bullet_time_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    for card in state.hand:
        if card.cost != -1:
            card.cost = 0


def finisher_pre_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    effect.hits = state.attacks_played_this_turn
