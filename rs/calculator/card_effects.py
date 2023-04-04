from enum import Enum
from typing import List

from rs.calculator.card_effect_custom_hooks import *
from rs.calculator.cards import Card, CardId
from rs.calculator.powers import Powers, PowerId
from rs.calculator.targets import Player


class TargetType(Enum):
    NONE = 0
    SELF = 1
    MONSTER = 2
    ALL_MONSTERS = 3


class CardEffects:
    def __init__(
            self,
            damage: int = 0,
            hits: int = 0,
            blockable: bool = True,
            block: int = 0,
            target: TargetType = TargetType.SELF,
            applies_powers=None,
            energy_gain: int = 0,
            draw: int = 0,
            pre_hooks: List[CardEffectCustomHook] = None,
            post_hooks: List[CardEffectCustomHook] = None,
            post_others_discarded_hooks: List[CardEffectCustomHookWithCard] = None,
            heal: int = 0,
            amount_to_discard: int = 0,
    ):
        self.damage: int = damage
        self.hits: int = hits
        self.blockable: bool = blockable
        self.block: int = block
        self.target: TargetType = target
        self.applies_powers: Powers = dict() if applies_powers is None else applies_powers
        self.energy_gain: int = energy_gain
        self.draw: int = draw
        self.pre_hooks: List[CardEffectCustomHook] = [] if pre_hooks is None else pre_hooks
        self.post_hooks: List[CardEffectCustomHook] = [] if post_hooks is None else post_hooks
        self.post_others_discarded_hooks: List[
            CardEffectCustomHookWithCard] = [] if post_others_discarded_hooks is None else post_others_discarded_hooks
        self.heal: int = heal
        self.amount_to_discard: int = amount_to_discard


