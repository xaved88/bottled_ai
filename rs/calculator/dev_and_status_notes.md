This is where we'll keep the status of the calculator organized for a bit, what next steps are, total prio lists, etc.

### We are disregarding:

- card draw
- ethereal
- _anything_ random
- X cards

### KEY:

normal = okay

*italic* = to investigate

**bold** = we need to make adjustments for

~~strikethrough~~ = done

## VITAL RELICS AND STATUS (all done!)

- ~~strike dummy~~
- ~~velvet choker~~
- ~~paper phrog~~
- ~~nunchaku~~
- ~~pen nib~~
- ~~strength~~
- ~~dexterity~~
- ~~vulnerable~~
- ~~weak~~
- ~~frail~~
- ~~entangled~~
- ~~vigor~~
- ~~curl up~~
- ~~artifact~~
- ~~plated armor~~

## VITAL CARDS

- ~~strike_r~~
- ~~defend_r~~
- ~~bash~~
- ~~anger~~ (won't duplicate cards)
- ~~cleave~~
- ~~clothesline~~
- ~~heavy blade~~
- ~~iron wave~~
- ~~perfected strike~~
- ~~pommel strike~~
- ~~shrug it off~~
- ~~thunderclap~~
- ~~twin strike~~
- ~~blood for blood~~ (cost doesn't lower when taking damage in turn yet :shrug:)
- ~~bloodletting~~
- ~~carnage~~ (no ethereal handling yet)
- ~~disarm~~
- ~~dropkick~~
- entrench :: can do with hooks
- flame barrier (maybe just say "add thorns" for the time being?)
- ghostly armor (no ethereal handling yet)
- hemokinesis
- inflame
- intimidate
- pummel
- seeing red
- shockwave
- ~~uppercut~~
- bludgeon
- feed :: can do with hooks
- **fiend fire** (need pre & post hooks definition, as right now they're all post)
- immolate
- impervious
- limit break
- offering
- **reaper** (need specific healing (damage dealt counter?))
- **apparition** (need intangible, no ethereal)
- **bite** (need healing? or can we just do it with -hp cost)
- jax
- **burn** (need end of turn in hand handling)
- **normality** (need in hand handling, plus cardplay counter?)
- **pain** (need in hand handling )
- **regret** (need end of turn in hand handling)

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
- 3 the boot
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
- 3 buffer
- 3 regen
- 3 thorns
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

### CARDS:

#### GENERAL CARDS

strike_r
defend_r
bash
anger
armaments
body slam
clash
cleave
clothesline
flex
havoc
headbutt
heavy blade
iron wave
perfected strike
pommel strike
shrug it off
sword boomerang
thunderclap
true grit
twin strike
warcry
wild strike
battle trance
blood for blood
bloodletting
burning pact
carnage
combust
dark embrace
disarm
dropkick
dual wield
entrench
evolve
feel no pain
fire breathing
flame barrier
ghostly armor
hemokinesis
infernal blade
inflame
intimidate
metallicize
power through
pummel
rage
rampage
reckless charge
rupture
searing blow
second wind
seeing red
sentinel
sever soul
shockwave
spot weakness
uppercut
whirlwind
barricade
beserk
bludgeon
brutality
corruption
demon form
exhume
feed
fiend fire
immolate
impervious
juggernaut
limit break
offering
reaper

#### Colorless cards

bandage up
blind
dark shackles
deep breath
discovery
dramatic entrance
enlightenment
flash of steel
forethought
good instincts
impatience
jack of all trades
madness
mind blast
panacea
panic button
purity
swift sttrike
trip
apotheosis
chrysalis
hand of greed
magnetism
master of strategy
mayhem
metamorphosis
panache
sadistic nature
secret technique
secret weapon
the bomb
thinking ahead
transmutation
violence
apparition
bite
jax

#### STATUS CARDS

burn
dazed
wound
slimed
void

#### CURSES

ascender's bane
clumsy
curse of the bell
decay
doubt
injury
necronomicurse
normality
pain
parasite
regret
shame
writhe

### INCOMPLETE/HALF BAKED FEATURES

- Consider extracting and decoupling the card type from the game to something within the calculator domain
- Blood for blood doesn't update cost when you lose hp from your own cards
- PerfectedStrike is doing string comparison, probably wants a enum list at some point