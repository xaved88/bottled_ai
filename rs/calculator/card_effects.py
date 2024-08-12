from typing import List

from rs.calculator.card_effect_custom_hooks import *
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.card_effect_hooks_interface import CardEffectCustomHook, CardEffectCustomHookWithCard
from rs.calculator.interfaces.card_effects_interface import CardEffectsInterface, TargetType
from rs.calculator.interfaces.memory_items import StanceType
from rs.calculator.interfaces.player import PlayerInterface
from rs.calculator.interfaces.powers import Powers
from rs.calculator.util import get_x_trigger_amount


class CardEffects(CardEffectsInterface):
    def __init__(
            self,
            damage: int = 0,
            hits: int = 0,
            blockable: bool = True,
            block: int = 0,
            block_times: int = 1,
            target: TargetType = TargetType.SELF,
            applies_powers=None,
            energy_gain: int = 0,
            draw: int = 0,
            pre_hooks: List[CardEffectCustomHook] = None,
            post_hooks: List[CardEffectCustomHook] = None,
            post_others_discarded_hooks: List[CardEffectCustomHookWithCard] = None,
            post_self_discarded_hooks: List[CardEffectCustomHook] = None,
            end_turn_hooks: List[CardEffectCustomHook] = None,
            heal: int = 0,
            amount_to_discard: int = 0,
            amount_to_exhaust: int = 0,
            spawn_cards_in_hand: [CardInterface, int] = None,
            spawn_cards_in_draw: [CardInterface, int] = None,
            spawn_cards_in_discard: [CardInterface, int] = None,
            channel_orbs: List[OrbId] = None,
            retains: bool = False,
            sets_stance: StanceType = None,
            amount_to_scry: int = 0
    ):
        self.damage: int = damage
        self.hits: int = hits
        self.blockable: bool = blockable
        self.block: int = block
        self.block_times: int = block_times
        self.target: TargetType = target
        self.applies_powers: Powers = dict() if applies_powers is None else applies_powers
        self.energy_gain: int = energy_gain
        self.draw: int = draw
        self.pre_hooks: List[CardEffectCustomHook] = [] if pre_hooks is None else pre_hooks
        self.post_hooks: List[CardEffectCustomHook] = [] if post_hooks is None else post_hooks
        self.post_others_discarded_hooks: List[
            CardEffectCustomHookWithCard] = [] if post_others_discarded_hooks is None else post_others_discarded_hooks
        self.post_self_discarded_hooks: List[
            CardEffectCustomHook] = [] if post_self_discarded_hooks is None else post_self_discarded_hooks
        self.end_turn_hooks: List[
            CardEffectCustomHook] = [] if end_turn_hooks is None else end_turn_hooks
        self.heal: int = heal
        self.amount_to_discard: int = amount_to_discard
        self.amount_to_exhaust: int = amount_to_exhaust
        self.spawn_cards_in_hand: [CardInterface, int] = spawn_cards_in_hand
        self.spawn_cards_in_draw: [CardInterface, int] = spawn_cards_in_draw
        self.spawn_cards_in_discard: [CardInterface, int] = spawn_cards_in_discard
        self.channel_orbs: List[OrbId] = [] if channel_orbs is None else channel_orbs
        self.retains: bool = retains
        self.sets_stance: StanceType = sets_stance
        self.amount_to_scry: int = amount_to_scry


