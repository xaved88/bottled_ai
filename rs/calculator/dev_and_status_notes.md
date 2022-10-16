This is where we'll keep the status of the calculator organized for a bit, what next steps are, total prio lists, etc.


So the concept for card draw...
We'll create a new "card_draw" card. Would be great if we could give it an internal stat for
"How much energy it had left" (though we could also just create 4 new cards for 3+, 2, 1, 0)...
Card draw will give you those into your hand.

Yeah, let's just do 4 different cards for right now, because that will fit best in it.


## NEXT FEATURES
- ~~card draw~~
- minion handling

## STRATEGY DECISIONS
- weak + vulnerable, improve valuing of it
- prioritizing card draw in the strategy?
- what else?

### KEY:

normal = okay

*italic* = to investigate

**bold** = we need to make adjustments for

~~strikethrough~~ = done



## NEXT RELICS

- 4 ornamental fan
- 4 orichalcum
- 4 odd mushroom
- 4 champion belt
- 4 letter opener
- 4 tori
- 4 fossilized helix
- 4 tungsten rod
- 4 the boot


## NEXT POWERS
- 4 rage
- 4 metallicize
- 4 intangible
- 4 thorns
- 4 angry
- 4 sharp hide (guardian)
- 4 flight
- 
## NEXT CARDS

- body slam
- clash
- flex
- wild strike
- battle trance
- rage
- metallicize
- reckless charge
- power through
- spot weakness
- reaper
- bandage up
- dark shackles
- flash of steel
- swift strike
- trip
- apotheosis
- hand of greed
- master of strategy
- apparition
- slimed
- normality
- pain
- regret

## ENTITY NEXT PRIORITIES

### RELICS

(5's are the mvp for release)

- 5 strike dummy
- 5 velvet choker
- 5 paper phrog
- 5 akabeko
- 5 nunchaku
- 5 pen nib


- 4 ornamental fan
- 4 orichalcum
- 4 odd mushroom
- 4 champion belt
- 4 letter opener
- 4 tori
- 4 fossilized helix
- 4 tungsten rod
- 4 the boot

- 3 gremlin horn
- 3 shuriken
- 3 kunai
- 3 stone calendar
- 3 charon's ashes
- 3 strange spoon
- 3 necrinomicon
- 2 bird-faced urn
- 2 lizard tail
- 2 magic flower
- 2 chem x
- 2 orange pellets
- 2 centennial puzzle
- 2 ink bottle
- 1 art of war
- 1 red skull
- 1 mummified hand
- 1 sundial
- 1 dead branch
- 1 med kit
- 1 mark of the bloom
- ? frozen eye
- ? runic dome

### STATUSES:

#### BUFFS:

- 5 strength
- 5 dexterity
- 5 artifact
- 5 plated armor
- 5 vigor


- 4 rage
- 4 metallicize
- 4 intangible
- 4 thorns
- 3 buffer
- 3 regen
- 3 flame barrier
- 3 combust
- 3 double tap / duplication
- 3 flame barrier
- 2 feel no pain
- 1 dark embrace
- 1 juggernaut
- 1 rupture

#### ENEMY BUFFS:

- 5 curl up


- 4 angry
- 4 sharp hide (guardian)
- 4 flight
- 3 mode shift (guardian)
- 3 explosive
- 3 enrage
- 3 spore cloud
- 1 time warp

### DEBUFFS:

- 5 vulnerable
- 5 weak
- 5 entangled
- 5 frail


- 3 constricted
- 3 no block
- 2 dexterity down
- 2 strength down
- 2 no draw

### REMAINING CARDS

- armaments
- havoc
- headbutt
- sword boomerang
- true grit
- warcry
- burning pact
- combust
- dark embrace
- dual wield
- evolve
- feel no pain
- fire breathing
- infernal blade
- rampage
- rupture
- searing blow
- second wind
- sentinel
- sever soul
- whirlwind
- barricade
- beserk
- brutality
- corruption
- demon form
- exhume
- juggernaut
- blind
- deep breath
- discovery
- dramatic entrance
- enlightenment
- forethought
- good instincts
- impatience
- jack of all trades
- madness
- mind blast
- panacea
- panic button
- purity
- chrysalis
- magnetism
- mayhem
- metamorphosis
- panache
- sadistic nature
- secret technique
- secret weapon
- the bomb
- thinking ahead
- transmutation
- violence
- bite
- dazed
- void
- ascender's bane
- clumsy
- curse of the bell
- decay
- doubt
- injury
- necronomicurse
- parasite
- shame
- writhe

### INCOMPLETE/HALF BAKED FEATURES

- Consider extracting and decoupling the card type from the game to something within the calculator domain
- Blood for blood doesn't update cost when you lose hp from your own cards
- For performance gains → consider only looking 3 or 4 card plays into the future, instead of the whole hand?
- ethereal
- _anything_ random
- X cards