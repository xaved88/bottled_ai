from typing import List

from rs.calculator.battle_state import BattleState
from rs.calculator.card_cost import Cost
from rs.calculator.cards import Card
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.potion_id import PotionId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.enums.relic_id import RelicId
from rs.calculator.interfaces.card_interface import CardInterface
from rs.calculator.interfaces.potions import Potions
from rs.calculator.interfaces.powers import Powers
from rs.calculator.interfaces.relics import Relics
from rs.calculator.monster import Monster
from rs.calculator.player import Player
from rs.game.card import CardType, Card as GameCard
from rs.helper.logger import log_calculator_missing_relic, log_calculator_missing_power, log_calculator_missing_card, \
    log_calculator_missing_potion
from rs.machine.state import GameState

possible_card_ids = set(item.value for item in CardId)


def make_card(card: GameCard) -> CardInterface:
    card_id = card.id.lower()
    if card_id not in possible_card_ids:
        log_calculator_missing_card(card_id)
        return Card(CardId.FAKE, 0, Cost.unplayable, False, CardType.FAKE)
    return Card(
        card_id=CardId(card.id.lower()),
        upgrade=card.upgrades,
        cost=card.cost,
        needs_target=card.has_target,
        card_type=card.type,
        ethereal=card.ethereal,
        exhausts=card.exhausts,
        uuid=card.uuid,
    )


possible_relic_ids = set(item.value for item in RelicId)


def make_relic_id(relic_id: str) -> RelicId:
    if relic_id not in possible_relic_ids:
        log_calculator_missing_relic(relic_id)
        return RelicId.FAKE
    return RelicId(relic_id)


possible_power_ids = set(item.value for item in PowerId)


def make_power_id(power_id: str) -> PowerId:
    if power_id not in possible_power_ids:
        log_calculator_missing_power(power_id)
        return PowerId.FAKE
    return PowerId(power_id)


possible_potion_ids = set(item.value for item in PotionId)


def make_potion_id(potion_id: str) -> PotionId:
    if potion_id not in possible_potion_ids:
        log_calculator_missing_potion(potion_id)
        return PotionId.FAKE
    return PotionId(potion_id)


def make_powers(powers: List[dict]) -> Powers:
    out = {make_power_id(power['id'].lower()): (power['amount']) for power in powers}

    # custom counters
    echo_form_charge = [p['misc'] for p in powers if p['id'].lower() == "echo form" and 'misc' in p and p['misc'] > 0]
    if len(echo_form_charge):
        out[PowerId.INTERNAL_ECHO_FORM_READY] = echo_form_charge[0]

    return out


def create_battle_state(game_state: GameState) -> BattleState:
    # make sure it's in a usable battle state
    if not game_state.combat_state():
        return None

    cs = game_state.combat_state()

    # get relics
    relics: Relics = {
        make_relic_id(relic['name'].lower()): (relic['counter'])
        for relic in game_state.game_state()['relics']
    }
    # get potions
    potions: Potions = [
        make_potion_id(potion['name'].lower())
        for potion in game_state.game_state()['potions']
    ]

    # get player status
    player = Player(
        is_player=True,
        current_hp=cs['player']['current_hp'],
        max_hp=cs['player']['max_hp'],
        powers=make_powers(cs['player']['powers']),
        block=cs['player']['block'],
        energy=cs['player']['energy'],
        relics=relics,
        potions=potions,
    )

    # get enemies
    monsters = [
        Monster(
            is_player=False,
            current_hp=monster['current_hp'],
            max_hp=monster['max_hp'],
            block=monster['block'],
            powers=make_powers(monster['powers']),
            damage=monster['move_base_damage'] if 'move_base_damage' in monster else 0,
            hits=monster['move_hits'] if 'move_hits' in monster else 0,
            is_gone=False if not monster['is_gone'] else True,
            name=monster['name']
        )
        for monster in cs['monsters']
    ]

    # get cards
    hand = [make_card(card) for card in game_state.hand.cards]
    draw_pile = [make_card(card) for card in game_state.draw_pile.cards]
    discard_pile = [make_card(card) for card in game_state.discard_pile.cards]
    exhaust_pile = [make_card(card) for card in game_state.exhaust_pile.cards]

    # get discard action state
    must_discard = not game_state.screen_state_must_pick_card()

    amount_to_exhaust = game_state.screen_state_exhaust_cards()
    amount_to_discard = game_state.screen_state_discard_cards()
    cards_discarded_this_turn = game_state.get_cards_discarded_this_turn()

    # get orbs
    orbs = [(OrbId(o.value), a) for o, a in game_state.get_player_orbs()]
    orb_slots = game_state.get_player_orb_slots()

    # get custom state
    memory_by_card = game_state.memory_by_card.copy()
    memory_general = game_state.memory_general.copy()

    return BattleState(player, hand, discard_pile, exhaust_pile, draw_pile, monsters, relics, must_discard,
                       amount_to_discard, cards_discarded_this_turn, orbs=orbs, orb_slots=orb_slots,
                       memory_general=memory_general, memory_by_card=memory_by_card, potions=potions,
                       amount_to_exhaust=amount_to_exhaust)


