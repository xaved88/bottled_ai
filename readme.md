To get this set up:

1) Have Python installed (Note: you might need to add Python to the system path variable things on Windows)
2) Through the steam workshop, make sure you have:
    - BaseMod https://steamcommunity.com/sharedfiles/filedetails/?id=1605833019
    - StSLib https://steamcommunity.com/sharedfiles/filedetails/?id=1609158507
    - ModTheSpire https://steamcommunity.com/sharedfiles/filedetails/?id=1605060445
    - Communication Mod https://steamcommunity.com/sharedfiles/filedetails/?id=2131373661
3) Checkout this repository, and clone it into the steam app folder in a new folder: `ai\requested_strike`. Ex: ` E:\Steam\steamapps\common\SlayTheSpire\ai\requested_strike`
4) Run the game with the mods enabled
5) Now your spire config file should be created: https://github.com/kiooeht/ModTheSpire/wiki/SpireConfig for how to navigate there
6) Find `config.properties` in the CommunicationMod folder. Add `command=python .\\ai\\requested_strike\\main.py` to the `config.properties` file there.
7) Add default.log to ai\requested_strike\logs 
8) Run the bot via the game's main menu -> Mods -> Communication Mod -> Config (next to "Return") -> Start external process

Now it should all be able to run!
