## Capabilities
See [this YouTube Video](https://youtu.be/830r7OCz-h4) for a general overview of capabilities and their current state.

### Ironclad
- Missing cards: several, but also specifically: Infernal Blade, True Grit

### Silent
- Missing cards: Distraction, All Out Attack, Well Laid Plans, Masterful Stab, Doppelganger, Setup, Nightmare, Alchemize,
- Strategies around poison use would require additional comparator adjustments: e.g. who to best target with Corpse Explosion? When do we want to apply Catalyst?

### Defect
- Missing cards: Force Field, Hologram, Rebound, Seek, Static Discharge, White Noise

### Watcher
- Missing cards: Conjure Blade, Foreign Influence, Meditate, Omniscience, Vault

### General
- **Calculation limit:** The bot will stop thinking after it has evaluated 11,000 battle paths (configurable as `max_path_count` in multiple places) for one play. This will often result in it just playing the card that's all the way on the right. This is an intentional trade-off vs waiting a long time. Most likely to happen when you've got a LOT of cards in hand, the potential to play a lot of them, and 3+ enemies.
- **Heart**: The bot doesn't know how to find the keys
- **Bug**: Prayer Wheel card reward is only checked if first card reward is picked up
- **Missing colorless cards**: Chrysalis, Discovery, Forethought, Jack of All Trades, Madness, Metamorphosis, Panic Button, Purity, Secret Technique, Secret Weapon, The Bomb, Thinking Ahead, Transmutation, Violence

### Misc improvement ideas
- Know that Writhing Mass will change intent after each hit. Could do: stop dealing damage when we can block the hit. Also avoid the curse.
- Know when Time Eater is going to heal, so don't waste resources on him.
- Add purchasing of potions (e.g. Ritual Potion) to the shop purchase handler.
- Make `common_` handlers for events, potions, and shop purchasing so they can stop being duplicated.

We maintain a big backlog of issues, let us know if you want inspiration. :D