def get_card_effects(card: Card, player: Player, draw_pile: List[Card], discard_pile: List[Card],
                     hand: List[Card]) -> List[CardEffects]:
    if card.id == CardId.STRIKE_R or card.id == CardId.STRIKE_G:
        return [CardEffects(damage=6 if not card.upgrade else 9, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.DEFEND_R or card.id == CardId.DEFEND_G:
        return [CardEffects(block=5 if not card.upgrade else 8, target=TargetType.SELF)]
    if card.id == CardId.BASH:
        return [CardEffects(damage=8 if not card.upgrade else 10, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.VULNERABLE: 2} if not card.upgrade else {PowerId.VULNERABLE: 3})]
    if card.id == CardId.ANGER:
        return [CardEffects(damage=6 if not card.upgrade else 8, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.CLEAVE:
        return [CardEffects(damage=8 if not card.upgrade else 11, hits=1, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.CLOTHESLINE:
        return [CardEffects(damage=12 if not card.upgrade else 14, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.WEAKENED: 2} if not card.upgrade else {PowerId.WEAKENED: 3})]
    if card.id == CardId.HEAVY_BLADE:
        str_bonus = player.powers.get(PowerId.STRENGTH, 0)
        damage = 12 + (str_bonus * 2 if not card.upgrade else str_bonus * 4)
        return [CardEffects(damage=damage, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.IRON_WAVE:
        amount = 5 if not card.upgrade else 7
        return [CardEffects(damage=amount, hits=1, block=amount, target=TargetType.MONSTER)]
    if card.id == CardId.PERFECTED_STRIKE:
        strike_amount = len([1 for c in discard_pile + draw_pile + hand if "strike" in c.id.value])
        damage = 6 + strike_amount * (2 if not card.upgrade else 3)
        return [CardEffects(damage=damage, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.POMMEL_STRIKE:
        return [CardEffects(damage=9 if not card.upgrade else 10, hits=1, draw=1, target=TargetType.MONSTER)]
    if card.id == CardId.SHRUG_IT_OFF:
        return [CardEffects(block=8 if not card.upgrade else 11, draw=1, target=TargetType.SELF)]
    if card.id == CardId.THUNDERCLAP:
        return [CardEffects(damage=4 if not card.upgrade else 6, hits=1, target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.VULNERABLE: 1})]
    if card.id == CardId.TWIN_STRIKE:
        return [CardEffects(damage=5 if not card.upgrade else 7, hits=2, target=TargetType.MONSTER)]
    if card.id == CardId.BLOOD_FOR_BLOOD:
        return [CardEffects(damage=18 if not card.upgrade else 22, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.BLOODLETTING:
        return [CardEffects(energy_gain=2 if not card.upgrade else 3, damage=3, hits=1, blockable=False,
                            target=TargetType.SELF)]
    if card.id == CardId.CARNAGE:
        return [CardEffects(damage=20 if not card.upgrade else 28, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.UPPERCUT:
        powers = {PowerId.WEAKENED: 1, PowerId.VULNERABLE: 1} if not card.upgrade \
            else {PowerId.WEAKENED: 2, PowerId.VULNERABLE: 2}
        return [CardEffects(damage=13, hits=1, target=TargetType.MONSTER, applies_powers=powers)]
    if card.id == CardId.DISARM:
        return [CardEffects(target=TargetType.MONSTER,
                            applies_powers={PowerId.STRENGTH: -2 if not card.upgrade else 3})]
    if card.id == CardId.DROPKICK:
        return [CardEffects(damage=5 if not card.upgrade else 8, hits=1, target=TargetType.MONSTER,
                            post_hooks=[dropkick_post_hook])]
    if card.id == CardId.ENTRENCH:
        return [CardEffects(target=TargetType.SELF, post_hooks=[entrench_post_hook])]
    if card.id == CardId.FLAME_BARRIER:
        return [CardEffects(target=TargetType.SELF, block=12 if not card.upgrade else 16,
                            applies_powers={PowerId.FLAME_BARRIER: 4 if not card.upgrade else 6})]
    if card.id == CardId.GHOSTLY_ARMOR:
        return [CardEffects(target=TargetType.SELF, block=10 if not card.upgrade else 13)]
    if card.id == CardId.HEMOKINESIS:
        return [CardEffects(damage=15 if not card.upgrade else 20, hits=1, target=TargetType.MONSTER),
                CardEffects(damage=2, hits=1, blockable=False, target=TargetType.SELF)]
    if card.id == CardId.INFLAME:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STRENGTH: 2 if not card.upgrade else 3})]
    if card.id == CardId.INTIMIDATE:
        return [CardEffects(target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.WEAKENED: 1 if not card.upgrade else 2})]
    if card.id == CardId.PUMMEL:
        return [CardEffects(damage=2, hits=4 if not card.upgrade else 5, target=TargetType.MONSTER)]
    if card.id == CardId.SEEING_RED:
        return [CardEffects(energy_gain=2, target=TargetType.SELF)]
    if card.id == CardId.SHOCKWAVE:
        amount = 3 if not card.upgrade else 5
        return [CardEffects(target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.WEAKENED: amount, PowerId.VULNERABLE: amount})]
    if card.id == CardId.BLUDGEON:
        return [CardEffects(target=TargetType.MONSTER, damage=32 if not card.upgrade else 42, hits=1)]
    if card.id == CardId.FEED:
        return [CardEffects(target=TargetType.MONSTER, damage=10 if not card.upgrade else 12, hits=1,
                            post_hooks=[feed_post_hook if not card.upgrade else feed_upgraded_post_hook])]
    if card.id == CardId.FIEND_FIRE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            pre_hooks=[fiend_fire_pre_hook], post_hooks=[fiend_fire_post_hook])]
    if card.id == CardId.WOUND:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.IMMOLATE:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=21 if not card.upgrade else 28, hits=1,
                            post_hooks=[immolate_post_hook])]
    if card.id == CardId.BURN:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.DECAY:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.REGRET:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.SHAME:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.CURSE_OF_THE_BELL:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.PARASITE:
        return [CardEffects(target=TargetType.NONE)]

    if card.id == CardId.IMPERVIOUS:
        return [CardEffects(target=TargetType.SELF, block=30 if not card.upgrade else 40)]
    if card.id == CardId.LIMIT_BREAK:
        return [CardEffects(target=TargetType.SELF, post_hooks=[limit_break_post_hook])]
    if card.id == CardId.OFFERING:
        return [CardEffects(target=TargetType.SELF, damage=6, hits=1, blockable=False,
                            draw=3 if not card.upgrade else 5, energy_gain=2)]
    if card.id == CardId.JAX:
        return [CardEffects(target=TargetType.SELF, damage=3, hits=1, blockable=False,
                            post_hooks=[jax_post_hook if not card.upgrade else jax_upgraded_post_hook])]
    if card.id == CardId.BODY_SLAM:
        return [CardEffects(target=TargetType.MONSTER, damage=player.block, hits=1)]
    if card.id == CardId.CLASH:
        return [CardEffects(target=TargetType.MONSTER, damage=14 if not card.upgrade else 18, hits=1)]
    if card.id == CardId.FLEX:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STRENGTH: 2 if not card.upgrade else 4})]
    if card.id == CardId.WILD_STRIKE:
        return [CardEffects(target=TargetType.MONSTER, damage=12 if not card.upgrade else 18, hits=1,
                            post_hooks=[wild_strike_post_hook])]
    if card.id == CardId.BATTLE_TRANCE:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 5),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.NO_DRAW: 1})]
    if card.id == CardId.RAGE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.RAGE: 3 if not card.upgrade else 5})]
    if card.id == CardId.RAMPAGE:
        return [CardEffects(target=TargetType.MONSTER, damage=8, hits=1)]
    if card.id == CardId.METALLICIZE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.METALLICIZE: 3 if not card.upgrade else 4})]
    if card.id == CardId.RECKLESS_CHARGE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            post_hooks=[reckless_charge_post_hook])]
    if card.id == CardId.POWER_THROUGH:
        return [CardEffects(block=15 if not card.upgrade else 20, target=TargetType.SELF,
                            post_hooks=[power_through_post_hook])]
    if card.id == CardId.SPOT_WEAKNESS:
        return [CardEffects(target=TargetType.MONSTER,
                            post_hooks=[
                                spot_weakness_post_hook if not card.upgrade else spot_weakness_upgraded_post_hook])]
    if card.id == CardId.REAPER:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=4 if not card.upgrade else 5, hits=1,
                            post_hooks=[reaper_post_hook])]
    if card.id == CardId.BANDAGE_UP:
        return [CardEffects(target=TargetType.SELF, heal=4 if not card.upgrade else 6)]
    if card.id == CardId.DARK_SHACKLES:
        return [CardEffects(target=TargetType.MONSTER,
                            applies_powers={PowerId.STRENGTH: -9 if not card.upgrade else -15})]
    if card.id == CardId.FLASH_OF_STEEL:
        return [CardEffects(target=TargetType.MONSTER, damage=3 if not card.upgrade else 6, hits=1, draw=1)]
    if card.id == CardId.SWIFT_STRIKE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1, draw=1)]
    if card.id == CardId.TRIP:
        return [CardEffects(target=TargetType.MONSTER if not card.upgrade else TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.VULNERABLE: 2})]
    if card.id == CardId.APOTHEOSIS:
        return [CardEffects(target=TargetType.SELF, post_hooks=[apotheosis_post_hook])]
    if card.id == CardId.HAND_OF_GREED:
        return [CardEffects(target=TargetType.MONSTER, damage=20 if not card.upgrade else 25, hits=1)]
    if card.id == CardId.MASTER_OF_STRATEGY:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 4)]
    if card.id == CardId.APPARITION:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.INTANGIBLE: 1})]

    # silent cards
    if card.id == CardId.NEUTRALIZE:
        return [CardEffects(damage=3 if not card.upgrade else 4, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.WEAKENED: 1} if not card.upgrade else {PowerId.WEAKENED: 2})]
    if card.id == CardId.SHIV:
        shiv_base_dmg = 4 if not card.upgrade else 6
        return [CardEffects(damage=shiv_base_dmg, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.TERROR:
        amount = 99
        return [CardEffects(target=TargetType.MONSTER, applies_powers={PowerId.VULNERABLE: amount})]
    if card.id == CardId.ADRENALINE:
        return [CardEffects(energy_gain=1 if not card.upgrade else 2, draw=2, target=TargetType.SELF)]
    if card.id == CardId.DIE_DIE_DIE:
        return [CardEffects(damage=13 if not card.upgrade else 17, hits=1, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.BLADE_DANCE:
        return [CardEffects(target=TargetType.SELF,
                            post_hooks=[blade_dance_post_hook] if not card.upgrade
                            else [blade_dance_upgraded_post_hook])]
    if card.id == CardId.CLOAK_AND_DAGGER:
        return [CardEffects(block=6, target=TargetType.SELF,
                            post_hooks=[cloak_and_dagger_post_hook] if not card.upgrade
                            else [cloak_and_dagger_upgraded_post_hook])]
    if card.id == CardId.LEG_SWEEP:
        weak_amount = 2 if not card.upgrade else 3
        block_amount = 11 if not card.upgrade else 14
        return [CardEffects(target=TargetType.MONSTER, block=block_amount,
                            applies_powers={PowerId.WEAKENED: weak_amount})]
    if card.id == CardId.SUCKER_PUNCH:
        return [CardEffects(damage=7 if not card.upgrade else 9, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.WEAKENED: 1} if not card.upgrade else {PowerId.WEAKENED: 2})]
    if card.id == CardId.ESCAPE_PLAN:  # Basically we consider block from this to be bonus.
        return [CardEffects(draw=1, target=TargetType.SELF)]
    if card.id == CardId.HEEL_HOOK:
        return [CardEffects(damage=5 if not card.upgrade else 8, hits=1, target=TargetType.MONSTER,
                            post_hooks=[heel_hook_post_hook])]
    if card.id == CardId.DAGGER_SPRAY:
        return [CardEffects(damage=4 if not card.upgrade else 6, hits=2, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.BACKSTAB:
        return [CardEffects(damage=11 if not card.upgrade else 15, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.CALTROPS:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.THORNS: 3 if not card.upgrade else 5})]
    if card.id == CardId.A_THOUSAND_CUTS:
        return [
            CardEffects(target=TargetType.SELF, applies_powers={PowerId.THOUSAND_CUTS: 1 if not card.upgrade else 2})]
    if card.id == CardId.ACCURACY:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.ACCURACY: 4 if not card.upgrade else 6})]
    if card.id == CardId.INFINITE_BLADES:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.INFINITE_BLADES: 1})]
    if card.id == CardId.AFTER_IMAGE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.AFTER_IMAGE: 1})]
    if card.id == CardId.FINESSE:
        return [CardEffects(block=2 if not card.upgrade else 4, draw=1, target=TargetType.SELF)]
    if card.id == CardId.DRAMATIC_ENTRANCE:
        return [CardEffects(damage=8 if not card.upgrade else 12, hits=1, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.SURVIVOR:
        return [CardEffects(block=8 if not card.upgrade else 11, target=TargetType.SELF, amount_to_discard=1)]
    if card.id == CardId.POISONED_STAB:
        return [CardEffects(damage=6 if not card.upgrade else 8, target=TargetType.MONSTER, hits=1,
                            applies_powers={PowerId.POISON: 3 if not card.upgrade else 4})]
    if card.id == CardId.TOOLS_OF_THE_TRADE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.TOOLS_OF_THE_TRADE: 1})]
    if card.id == CardId.STORM_OF_STEEL:
        hook = storm_of_steel_post_hook if not card.upgrade else storm_of_steel_upgraded_post_hook
        return [CardEffects(target=TargetType.SELF, post_hooks=[hook])]
    if card.id == CardId.EVISCERATE:
        return [CardEffects(damage=7 if not card.upgrade else 9, hits=3, target=TargetType.MONSTER,
                            post_others_discarded_hooks=[eviscerate_post_others_discarded_hook])]
    if card.id == CardId.SNEAKY_STRIKE:
        return [CardEffects(damage=12 if not card.upgrade else 16, target=TargetType.MONSTER, hits=1,
                            post_hooks=[sneaky_strike_post_hook])]
    if card.id == CardId.PREPARED:
        amount = 1 if not card.upgrade else 2
        return [CardEffects(target=TargetType.SELF, draw=amount, amount_to_discard=amount)]
    if card.id == CardId.DAGGER_THROW:
        return [CardEffects(damage=9 if not card.upgrade else 12, target=TargetType.MONSTER, hits=1,
                            amount_to_discard=1, draw=1)]
    if card.id == CardId.UNLOAD:
        return [CardEffects(damage=14 if not card.upgrade else 18, target=TargetType.MONSTER, hits=1,
                            post_hooks=[unload_post_hook])]
    if card.id == CardId.FOOTWORK:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DEXTERITY: 2 if not card.upgrade else 3})]
    if card.id == CardId.RIDDLE_WITH_HOLES:
        return [CardEffects(damage=3 if not card.upgrade else 4, hits=5, target=TargetType.MONSTER)]
    if card.id == CardId.DEFLECT:
        return [CardEffects(block=4 if not card.upgrade else 7, target=TargetType.SELF)]
    if card.id == CardId.DASH:
        amount = 10 if not card.upgrade else 13
        return [CardEffects(damage=amount, hits=1, block=amount, target=TargetType.MONSTER)]
    if card.id == CardId.SLICE:
        return [CardEffects(target=TargetType.MONSTER, damage=6 if not card.upgrade else 9, hits=1)]
    if card.id == CardId.QUICK_SLASH:
        return [CardEffects(target=TargetType.MONSTER, damage=8 if not card.upgrade else 12, hits=1, draw=1)]

    return [CardEffects()]
