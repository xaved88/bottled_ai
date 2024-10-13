# Bottled AI
Customizable bot for roguelike deck-building game [Slay the Spire](https://store.steampowered.com/app/646570/Slay_the_Spire/).

## FAQ
### Does it win a lot? Is it super smart?
Depends on which character and strategy is in use. We've got a few different ones! Our current best is a watcher strategy with 52% winrate. You can see our most current [winrates here](docs/winrates.md).

### How does it work? Machine Learning? Gen AI?
Nah, just good old-fashioned manually constructed automated decision-making. For example:
- Selecting Cards, Boss Relics, and Upgrades works with a prioritized list, e.g. our strategy for Watcher might prefer taking Blasphemy over Tranquility.
- Some decisions have specific conditions attached to them, like in the Shining Light event: take the damage for the 2 random upgrades... but not if we don't have much health left.
- In combat, the bot figures out what the outcome would be for each of the different ways it could play its hand (with a graph traversal and a simulation we constructed). Then, the bot picks the outcome it likes best and plays the cards in that order.
  - To decide what the best outcome is, the bot weighs about 40 different values against each other. Simple example: the bot prefers a turn where it defeats an enemy, but not if we will take a bunch of damage to make it happen.

### Does the bot have access to secret information, e.g. the outcomes of random rolls, or what it will draw next?
No, it can only see what the player does.

### What are its current limitations/capabilities?
See [capabilities.md](docs/capabilities.md).

### Do you make videos about the bot?
Actually, yes. Check out the [YouTube channel](https://www.youtube.com/@BottledAI)!

## Setup

### Python Setup
1) Have Python installed (min version 3.11.8).
    - Windows: you will likely need to add Python to the Path Environmental Variable.
    - MacOS: you need Python 3.11+ within xcode. This requires xcode 14.0+ (this applied for python 3.9+, might need to be higher now), which in turn requires macOS Monterey (lower versions won't work!).
2) Have [PIP](https://pip.pypa.io/en/stable/installation/) (python package manager) installed.

### Project Setup
1) Clone this repository into the game's install folder, in a new folder: `\bottled_ai`.
   - Windows example: ` E:\Steam\steamapps\common\SlayTheSpire\bottled_ai`
   - MacOS example: Browse local files of StS via Steam -> Right click and Show Package Contents -> Resources -> bottled_ai
2) Get/subscribe these mods via the Steam Workshop:
    - [BaseMod](https://steamcommunity.com/sharedfiles/filedetails/?id=1605833019) 
    - [StSLib](https://steamcommunity.com/sharedfiles/filedetails/?id=1609158507)
    - [ModTheSpire](https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445)
    - [Communication Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=2131373661)
3) Run the game with the mods enabled - this will create your spire mod config files.
4) Navigate to your CommunicationMod folder. How to find it:
   - Windows: `%LOCALAPPDATA%\ModTheSpire\`
   - MacOS: `~/Library/Preferences/ModTheSpire/`
5) Modify `config.properties` in the CommunicationMod folder:
    - Windows: Add `command=python .\\bottled_ai\\main.py` to the `config.properties` file there.
    - MacOS: Add `command=python3 ./bottled_ai/main.py` to the `config.properties` file there.

### Running the bot
Start the bot via the game's main menu:
- → Mods
- → Communication Mod
- → Config (next to "Return")
- → Start external process

You can configure some run settings in [main.py](main.py).

The process has a timeout of 10s so if you simply see that delay but nothing's happening - something isn't working.
To debug, check the output in the ModTheSpire console, or the `communication_mod_errors.log` in the StS folder.

## Making your own bot
- See [how_to_make_your_own_bot.md](docs/how_to_make_your_own_bot.md).


## Contact
Just use the Discussions feature here on GitHub. We're happy to discuss or support!


## Tools

### Bot Controls
- Adjust which bot strategy is used, the amount of runs, and the seed in [main.py](main.py).
- Pause the bot in [run_controller.txt](run_controller.txt).
- Adjust the speed of certain actions in [presentation_config.py](presentation_config.py).

### Tests
- All tests can be found in the `/tests` directory.
- They're VERY useful for checking bot behavior without needing to run the game.


## Contributing
We're happy to see you use this code for your own projects!

We're also  happy to have you contribute to this repository! What we'd specifically love to see in _this_ project:
- Any increased card / functionality coverage.
- Performance improvements.
- New handlers that add give strategies more options for effectiveness (like better potion handling for example).
- Bugfixes!

See [capabilities.md](docs/capabilities.md) for a _rough_ overview of current functionality coverage.

Please note:
- We will be hesitant to integrate any new strategies - unless they bring in a particular new approach that would be beneficial for others to use / learn from. 
- We normally will not accept major changes to the systems or code structure. If you'd like to do this, please fork the repo and share it with us so that we can see what you've created!
- Please cover any new functionality with tests. If you're not sure how to do that, just submit your changes without tests anyway, and we can support you with adding them.

Just create a pull request with your changes, and we'll address them promptly. Thank you!