def battlestate_deepcopy(game_state: BattleState) -> BattleState:
    # get relics
    relics: Relics = dict(game_state.relics)

    # get potions
    potions: Potions = list(game_state.potions)

    # get player status
    player = Player(
        is_player=True,
        current_hp=game_state.player.current_hp,
        max_hp=game_state.player.max_hp,
        powers=dict(game_state.player.powers),
        block=game_state.player.block,
        energy=game_state.player.energy,
        relics=relics,
        potions=potions,
    )

    # get enemies
    monsters = [
        Monster(
            is_player=False,
            current_hp=monster.current_hp,
            max_hp=monster.max_hp,
            block=monster.block,
            powers=dict(monster.powers),
            damage=monster.damage,
            hits=monster.hits,
            is_gone=monster.is_gone,
            name=monster.name
        )
        for monster in game_state.monsters
    ]

    # get cards     ## Need to figure out how to deep-copy cards
    hand = [Card(card.id, card.upgrade,
            card.cost, card.needs_target,
            card.type, card.ethereal,
            card.exhausts, card.uuid)
            for card in game_state.hand]

    draw_pile = [Card(card.id, card.upgrade,
            card.cost, card.needs_target,
            card.type, card.ethereal,
            card.exhausts, card.uuid)
            for card in game_state.draw_pile]

    discard_pile = [Card(card.id, card.upgrade,
            card.cost, card.needs_target,
            card.type, card.ethereal,
            card.exhausts, card.uuid)
            for card in game_state.discard_pile]

    exhaust_pile = [Card(card.id, card.upgrade,
            card.cost, card.needs_target,
            card.type, card.ethereal,
            card.exhausts, card.uuid)
            for card in game_state.exhaust_pile]

    # get discard action state
    must_discard = game_state.must_discard

    amount_to_exhaust = game_state.amount_to_exhaust
    amount_to_discard = game_state.amount_to_discard
    cards_discarded_this_turn = game_state.cards_discarded_this_turn

    # get orbs
    orbs = [(OrbId(o.value), a) for o, a in game_state.orbs]
    orb_slots = game_state.orb_slots

    # get custom state
    memory_by_card = {}

    for key, value in game_state.memory_by_card.items():
        for resetKey, val in value.items():
            new_value = {resetKey : val.copy()}
            memory_by_card[key] = new_value


    memory_general = game_state.memory_general.copy()

    #Other battle state items
    total_random_damage_dealt = game_state.total_random_damage_dealt
    total_random_poison_added = game_state.total_random_poison_added
    amount_scryed = game_state.amount_scryed
    saved_block_for_next_turn = game_state.saved_block_for_next_turn

    new_battle_state = BattleState(player, hand, discard_pile, exhaust_pile, draw_pile, monsters, relics, must_discard,
                       amount_to_discard, cards_discarded_this_turn, total_random_damage_dealt, total_random_poison_added,
                       orbs=orbs, orb_slots=orb_slots, memory_general=memory_general, memory_by_card=memory_by_card,
                       amount_scryed = amount_scryed, saved_block_for_next_turn = saved_block_for_next_turn, potions=potions,
                       amount_to_exhaust=amount_to_exhaust)

    new_battle_state.draw_free_early = game_state.draw_free_early
    new_battle_state.draw_free = game_state.draw_free
    new_battle_state.draw_pay_early = game_state.draw_pay_early
    new_battle_state.draw_pay = game_state.draw_pay
    new_battle_state.time_warp_full = game_state.time_warp_full

    return new_battle_state