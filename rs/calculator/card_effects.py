from typing import List

from rs.calculator.card_effect_custom_hooks import *
from rs.calculator.enums.card_id import CardId
from rs.calculator.enums.orb_id import OrbId
from rs.calculator.enums.power_id import PowerId
from rs.calculator.interfaces.card_effect_hooks_interface import CardEffectCustomHook, CardEffectCustomHookWithCard
from rs.calculator.interfaces.card_effects_interface import CardEffectsInterface, TargetType
from rs.calculator.interfaces.player import PlayerInterface
from rs.calculator.interfaces.powers import Powers


class CardEffects(CardEffectsInterface):
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
            post_self_discarded_hooks: List[CardEffectCustomHook] = None,
            end_turn_hooks: List[CardEffectCustomHook] = None,
            heal: int = 0,
            amount_to_discard: int = 0,
            add_cards_to_hand: [CardInterface, int] = None,
            channel_orbs: List[OrbId] = None,
            retains: bool = False
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
        self.post_self_discarded_hooks: List[
            CardEffectCustomHook] = [] if post_self_discarded_hooks is None else post_self_discarded_hooks
        self.end_turn_hooks: List[
            CardEffectCustomHook] = [] if end_turn_hooks is None else end_turn_hooks
        self.heal: int = heal
        self.amount_to_discard: int = amount_to_discard
        self.add_cards_to_hand: [CardInterface, int] = add_cards_to_hand
        self.channel_orbs: List[OrbId] = [] if channel_orbs is None else channel_orbs
        self.retains: bool = retains


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
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.FIRE_BREATHING: 6 if not card.upgrade else 10})]
    if card.id == CardId.EVOLVE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.EVOLVE: 1 if not card.upgrade else 2})]
    if card.id == CardId.DEMON_FORM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DEMON_FORM: 2 if not card.upgrade else 3})]
    if card.id == CardId.BERSERK:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.VULNERABLE: 2 if not card.upgrade else 1, PowerId.BERSERK: 1})]
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
    if card.id == CardId.VOID:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.IMMOLATE:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=21 if not card.upgrade else 28, hits=1,
                            post_hooks=[immolate_post_hook])]
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
    if card.id == CardId.PARASITE:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.INJURY:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.CLUMSY:
        return [CardEffects(target=TargetType.NONE)]
    if card.id == CardId.ASCENDERS_BANE:
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
                            post_hooks=[wild_strike_post_hook])]
    if card.id == CardId.BATTLE_TRANCE:
        return [CardEffects(target=TargetType.SELF, draw=3 if not card.upgrade else 5),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.NO_DRAW: 1})]
    if card.id == CardId.RAGE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.RAGE: 3 if not card.upgrade else 5})]
    if card.id == CardId.RAMPAGE:
        return [CardEffects(target=TargetType.MONSTER, damage=8, hits=1)]
    if card.id == CardId.SWORD_BOOMERANG:
        hook = sword_boomerang_post_hook if not card.upgrade else sword_boomerang_upgraded_post_hook
        return [CardEffects(target=TargetType.ALL_MONSTERS, post_hooks=[hook])]
    if card.id == CardId.JUGGERNAUT:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.JUGGERNAUT: 5 if not card.upgrade else 7})]
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
        hook = impatience_post_hook if not card.upgrade else impatience_upgraded_post_hook
        return [CardEffects(target=TargetType.SELF, post_hooks=[hook])]
    if card.id == CardId.MAYHEM:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.MAYHEM: 1})]
    if card.id == CardId.PANACHE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.PANACHE: 5})]
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
        return [CardEffects(target=TargetType.SELF, add_cards_to_hand=(get_card(CardId.SHIV), amount))]
    if card.id == CardId.CLOAK_AND_DAGGER:
        amount = 1 if not card.upgrade else 2
        return [CardEffects(block=6, target=TargetType.SELF, add_cards_to_hand=(get_card(CardId.SHIV), amount))]
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
                                                                       PowerId.CORPSE_EXPLOSION_POWER: 1})]
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
        hook = bouncing_flask_post_hook if not card.upgrade else bouncing_flask_upgraded_post_hook
        return [CardEffects(target=TargetType.ALL_MONSTERS, post_hooks=[hook])]
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
        hook = rip_and_tear_post_hook if not card.upgrade else rip_and_tear_upgraded_post_hook
        return [CardEffects(target=TargetType.ALL_MONSTERS, post_hooks=[hook])]
    if card.id == CardId.SWEEPING_BEAM:
        return [CardEffects(target=TargetType.ALL_MONSTERS, damage=6 if not card.upgrade else 9, hits=1, draw=1)]
    if card.id == CardId.CORE_SURGE:
        return [CardEffects(target=TargetType.MONSTER, damage=11 if not card.upgrade else 15, hits=1),
                CardEffects(target=TargetType.SELF, applies_powers={PowerId.ARTIFACT: 1})]
    if card.id == CardId.BOOT_SEQUENCE:
        return [CardEffects(target=TargetType.SELF, block=10 if not card.upgrade else 13)]
    if card.id == CardId.STACK:
        return [CardEffects(target=TargetType.SELF,
                            pre_hooks=[stack_pre_hook] if not card.upgrade else [stack_upgraded_pre_hook])]
    if card.id == CardId.AUTO_SHIELDS:
        hook = auto_shields_post_hook if not card.upgrade else auto_shields_upgraded_post_hook
        return [CardEffects(target=TargetType.SELF, post_hooks=[hook])]
    if card.id == CardId.STREAMLINE:
        return [CardEffects(target=TargetType.MONSTER, damage=15 if not card.upgrade else 20, hits=1)]
    if card.id == CardId.TURBO:
        return [
            CardEffects(target=TargetType.SELF, energy_gain=2 if not card.upgrade else 3, post_hooks=[turbo_post_hook])]
    if card.id == CardId.AGGREGATE:
        return [CardEffects(target=TargetType.SELF,
                            post_hooks=[aggregate_post_hook] if not card.upgrade else [aggregate_upgraded_post_hook])]
    if card.id == CardId.DOUBLE_ENERGY:
        return [CardEffects(target=TargetType.SELF, post_hooks=[double_energy_post_hook])]
    if card.id == CardId.HEATSINKS:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.HEATSINK: 1 if not card.upgrade else 2})]
    if card.id == CardId.OVERCLOCK:
        return [
            CardEffects(target=TargetType.SELF, draw=2 if not card.upgrade else 3, post_hooks=[overclock_post_hook])]
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
        orbs = [OrbId.INTERNAL_RANDOM_ORB] if not card.upgrade else [OrbId.INTERNAL_RANDOM_ORB, OrbId.INTERNAL_RANDOM_ORB]
        return [CardEffects(target=TargetType.SELF, channel_orbs=orbs)]
    if card.id == CardId.DARKNESS:
        hook = darkness_post_hook if not card.upgrade else darkness_upgraded_post_hook
        return [CardEffects(target=TargetType.SELF, post_hooks=[hook])]
    if card.id == CardId.DUALCAST:
        return [CardEffects(target=TargetType.SELF, post_hooks=[dualcast_post_hook])]
    if card.id == CardId.BALL_LIGHTNING:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10, hits=1,
                            channel_orbs=[OrbId.LIGHTNING])]
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
        return [CardEffects(target=TargetType.SELF,
                            post_hooks=[reboot_post_hook] if not card.upgrade else [reboot_upgraded_post_hook])]
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
        hook = go_for_the_eyes_post_hook if not card.upgrade else go_for_the_eyes_upgraded_post_hook
        return [CardEffects(target=TargetType.MONSTER, damage=3 if not card.upgrade else 4, hits=1, post_hooks=[hook])]
    if card.id == CardId.AMPLIFY:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.AMPLIFY: 1 if not card.upgrade else 2})]
    if card.id == CardId.BURST:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.BURST: 1 if not card.upgrade else 2})]
    if card.id == CardId.DOUBLE_TAP:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DOUBLE_TAP: 1 if not card.upgrade else 2})]
    if card.id == CardId.EQUILIBRIUM:
        return [CardEffects(target=TargetType.SELF, block=13 if not card.upgrade else 16,
                            applies_powers={PowerId.RETAIN_ALL: 1})]
    if card.id == CardId.FLYING_SLEEVES:
        return [CardEffects(target=TargetType.MONSTER, damage=4 if not card.upgrade else 6, hits=2, retains=True)]
    if card.id == CardId.ESTABLISHMENT:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.ESTABLISHMENT: 1})]
    if card.id == CardId.BOWLING_BASH:
        return [CardEffects(target=TargetType.MONSTER, damage=7 if not card.upgrade else 10,
                            pre_hooks=[bowling_bash_pre_hook])]
    if card.id == CardId.CONSECRATE:
        return [CardEffects(damage=5 if not card.upgrade else 8, hits=1, target=TargetType.ALL_MONSTERS)]
    if card.id == CardId.CONCLUDE:
        return [CardEffects(damage=12 if not card.upgrade else 16, hits=1, target=TargetType.ALL_MONSTERS,
                post_hooks=[conclude_post_hook])]
    if card.id == CardId.RAGNAROK:
        hook = ragnarok_post_hook if not card.upgrade else ragnarok_upgraded_post_hook
        return [CardEffects(target=TargetType.ALL_MONSTERS, post_hooks=[hook])]
    if card.id == CardId.INSIGHT:
        return [CardEffects(draw=2 if not card.upgrade else 3, retains=True)]
    if card.id == CardId.PROTECT:
        return [CardEffects(block=12 if not card.upgrade else 16, target=TargetType.SELF, retains=True)]
    if card.id == CardId.SMITE:
        return [CardEffects(damage=12 if not card.upgrade else 16, hits=1, target=TargetType.MONSTER, retains=True)]
    if card.id == CardId.FEEL_NO_PAIN:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.FEEL_NO_PAIN: 3 if not card.upgrade else 4})]
    if card.id == CardId.DARK_EMBRACE:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.DARK_EMBRACE: 1})]
    if card.id == CardId.CORRUPTION:
        return [CardEffects(target=TargetType.SELF, applies_powers={PowerId.CORRUPTION: 1})]
    if card.id == CardId.SENTINEL:
        # additional effect handled in exhaust_card directly
        return [CardEffects(block=5 if not card.upgrade else 8, target=TargetType.SELF)]
    return [CardEffects()]
