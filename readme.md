To get this set up:

1) Have Python 3.9 or .10 or so installed (Note: you might need to add Python to the system path variable things on Windows)
2) Through the steam workshop, make sure you have:
    - BaseMod https://steamcommunity.com/sharedfiles/filedetails/?id=1605833019
    - StSLib https://steamcommunity.com/sharedfiles/filedetails/?id=1609158507
    - ModTheSpire https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445
    - Communication Mod https://steamcommunity.com/sharedfiles/filedetails/?id=2131373661
3) Checkout this repository, and clone it into the steam app folder in a new folder: `ai\requested_strike`.
    - Windows ex: ` E:\Steam\steamapps\common\SlayTheSpire\ai\requested_strike`
    - MacOS ex: Browse local files of StS via Steam -> Right click and Show Package Contents -> Resources -> ai -> requested_strike
4) Run the game with the mods enabled
5) Now your spire config file should be created! See https://github.com/kiooeht/ModTheSpire/wiki/SpireConfig for how to navigate there
6) Find `config.properties` in the CommunicationMod folder. Then:
    - Windows: Add `command=python .\\ai\\requested_strike\\main.py` to the `config.properties` file there.
    - MacOS: Add `command=python3 ./ai/requested_strike/main.py` to the `config.properties` file there.
7) Run the bot via the game's main menu -> Mods -> Communication Mod -> Config (next to "Return") -> Start external process

Now it should all be able to run!

The process has a timeout of 10s so if you simply see that delay but nothing's happening, then something isn't working.
To debug, check the output in the ModTheSpire console, or the `communication_mod_errors.log` in the StS folder.
