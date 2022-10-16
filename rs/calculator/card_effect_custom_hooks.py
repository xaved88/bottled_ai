from typing import Callable

from rs.calculator.cards import get_card, CardId
from rs.calculator.interfaces_for_hooks import CardEffectsInterface, HandStateInterface
from rs.calculator.powers import PowerId

CardEffectCustomHook = Callable[[HandStateInterface, CardEffectsInterface, int], None]


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
