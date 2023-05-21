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


def limit_break_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if state.player.powers.get(PowerId.STRENGTH):
        state.player.powers[PowerId.STRENGTH] *= 2


def wild_strike_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_pile.append(get_card(CardId.WOUND))


def reckless_charge_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.draw_pile.append(get_card(CardId.DAZED))


def power_through_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    state.add_cards_to_hand(get_card(CardId.WOUND), 2)


def spot_weakness_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 3)


def spot_weakness_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __spot_weakness_post_hook(state, target_index, 4)


def __spot_weakness_post_hook(state: HandStateInterface, target_index: int, amount: int):
    if state.monsters[target_index].hits:
        state.player.add_powers({PowerId.STRENGTH: amount}, state.player.relics)


def reaper_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if hasattr(effect, 'hp_damage'):
        state.player.heal(effect.hp_damage)


def apotheosis_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    for i in range(len(state.draw_pile)):
        c = state.draw_pile[i]
        state.draw_pile[i] = get_card(c.id, upgrade=c.upgrade + 1)


def heel_hook_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.WEAKENED):
            state.player.energy += 1
            state.draw_cards(1)


def storm_of_steel_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.add_cards_to_hand(get_card(CardId.SHIV), amount)


def storm_of_steel_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    amount = len(state.hand)
    for _ in range(amount):
        state.discard_card(state.hand[0])
    state.add_cards_to_hand(get_card(CardId.SHIV, upgrade=1), amount)


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
    if target_index > -1:
        effect.hits = state.attacks_played_this_turn


def catalyst_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.POISON):
            base_poison = state.monsters[target_index].powers.get(PowerId.POISON)
            state.monsters[target_index].add_powers({PowerId.POISON: base_poison}, state.player.relics)


def catalyst_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    if target_index > -1:
        if state.monsters[target_index].powers.get(PowerId.POISON):
            base_poison = state.monsters[target_index].powers.get(PowerId.POISON)
            state.monsters[target_index].add_powers({PowerId.POISON: base_poison * 2}, state.player.relics)


def sword_boomerang_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __sword_boomerang_post_hook(state, 3)


def sword_boomerang_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __sword_boomerang_post_hook(state, 4)


def __sword_boomerang_post_hook(state: HandStateInterface, hits: int):
    state.inflict_random_target_damage(3, hits, True, 1.5, True, 1)


def bouncing_flask_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __bouncing_flask_post_hook(state, 3)


def bouncing_flask_upgraded_post_hook(state: HandStateInterface, effect: CardEffectsInterface, target_index: int = -1):
    __bouncing_flask_post_hook(state, 4)


def __bouncing_flask_post_hook(state: HandStateInterface, hits: int):
    state.add_random_poison(3, hits)
