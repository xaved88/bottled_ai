## Setup Guidelines

### Getting Python Setup:
1) Have Python 3.11.8 or so installed
    - Windows: you might need to add Python to the system path variable things
    - MacOS: you need Python 3.11.8+ within xcode. This requires xcode 14.0+ (14.0+ applied for 3.9, you might need a higher version now), which in turn requires MacOS Monterey (lower versions won't work!)
2) Have PIP (python package manager) installed: https://pip.pypa.io/en/stable/installation/

### Getting the Project Setup:
1) Checkout this repository, and clone it into the steam app folder in a new folder: `ai\requested_strike`.
    - Windows ex: ` E:\Steam\steamapps\common\SlayTheSpire\ai\requested_strike`
    - MacOS ex: Browse local files of StS via Steam -> Right click and Show Package Contents -> Resources -> ai -> requested_strike
2) Run `python -m pip install -r requirements.txt` in the root folder of the project (installs python dependencies)

### Getting The Game Setup
1) Through the steam workshop, make sure you have:
    - BaseMod https://steamcommunity.com/sharedfiles/filedetails/?id=1605833019
    - StSLib https://steamcommunity.com/sharedfiles/filedetails/?id=1609158507
    - ModTheSpire https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445
    - Communication Mod https://steamcommunity.com/sharedfiles/filedetails/?id=2131373661
2) Run the game with the mods enabled
3) Now your spire config file should be created! See https://github.com/kiooeht/ModTheSpire/wiki/SpireConfig for how to navigate there
4) Find `config.properties` in the CommunicationMod folder. Then:
    - Windows: Add `command=python .\\ai\\requested_strike\\main.py` to the `config.properties` file there.
    - MacOS: Add `command=python3 ./ai/requested_strike/main.py` to the `config.properties` file there.

### Running the Bot
- Run the bot via the game's main menu
  - -> Mods 
  - -> Communication Mod 
  - -> Config (next to "Return") 
  - -> Start external process

Now it should all be able to run!

The process has a timeout of 10s so if you simply see that delay but nothing's happening, then something isn't working.
To debug, check the output in the ModTheSpire console, or the `communication_mod_errors.log` in the StS folder.

### Screenshots
- You'll need to adjust the display settings in game to be bordered window (not fullscreen, not borderless window)
- In the config parameters in main.py, turn "take_screenshots" to True
- Only the last run will have its screenshots saved, and they're in logs/screenshots (starting a new run will delete anything in there)
- Doesn't run on Mac, so also various previous steps about python dependencies may not be required

### Testing
- All tests can be found in the /tests directory
- You can run coverage checks with:
  - `python -m coverage run -m unittest discover .\tests`
  - `python -m coverage report`
  - `python -m coverage html`
- We don't know if we trust them yet, but yeah

### Analyzing
You can run `analyze.py` to do analysis on recent runs. Simply supply a list of seeds to the variable at the top.

It can be used for just seeing how a session went, but it will naturally get the last two instances of a seed and compare them. 
So, it's made for doing a set of runs, changing the logic and rerunning them, then comparing performance results.