def get_card_effects(card: CardInterface, player: PlayerInterface, draw_pile: List[CardInterface],
                     discard_pile: List[CardInterface], hand: List[CardInterface]) -> List[CardEffectsInterface]:
    if card.id == CardId.STRIKE_R or card.id == CardId.STRIKE_G \
            or card.id == CardId.STRIKE_B or card.id == CardId.STRIKE_P:
        return [CardEffects(damage=6 if not card.upgrade else 9, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.DEFEND_R or card.id == CardId.DEFEND_G \
            or card.id == CardId.DEFEND_B or card.id == CardId.DEFEND_P:
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
    if card.id == CardId.WHIRLWIND:
        base_damage = 5 if not card.upgrade else 8
        return [CardEffects(damage=base_damage, hits=get_x_trigger_amount(player), target=TargetType.ALL_MONSTERS)]
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
    if card.id == CardId.FIRE_BREATHING:
        return [
            CardEffects(target=TargetType.SELF, applies_powers={PowerId.FIRE_BREATHING: 6 if not card.upgrade else 10})]
    if card.id == CardId.EVOLVE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.EVOLVE: 1 if not card.upgrade else 2})]
    if card.id == CardId.DEMON_FORM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DEMON_FORM: 2 if not card.upgrade else 3})]
    if card.id == CardId.BERSERK:
        return [CardEffects(target=TargetType.SELF,
                            applies_powers={PowerId.VULNERABLE: 2 if not card.upgrade else 1, PowerId.BERSERK: 1})]
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
                            post_hooks=[feed_post_hook])]
    if card.id == CardId.FIEND_FIRE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            pre_hooks=[fiend_fire_pre_hook], post_hooks=[fiend_fire_post_hook])]
    if card.id == CardId.WOUND:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.VOID:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.IMMOLATE:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=21 if not card.upgrade else 28, hits=1,
                            spawn_cards_in_discard=(get_card(CardId.BURN), 1))]
    if card.id == CardId.BURN:
        hook = burn_end_turn_hook if not card.upgrade else burn_upgraded_end_turn_hook
        return [CardEffects(target=TargetType.NONE, end_turn_hooks=[hook])]
    if card.id == CardId.SLIMED:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.DECAY:
        return [CardEffects(target=TargetType.NONE, end_turn_hooks=[decay_end_turn_hook])]
    if card.id == CardId.REGRET:
        return [CardEffects(target=TargetType.NONE, end_turn_hooks=[regret_end_turn_hook])]
    if card.id == CardId.SHAME:
        return [CardEffects(target=TargetType.NONE, end_turn_hooks=[shame_end_turn_hook])]
    if card.id == CardId.DOUBT:
        return [CardEffects(target=TargetType.NONE, end_turn_hooks=[doubt_end_turn_hook])]
    if card.id == CardId.CURSE_OF_THE_BELL:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.NECRONOMICURSE:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.PARASITE:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.INJURY:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.CLUMSY:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.ASCENDERS_BANE:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.NORMALITY:
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
                            applies_powers={PowerId.STRENGTH: 2 if not card.upgrade else 3})]
    if card.id == CardId.BODY_SLAM:
        return [CardEffects(target=TargetType.MONSTER, damage=player.block, hits=1)]
    if card.id == CardId.CLASH:
        return [CardEffects(target=TargetType.MONSTER, damage=14 if not card.upgrade else 18, hits=1)]
    if card.id == CardId.FLEX:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STRENGTH: 2 if not card.upgrade else 4})]
    if card.id == CardId.WILD_STRIKE:
        return [CardEffects(target=TargetType.MONSTER, damage=12 if not card.upgrade else 18, hits=1,
                            spawn_cards_in_draw=(get_card(CardId.WOUND), 1))]
    if card.id == CardId.BATTLE_TRANCE:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 5),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.NO_DRAW: 1})]
    if card.id == CardId.RAGE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.RAGE: 3 if not card.upgrade else 5})]
    if card.id == CardId.RAMPAGE:
        return [CardEffects(target=TargetType.MONSTER, damage=8, hits=1, pre_hooks=[rampage_pre_hook],
                            post_hooks=[rampage_post_hook])]
    if card.id == CardId.SWORD_BOOMERANG:
        hits = 3 if not card.upgrade else 4
        return [CardEffects(target=TargetType.RANDOM, hits=hits, damage=3)]
    if card.id == CardId.JUGGERNAUT:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.JUGGERNAUT: 5 if not card.upgrade else 7})]
    if card.id == CardId.METALLICIZE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.METALLICIZE: 3 if not card.upgrade else 4})]
    if card.id == CardId.RECKLESS_CHARGE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            spawn_cards_in_draw=(get_card(CardId.DAZED), 1))]
    if card.id == CardId.POWER_THROUGH:
        return [CardEffects(block=15 if not card.upgrade else 20, target=TargetType.SELF,
                            spawn_cards_in_hand=(get_card(CardId.WOUND), 2))]
    if card.id == CardId.SPOT_WEAKNESS:
        return [CardEffects(target=TargetType.MONSTER, post_hooks=[spot_weakness_post_hook])]
    if card.id == CardId.REAPER:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=4 if not card.upgrade else 5, hits=1)]
    if card.id == CardId.BANDAGE_UP:
        return [CardEffects(target=TargetType.SELF, heal=4 if not card.upgrade else 6)]
    if card.id == CardId.BITE:
        return [CardEffects(damage=7 if not card.upgrade else 8, hits=1, target=TargetType.MONSTER),
                CardEffects(heal=2 if not card.upgrade else 3, target=TargetType.SELF)]
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
    if card.id == CardId.BLIND:
        return [CardEffects(target=TargetType.MONSTER if not card.upgrade else TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.WEAKENED: 2})]
    if card.id == CardId.APOTHEOSIS:
        return [CardEffects(target=TargetType.SELF, post_hooks=[apotheosis_post_hook])]
    if card.id == CardId.HAND_OF_GREED:
        return [CardEffects(target=TargetType.MONSTER, damage=20 if not card.upgrade else 25, hits=1)]
    if card.id == CardId.MASTER_OF_STRATEGY:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 4)]
    if card.id == CardId.APPARITION:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.INTANGIBLE_PLAYER: 1})]
    if card.id == CardId.DEEP_BREATH:
        return [
            CardEffects(target=TargetType.SELF, draw=1 if not card.upgrade else 2, pre_hooks=[deep_breath_pre_hook])]
    if card.id == CardId.ENLIGHTENMENT:
        return [CardEffects(target=TargetType.SELF, post_hooks=[enlightenment_post_hook])]
    if card.id == CardId.IMPATIENCE:
        return [CardEffects(target=TargetType.SELF, post_hooks=[impatience_post_hook])]
    if card.id == CardId.MAYHEM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MAYHEM: 1})]
    if card.id == CardId.PANACHE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.PANACHE_INTERNAL: 1},
                            post_hooks=[panache_post_hook])]
    if card.id == CardId.SADISTIC_NATURE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.SADISTIC: 5 if not card.upgrade else 7})]

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
        amount = 3 if not card.upgrade else 4
        return [CardEffects(target=TargetType.SELF, spawn_cards_in_hand=(get_card(CardId.SHIV), amount))]
    if card.id == CardId.CLOAK_AND_DAGGER:
        amount = 1 if not card.upgrade else 2
        return [CardEffects(block=6, target=TargetType.SELF, spawn_cards_in_hand=(get_card(CardId.SHIV), amount))]
    if card.id == CardId.LEG_SWEEP:
        weak_amount = 2 if not card.upgrade else 3
        block_amount = 11 if not card.upgrade else 14
        return [
            CardEffects(target=TargetType.MONSTER, applies_powers={PowerId.WEAKENED: weak_amount}),
            CardEffects(target=TargetType.SELF, block=block_amount)]
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
    if card.id == CardId.CRIPPLING_CLOUD:
        return [CardEffects(target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.POISON: 4 if not card.upgrade else 7, PowerId.WEAKENED: 2})]
    if card.id == CardId.PANACEA:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.ARTIFACT: 1 if not card.upgrade else 2})]
    if card.id == CardId.MIND_BLAST:
        return [CardEffects(target=TargetType.MONSTER, hits=1, pre_hooks=[mind_blast_pre_hook])]
    if card.id == CardId.GOOD_INSTINCTS:
        return [CardEffects(block=6 if not card.upgrade else 9, target=TargetType.SELF)]
    if card.id == CardId.ACROBATICS:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 4, amount_to_discard=1)]
    if card.id == CardId.BACKFLIP:
        return [CardEffects(target=TargetType.SELF, block=5 if not card.upgrade else 8, draw=2)]
    if card.id == CardId.DEADLY_POISON:
        return [CardEffects(target=TargetType.MONSTER, applies_powers={PowerId.POISON: 5 if not card.upgrade else 7})]
    if card.id == CardId.TACTICIAN:
        return [CardEffects(target=TargetType.NONE,
                            post_self_discarded_hooks=[tactician_post_self_discarded_hook] if not card.upgrade else [
                                tactician_upgraded_post_self_discarded_hook])]
    if card.id == CardId.REFLEX:
        return [CardEffects(target=TargetType.NONE,
                            post_self_discarded_hooks=[reflex_post_self_discarded_hook] if not card.upgrade else [
                                reflex_upgraded_post_self_discarded_hook])]
    if card.id == CardId.CONCENTRATE:
        return [CardEffects(target=TargetType.SELF, energy_gain=2, amount_to_discard=3 if not card.upgrade else 2)]
    if card.id == CardId.FLECHETTES:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6,
                            hits=len([1 for c in hand if c.type == CardType.SKILL]))]
    if card.id == CardId.EXPERTISE:
        return [CardEffects(target=TargetType.SELF, draw=6 - len(hand) + 1 if not card.upgrade else 7 - len(
            hand) + 1)]  # The +1 is for accounting for the EXPERTISE that doesn't disappear until after we've resolved the play.
    if card.id == CardId.BANE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            pre_hooks=[bane_pre_hook])]
    if card.id == CardId.BULLET_TIME:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.NO_DRAW: 1},
                            post_hooks=[bullet_time_post_hook])]
    if card.id == CardId.CHOKE:
        return [CardEffects(target=TargetType.MONSTER, damage=12, hits=1,
                            applies_powers={PowerId.CHOKED: 3 if not card.upgrade else 5})]
    if card.id == CardId.FLYING_KNEE:
        return [CardEffects(target=TargetType.MONSTER, damage=8 if not card.upgrade else 11, hits=1),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.ENERGIZED: 1})]
    if card.id == CardId.PREDATOR:
        return [CardEffects(target=TargetType.MONSTER, damage=15 if not card.upgrade else 20, hits=1),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.DRAW_CARD: 2})]
    if card.id == CardId.DODGE_AND_ROLL:
        amount = 4 if not card.upgrade else 6
        return [CardEffects(target=TargetType.SELF, block=amount, applies_powers={PowerId.NEXT_TURN_BLOCK: amount})]
    if card.id == CardId.OUTMANEUVER:
        return [CardEffects(target=TargetType.SELF,
                            applies_powers={PowerId.ENERGIZED: 2} if not card.upgrade else {PowerId.ENERGIZED: 3})]
    if card.id == CardId.ENVENOM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.ENVENOM: 1})]
    if card.id == CardId.HELLO_WORLD:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.HELLO: 1})]
    if card.id == CardId.MAGNETISM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MAGNETISM: 1})]
    if card.id == CardId.NOXIOUS_FUMES:
        return [
            CardEffects(target=TargetType.SELF, applies_powers={PowerId.NOXIOUS_FUMES: 2 if not card.upgrade else 3})]
    if card.id == CardId.ENDLESS_AGONY:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6, hits=1)]
    if card.id == CardId.CORPSE_EXPLOSION:
        return [CardEffects(target=TargetType.MONSTER, applies_powers={PowerId.POISON: 6 if not card.upgrade else 9,
                                                                       PowerId.CORPSE_EXPLOSION: 1})]
    if card.id == CardId.GRAND_FINALE:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=50 if not card.upgrade else 60, hits=1)]
    if card.id == CardId.WRAITH_FORM:
        return [CardEffects(target=TargetType.SELF,
                            applies_powers={PowerId.INTANGIBLE_PLAYER: 2 if not card.upgrade else 3,
                                            PowerId.WRAITH_FORM_POWER: 1})]
    if card.id == CardId.PIERCING_WAIL:
        return [CardEffects(target=TargetType.ALL_MONSTERS,
                            applies_powers={PowerId.STRENGTH: -6 if not card.upgrade else -8})]
    if card.id == CardId.BLUR:
        return [
            CardEffects(target=TargetType.SELF, block=5 if not card.upgrade else 8, applies_powers={PowerId.BLUR: 1})]
    if card.id == CardId.CATALYST:
        return [CardEffects(target=TargetType.MONSTER,
                            post_hooks=[catalyst_post_hook] if not card.upgrade else [catalyst_upgraded_post_hook])]
    if card.id == CardId.PHANTASMAL_KILLER:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.PHANTASMAL: 1})]
    if card.id == CardId.BOUNCING_FLASK:
        return [CardEffects(target=TargetType.ALL_MONSTERS, post_hooks=[bouncing_flask_post_hook])]
    if card.id == CardId.BEAM_CELL:
        return [CardEffects(target=TargetType.MONSTER, damage=3 if not card.upgrade else 4, hits=1,
                            applies_powers={PowerId.VULNERABLE: 1 if not card.upgrade else 2})]
    if card.id == CardId.LEAP:
        return [CardEffects(target=TargetType.SELF, block=9 if not card.upgrade else 12)]
    if card.id == CardId.CHARGE_BATTERY:
        return [CardEffects(target=TargetType.SELF, block=7 if not card.upgrade else 10,
                            applies_powers={PowerId.ENERGIZED: 1})]
    if card.id == CardId.BUFFER:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.BUFFER: 1 if not card.upgrade else 2})]
    if card.id == CardId.SKIM:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 4)]
    if card.id == CardId.RIP_AND_TEAR:
        damage = 7 if not card.upgrade else 9
        return [CardEffects(target=TargetType.RANDOM, hits=2, damage=damage)]
    if card.id == CardId.SWEEPING_BEAM:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=6 if not card.upgrade else 9, hits=1, draw=1)]
    if card.id == CardId.CORE_SURGE:
        return [CardEffects(target=TargetType.MONSTER, damage=11 if not card.upgrade else 15, hits=1),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.ARTIFACT: 1})]
    if card.id == CardId.FTL:
        return [CardEffects(target=TargetType.MONSTER, damage=5 if not card.upgrade else 6, hits=1,
                            pre_hooks=[ftl_pre_hook])]
    if card.id == CardId.BLIZZARD:
        return [CardEffects(hits=1, target=TargetType.ALL_MONSTERS, pre_hooks=[blizzard_pre_hook])]
    if card.id == CardId.THUNDER_STRIKE:
        return [CardEffects(target=TargetType.RANDOM, damage=7 if not card.upgrade else 9,
                            pre_hooks=[thunder_strike_pre_hook])]
    if card.id == CardId.SCRAPE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            draw=4 if not card.upgrade else 5)]
    if card.id == CardId.BOOT_SEQUENCE:
        return [CardEffects(target=TargetType.SELF, block=10 if not card.upgrade else 13)]
    if card.id == CardId.STACK:
        return [CardEffects(target=TargetType.SELF, pre_hooks=[stack_pre_hook])]
    if card.id == CardId.AUTO_SHIELDS:
        return [CardEffects(target=TargetType.SELF, pre_hooks=[auto_shields_pre_hook])]
    if card.id == CardId.STREAMLINE:
        return [CardEffects(target=TargetType.MONSTER, damage=15 if not card.upgrade else 20, hits=1,
                            post_hooks=[streamline_post_hook])]
    if card.id == CardId.TURBO:
        return [
            CardEffects(target=TargetType.SELF, energy_gain=2 if not card.upgrade else 3,
                        spawn_cards_in_discard=(get_card(CardId.VOID), 1))]
    if card.id == CardId.AGGREGATE:
        return [CardEffects(target=TargetType.SELF,
                            post_hooks=[aggregate_post_hook] if not card.upgrade else [aggregate_upgraded_post_hook])]
    if card.id == CardId.DOUBLE_ENERGY:
        return [CardEffects(target=TargetType.SELF, post_hooks=[double_energy_post_hook])]
    if card.id == CardId.HEATSINKS:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.HEATSINK: 1 if not card.upgrade else 2})]
    if card.id == CardId.OVERCLOCK:
        return [
            CardEffects(target=TargetType.SELF, draw=2 if not card.upgrade else 3,
                        spawn_cards_in_discard=(get_card(CardId.BURN), 1))]
    if card.id == CardId.SELF_REPAIR:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.REPAIR: 7 if not card.upgrade else 10})]
    if card.id == CardId.MACHINE_LEARNING:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MACHINE_LEARNING: 1})]
    if card.id == CardId.STORM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STORM: 1})]
    if card.id == CardId.LOOP:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.LOOP: 1 if not card.upgrade else 2})]
    if card.id == CardId.ELECTRODYNAMICS:
        orbs = [OrbId.LIGHTNING, OrbId.LIGHTNING]
        if card.upgrade:
            orbs.append(OrbId.LIGHTNING)
        # we add the power by pre-hook because it's being applied before orbs are channeled...
        return [CardEffects(target=TargetType.SELF, pre_hooks=[electrodynamics_pre_hook], channel_orbs=orbs)]
    if card.id == CardId.DEFRAGMENT:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.FOCUS: 1 if not card.upgrade else 2})]
    if card.id == CardId.BIASED_COGNITION:
        return [CardEffects(target=TargetType.SELF,
                            applies_powers={PowerId.FOCUS: 4 if not card.upgrade else 5, PowerId.BIAS: 1})]
    if card.id == CardId.CREATIVE_AI:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.CREATIVE_AI: 1})]
    if card.id == CardId.CAPACITOR:
        return [CardEffects(target=TargetType.SELF,
                            post_hooks=[capacitor_post_hook] if not card.upgrade else [capacitor_upgraded_post_hook])]
    if card.id == CardId.FISSION:
        return [CardEffects(target=TargetType.SELF,
                            post_hooks=[fission_post_hook] if not card.upgrade else [fission_upgraded_post_hook])]
    if card.id == CardId.ZAP:
        return [CardEffects(target=TargetType.SELF, channel_orbs=[OrbId.LIGHTNING])]
    if card.id == CardId.FUSION:
        return [CardEffects(target=TargetType.SELF, channel_orbs=[OrbId.PLASMA])]
    if card.id == CardId.CHAOS:
        orbs = [OrbId.INTERNAL_RANDOM_ORB] if not card.upgrade else [OrbId.INTERNAL_RANDOM_ORB,
                                                                     OrbId.INTERNAL_RANDOM_ORB]
        return [CardEffects(target=TargetType.SELF, channel_orbs=orbs)]
    if card.id == CardId.DARKNESS:
        hook = darkness_post_hook if not card.upgrade else darkness_upgraded_post_hook
        return [CardEffects(target=TargetType.SELF, post_hooks=[hook])]
    if card.id == CardId.DUALCAST:
        return [CardEffects(target=TargetType.SELF, post_hooks=[dualcast_post_hook])]
    if card.id == CardId.MULTI_CAST:
        return [CardEffects(target=TargetType.SELF, post_hooks=[multicast_post_hook])]
    if card.id == CardId.BALL_LIGHTNING:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            channel_orbs=[OrbId.LIGHTNING])]
    if card.id == CardId.TEMPEST:
        x_amount = get_x_trigger_amount(player) + min(card.upgrade, 1)
        return [CardEffects(target=TargetType.SELF, channel_orbs=[OrbId.LIGHTNING] * x_amount)]
    if card.id == CardId.REINFORCED_BODY:
        return [CardEffects(target=TargetType.SELF, block=7 if not card.upgrade else 9,
                            block_times=get_x_trigger_amount(player))]
    if card.id == CardId.COOLHEADED:
        return [CardEffects(draw=1 if not card.upgrade else 2, target=TargetType.SELF, channel_orbs=[OrbId.FROST])]
    if card.id == CardId.COLD_SNAP:
        return [CardEffects(target=TargetType.MONSTER, damage=6 if not card.upgrade else 9, hits=1,
                            channel_orbs=[OrbId.FROST])]
    if card.id == CardId.DOOM_AND_GLOOM:
        return [CardEffects(damage=10 if not card.upgrade else 14, hits=1, target=TargetType.ALL_MONSTERS,
                            channel_orbs=[OrbId.DARK])]
    if card.id == CardId.GLACIER:
        return [CardEffects(block=7 if not card.upgrade else 10, target=TargetType.SELF,
                            channel_orbs=[OrbId.FROST, OrbId.FROST])]
    if card.id == CardId.CONSUME:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.FOCUS: 2 if not card.upgrade else 3},
                            post_hooks=[consume_post_hook])]
    if card.id == CardId.CHILL:
        return [CardEffects(target=TargetType.SELF, post_hooks=[chill_post_hook])]
    if card.id == CardId.RECURSION:
        return [CardEffects(target=TargetType.SELF, post_hooks=[recursion_post_hook])]
    if card.id == CardId.BARRAGE:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6, hits=0,
                            pre_hooks=[barrage_pre_hook])]
    if card.id == CardId.METEOR_STRIKE:
        return [CardEffects(target=TargetType.MONSTER, damage=24 if not card.upgrade else 30, hits=1,
                            channel_orbs=[OrbId.PLASMA, OrbId.PLASMA, OrbId.PLASMA])]
    if card.id == CardId.RAINBOW:
        return [CardEffects(target=TargetType.SELF, channel_orbs=[OrbId.LIGHTNING, OrbId.FROST, OrbId.DARK])]
    if card.id == CardId.REPROGRAM:
        amount = 1 if not card.upgrade else 2
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.FOCUS: -amount, PowerId.STRENGTH: amount,
                                                                    PowerId.DEXTERITY: amount})]
    if card.id == CardId.HYPERBEAM:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=26 if not card.upgrade else 34, hits=1),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.FOCUS: -3})]
    if card.id == CardId.SUNDER:
        return [CardEffects(target=TargetType.MONSTER, damage=24 if not card.upgrade else 32, hits=1,
                            post_hooks=[sunder_post_hook])]
    if card.id == CardId.ALL_FOR_ONE:
        return [CardEffects(target=TargetType.MONSTER, damage=10 if not card.upgrade else 14, hits=1,
                            post_hooks=[all_for_one_post_hook])]
    if card.id == CardId.MELTER:
        return [CardEffects(target=TargetType.MONSTER, damage=10 if not card.upgrade else 14, hits=1,
                            pre_hooks=[melter_pre_hook])]
    if card.id == CardId.REBOOT:
        return [CardEffects(target=TargetType.SELF, post_hooks=[reboot_post_hook])]
    if card.id == CardId.BULLSEYE:
        return [CardEffects(target=TargetType.MONSTER, damage=8 if not card.upgrade else 11, hits=1,
                            applies_powers={PowerId.LOCK_ON: 2 if not card.upgrade else 3})]
    if card.id == CardId.CALCULATED_GAMBLE:
        return [CardEffects(target=TargetType.SELF, post_hooks=[calculated_gamble_post_hook])]
    if card.id == CardId.COMPILE_DRIVER:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            post_hooks=[compile_driver_post_hook])]
    if card.id == CardId.ECHO_FORM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.ECHO_FORM: 1})]
    if card.id == CardId.GO_FOR_THE_EYES:
        return [CardEffects(target=TargetType.MONSTER, damage=3 if not card.upgrade else 4, hits=1,
                            post_hooks=[go_for_the_eyes_post_hook])]
    if card.id == CardId.AMPLIFY:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.AMPLIFY: 1 if not card.upgrade else 2})]
    if card.id == CardId.BURST:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.BURST: 1 if not card.upgrade else 2})]
    if card.id == CardId.MALAISE:
        x_amount = get_x_trigger_amount(player) if not card.upgrade else get_x_trigger_amount(player) + 1
        return [CardEffects(target=TargetType.MONSTER,
                            applies_powers={PowerId.WEAKENED: x_amount, PowerId.STRENGTH: -x_amount})]
    if card.id == CardId.SKEWER:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10,
                            hits=get_x_trigger_amount(player))]
    if card.id == CardId.DOUBLE_TAP:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DOUBLE_TAP: 1 if not card.upgrade else 2})]
    if card.id == CardId.EQUILIBRIUM:
        return [CardEffects(target=TargetType.SELF, block=13 if not card.upgrade else 16,
                            applies_powers={PowerId.EQUILIBRIUM: 1})]
    if card.id == CardId.FLYING_SLEEVES:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6, hits=2, retains=True)]
    if card.id == CardId.ESTABLISHMENT:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.ESTABLISHMENT: 1})]
    if card.id == CardId.BATTLE_HYMN:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.BATTLE_HYMN: 1})]
    if card.id == CardId.STUDY:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STUDY: 1})]
    if card.id == CardId.BOWLING_BASH:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10,
                            pre_hooks=[bowling_bash_pre_hook])]
    if card.id == CardId.CONSECRATE:
        return [CardEffects(damage=5 if not card.upgrade else 8, hits=1, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.CONCLUDE:
        return [CardEffects(damage=12 if not card.upgrade else 16, hits=1, target=TargetType.ALL_MONSTERS,
                            post_hooks=[conclude_post_hook])]
    if card.id == CardId.RAGNAROK:
        hits_and_damage = 5 if not card.upgrade else 6
        return [CardEffects(target=TargetType.RANDOM, hits=hits_and_damage, damage=hits_and_damage)]
    if card.id == CardId.INSIGHT:
        return [CardEffects(draw=2 if not card.upgrade else 3, retains=True)]
    if card.id == CardId.PROTECT:
        return [CardEffects(block=12 if not card.upgrade else 16, target=TargetType.SELF, retains=True)]
    if card.id == CardId.SMITE:
        return [CardEffects(damage=12 if not card.upgrade else 16, hits=1, target=TargetType.MONSTER, retains=True)]
    if card.id == CardId.FEEL_NO_PAIN:
        return [
            CardEffects(target=TargetType.SELF, applies_powers={PowerId.FEEL_NO_PAIN: 3 if not card.upgrade else 4})]
    if card.id == CardId.DARK_EMBRACE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DARK_EMBRACE: 1})]
    if card.id == CardId.CORRUPTION:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.CORRUPTION: 1})]
    if card.id == CardId.SENTINEL:
        # additional effect handled in exhaust_card directly
        return [CardEffects(block=5 if not card.upgrade else 8, target=TargetType.SELF)]
    if card.id == CardId.SEVER_SOUL:
        return [CardEffects(damage=16 if not card.upgrade else 22, hits=1, target=TargetType.MONSTER,
                            post_hooks=[sever_soul_post_hook])]
    if card.id == CardId.SECOND_WIND:
        return [CardEffects(target=TargetType.SELF, post_hooks=[second_wind_post_hook])]
    if card.id == CardId.RITUAL_DAGGER:
        return [CardEffects(hits=1, target=TargetType.MONSTER, pre_hooks=[ritual_dagger_pre_hook],
                            post_hooks=[ritual_dagger_post_hook])]
    if card.id == CardId.FINISHER:
        return [CardEffects(damage=6 if not card.upgrade else 8, target=TargetType.MONSTER,
                            pre_hooks=[finisher_pre_hook])]
    if card.id == CardId.CLAW:
        return [CardEffects(hits=1, target=TargetType.MONSTER, pre_hooks=[claw_pre_hook], post_hooks=[claw_post_hook])]
    if card.id == CardId.GENETIC_ALGORITHM:
        return [CardEffects(target=TargetType.SELF, pre_hooks=[genetic_algorithm_pre_hook],
                            post_hooks=[genetic_algorithm_post_hook])]
    if card.id == CardId.STEAM_BARRIER:
        return [CardEffects(target=TargetType.SELF, pre_hooks=[steam_barrier_pre_hook],
                            post_hooks=[steam_barrier_post_hook])]
    if card.id == CardId.GLASS_KNIFE:
        return [CardEffects(hits=2, target=TargetType.MONSTER, pre_hooks=[glass_knife_pre_hook],
                            post_hooks=[glass_knife_post_hook])]
    if card.id == CardId.JUDGEMENT:
        return [CardEffects(target=TargetType.MONSTER, post_hooks=[judgement_post_hook])]
    if card.id == CardId.SCRAWL:
        return [CardEffects(target=TargetType.SELF, draw=10 - len(hand) + 1)]
        # The +1 is for accounting for the SCRAWL that doesn't disappear until after we've resolved the play.
    if card.id == CardId.SANCTITY:
        return [CardEffects(block=6 if not card.upgrade else 9, target=TargetType.SELF,
                            pre_hooks=[sanctity_pre_hook])]
    if card.id == CardId.CRUSH_JOINTS:
        return [CardEffects(damage=8 if not card.upgrade else 10, hits=1, target=TargetType.MONSTER,
                            pre_hooks=[crush_joints_pre_hook])]
    if card.id == CardId.SASH_WHIP:
        return [CardEffects(damage=8 if not card.upgrade else 10, hits=1, target=TargetType.MONSTER,
                            pre_hooks=[sash_whip_pre_hook])]
    if card.id == CardId.FOLLOW_UP:
        return [CardEffects(damage=7 if not card.upgrade else 11, hits=1, target=TargetType.MONSTER,
                            pre_hooks=[follow_up_pre_hook])]
    if card.id == CardId.CRESCENDO:
        return [CardEffects(target=TargetType.SELF, retains=True, sets_stance=StanceType.WRATH)]
    if card.id == CardId.TRANQUILITY:
        return [CardEffects(target=TargetType.SELF, retains=True, sets_stance=StanceType.CALM)]
    if card.id == CardId.VIGILANCE:
        return [CardEffects(target=TargetType.SELF, block=8 if not card.upgrade else 12, sets_stance=StanceType.CALM)]
    if card.id == CardId.LIKE_WATER:
        amount = 5 if not card.upgrade else 7
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.LIKE_WATER: amount})]
    if card.id == CardId.RUSHDOWN:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.RUSHDOWN: 2})]
    if card.id == CardId.ERUPTION:
        return [CardEffects(damage=9, hits=1, target=TargetType.MONSTER, sets_stance=StanceType.WRATH)]
    if card.id == CardId.PROSTRATE:
        amount_of_mantra = 2 if not card.upgrade else 3
        return [
            CardEffects(target=TargetType.SELF, block=4, applies_powers={PowerId.MANTRA_INTERNAL: amount_of_mantra})]
    if card.id == CardId.WORSHIP:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MANTRA_INTERNAL: 5},
                            retains=False if not card.upgrade else True)]
    if card.id == CardId.MIRACLE:
        return [CardEffects(target=TargetType.SELF, energy_gain=1 if not card.upgrade else 2, retains=True)]
    if card.id == CardId.DEVOTION:
        amount = 2 if not card.upgrade else 3
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DEVOTION: amount})]
    if card.id == CardId.PRAY:
        amount_of_mantra = 3 if not card.upgrade else 4
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MANTRA_INTERNAL: amount_of_mantra},
                            spawn_cards_in_draw=(get_card(CardId.INSIGHT), 1))]
    if card.id == CardId.EMPTY_BODY:
        return [
            CardEffects(block=7 if not card.upgrade else 10, target=TargetType.SELF, sets_stance=StanceType.NO_STANCE)]
    if card.id == CardId.EMPTY_FIST:
        return [CardEffects(damage=9 if not card.upgrade else 14, hits=1, target=TargetType.MONSTER,
                            sets_stance=StanceType.NO_STANCE)]
    if card.id == CardId.EMPTY_MIND:
        return [
            CardEffects(draw=2 if not card.upgrade else 3, target=TargetType.SELF, sets_stance=StanceType.NO_STANCE)]
    if card.id == CardId.EVALUATE:
        return [
            CardEffects(block=6 if not card.upgrade else 10, target=TargetType.SELF,
                        spawn_cards_in_draw=(get_card(CardId.INSIGHT), 1))]
    if card.id == CardId.MENTAL_FORTRESS:
        amount = 4 if not card.upgrade else 6
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MENTAL_FORTRESS: amount})]
    if card.id == CardId.FLURRY_OF_BLOWS:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6, hits=1)]
    if card.id == CardId.TANTRUM:
        return [CardEffects(target=TargetType.MONSTER, damage=3, hits=3 if not card.upgrade else 4,
                            sets_stance=StanceType.WRATH, post_hooks=[tantrum_post_hook])]
    if card.id == CardId.INNER_PEACE:
        return [CardEffects(target=TargetType.SELF, post_hooks=[inner_peace_post_hook])]
    if card.id == CardId.INDIGNATION:
        return [CardEffects(target=TargetType.SELF, post_hooks=[indignation_post_hook])]
    if card.id == CardId.FEAR_NO_EVIL:
        return [CardEffects(target=TargetType.MONSTER, damage=8 if not card.upgrade else 11, hits=1,
                            post_hooks=[fear_no_evil_post_hook])]
    if card.id == CardId.HALT:
        return [CardEffects(target=TargetType.SELF, block=3 if not card.upgrade else 4, pre_hooks=[halt_pre_hook])]
    if card.id == CardId.WREATH_OF_FLAME:
        amount = 5 if not card.upgrade else 8
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.VIGOR: amount})]
    if card.id == CardId.SAFETY:
        return [CardEffects(target=TargetType.SELF, block=12 if not card.upgrade else 16, retains=True)]
    if card.id == CardId.DECEIVE_REALITY:
        return [
            CardEffects(block=4 if not card.upgrade else 7, target=TargetType.SELF,
                        spawn_cards_in_hand=(get_card(CardId.SAFETY), 1))]
    if card.id == CardId.MASTER_REALITY:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MASTER_REALITY: 1})]
    if card.id == CardId.CARVE_REALITY:
        return [
            CardEffects(damage=6 if not card.upgrade else 10, hits=1, target=TargetType.MONSTER,
                        spawn_cards_in_hand=(get_card(CardId.SMITE), 1))]
    if card.id == CardId.PERSEVERANCE:
        return [CardEffects(target=TargetType.SELF, pre_hooks=[perseverance_pre_hook], retains=True)]
    if card.id == CardId.REACH_HEAVEN:
        return [
            CardEffects(damage=10 if not card.upgrade else 15, hits=1, target=TargetType.MONSTER,
                        spawn_cards_in_draw=(get_card(CardId.THROUGH_VIOLENCE), 1))]
    if card.id == CardId.THROUGH_VIOLENCE:
        return [
            CardEffects(damage=20 if not card.upgrade else 30, hits=1, target=TargetType.MONSTER, retains=True)]
    if card.id == CardId.SIGNATURE_MOVE:
        return [
            CardEffects(damage=30 if not card.upgrade else 40, hits=1, target=TargetType.MONSTER)]
    if card.id == CardId.WHEEL_KICK:
        return [
            CardEffects(damage=15 if not card.upgrade else 20, hits=1, target=TargetType.MONSTER, draw=2)]
    if card.id == CardId.SPIRIT_SHIELD:
        return [CardEffects(target=TargetType.SELF, pre_hooks=[spirit_shield_pre_hook])]
    if card.id == CardId.WALLOP:
        return [CardEffects(target=TargetType.MONSTER, damage=9 if not card.upgrade else 12, hits=1)]
    if card.id == CardId.WINDMILL_STRIKE:
        return [CardEffects(target=TargetType.MONSTER, hits=1, pre_hooks=[windmill_strike_pre_hook], retains=True)]
    if card.id == CardId.BRILLIANCE:
        return [CardEffects(target=TargetType.MONSTER, hits=1, pre_hooks=[brilliance_pre_hook])]
    if card.id == CardId.DEVA_FORM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DEVA: 1})]
    if card.id == CardId.WAVE_OF_THE_HAND:
        power_amount = 1 if not card.upgrade else 2
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.WAVE_OF_THE_HAND: power_amount})]
    if card.id == CardId.SANDS_OF_TIME:
        return [
            CardEffects(damage=20 if not card.upgrade else 26, hits=1, target=TargetType.MONSTER, retains=True)]
    if card.id == CardId.FASTING:
        power_amount = 3 if not card.upgrade else 4
        return [CardEffects(target=TargetType.SELF,
                            applies_powers={PowerId.STRENGTH: power_amount, PowerId.DEXTERITY: power_amount,
                                            PowerId.FASTING: 1})]
    if card.id == CardId.SWIVEL:
        block_amount = 8 if not card.upgrade else 11
        return [CardEffects(target=TargetType.SELF, block=block_amount, applies_powers={PowerId.FREE_ATTACK_POWER: 1})]
    if card.id == CardId.TALK_TO_THE_HAND:
        power_amount = 2 if not card.upgrade else 3
        return [CardEffects(damage=5 if not card.upgrade else 7, hits=1, target=TargetType.MONSTER,
                            applies_powers={PowerId.BLOCK_RETURN: power_amount})]
    if card.id == CardId.COLLECT:
        x_amount = get_x_trigger_amount(player) + min(card.upgrade, 1)
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.COLLECT: x_amount})]
    if card.id == CardId.PRESSURE_POINTS:
        power_amount = 8 if not card.upgrade else 11
        return [CardEffects(target=TargetType.MONSTER, applies_powers={PowerId.MARK: power_amount},
                            post_hooks=[pressure_points_post_hook])]
    if card.id == CardId.CUT_THROUGH_FATE:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 9, hits=1,
                            draw=1, amount_to_scry=2 if not card.upgrade else 3)]
    if card.id == CardId.JUST_LUCKY:
        return [CardEffects(target=TargetType.MONSTER, damage=3 if not card.upgrade else 4, hits=1),
                CardEffects(target=TargetType.SELF, block=2 if not card.upgrade else 3,
                            amount_to_scry=1 if not card.upgrade else 2)]
    if card.id == CardId.THIRD_EYE:
        return [CardEffects(target=TargetType.SELF, block=7 if not card.upgrade else 9,
                            amount_to_scry=3 if not card.upgrade else 5)]
    if card.id == CardId.FORESIGHT:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.FORESIGHT: 3 if not card.upgrade else 4})]
    if card.id == CardId.WEAVE:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6, hits=1)]
    if card.id == CardId.NIRVANA:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.NIRVANA: 3 if not card.upgrade else 4})]
    if card.id == CardId.BLASPHEMY:
        return [
            CardEffects(target=TargetType.SELF, sets_stance=StanceType.DIVINITY, applies_powers={PowerId.BLASPHEMER: 1},
                        retains=False if not card.upgrade else True)]
    if card.id == CardId.ALPHA:
        return [CardEffects(target=TargetType.SELF, spawn_cards_in_draw=(get_card(CardId.BETA), 1),
                            applies_powers={PowerId.FAKE_ALPHA_BETA: 1})]
    if card.id == CardId.BETA:
        return [CardEffects(target=TargetType.SELF, spawn_cards_in_draw=(get_card(CardId.OMEGA), 1),
                            applies_powers={PowerId.FAKE_ALPHA_BETA: 1})]
    if card.id == CardId.OMEGA:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.OMEGA: 50 if not card.upgrade else 60})]
    if card.id == CardId.LESSON_LEARNED:
        return [CardEffects(target=TargetType.MONSTER, damage=10 if not card.upgrade else 13, hits=1,
                            post_hooks=[lesson_learned_post_hook])]
    if card.id == CardId.SIMMERING_FURY:
        return [
            CardEffects(target=TargetType.SELF, applies_powers={PowerId.SIMMERING_RAGE: 2 if not card.upgrade else 2})]
    if card.id == CardId.WISH:
        strength_amount = 3 if not card.upgrade else 4
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.STRENGTH: strength_amount})]
    if card.id == CardId.FOREIGN_INFLUENCE:
        return [CardEffects(target=TargetType.SELF)]
    if card.id == CardId.BARRICADE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.BARRICADE: 1})]
    if card.id == CardId.BURNING_PACT:
        return [CardEffects(target=TargetType.SELF, draw=2 if not card.upgrade else 3, amount_to_exhaust=1)]
    if card.id == CardId.RECYCLE:
        return [CardEffects(target=TargetType.SELF, amount_to_exhaust=1, post_hooks=[recycle_post_hook])]
    return [CardEffects()]
