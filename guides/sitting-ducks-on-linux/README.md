# Installing and running Sitting Ducks on Linux

## LibreSplit resources
[Splits](https://github.com/LibreSplit/LibreSplit-resources/tree/main/splits/Sitting_Ducks)  
[Autosplitter](https://github.com/LibreSplit/LibreSplit-resources/tree/main/auto-splitters/Sitting_Ducks)  
From my testing, autosplitter may not work when running game through Steam from `SittingDucks.exe`, run directly from `OVERLAY.exe`

## Prerequisites
* Steam or other application to run Proton runtimes
* ProtonUp-Qt (for GE-Proton, required for ingame music to play)
* Protontricks or other way of installing dependencies into Proton prefixes
* Game installer or game files
* mangohud, for FPS limiter
* gamescope, for windowed mode

## Installation
I will be using Steam, adjust for your Proton/Wine runtime. If you have a disk image, I suggest unpacking the files to your hard drive

1. Go to Steam Library, at the bottom of UI click Add a Game -> Add a Non-Steam Game, in a new window, click Browse. Find your game exe or installer, click Open, then Add Selected Programs. Find your newly added file in your library. If you have already preinstalled game files, skip ahead to step 4
2. Right click the file in Steam Library, click Properties. Go to Compatibility, check "Force use of a specific Steam Play compatibility tool", choose Proton Experimental
3. Launch the setup. Run through it normally. Do not adjust installation directory, do not install DirectX if asked. Finish installation
4. Open ProtonUp-Qt. Choose Installation for: Steam (or other runner you might use). Click Add version, choose GE-Proton and whatever the latest version is (GE-Proton10-32 at the time of writing). Click install. After finishing, exit application, restart Steam
5. Open Protontricks. Find the app "Non-Steam shortcut" corresponding to your game. Note the ID number next to it, select it and click OK. Select "Select the default wineprefix", click OK. Select Install a Windows DLL or component, click OK. Select mfc42, click OK. An installer may pop up in German, click Ja. After everything is done, close Protontricks
6. Find your game installation. If you adjusted it in step 3 or have preinstalled files, go to the location you chose. If you left installation to default, the location will be inside your default Steam library (`~/.steam/steam/steamapps`), in `compatdata`, in subdirectory matching ID from step 5, `pfx/drive_c`, then navigate to installation directory.
7. Remove all files from Videos directory, the game won't start with them present, and entire Savegame directory, for speedrun reasons
8. Go back to Steam, right click on your game, then Properties. Update name to `Sitting Ducks`, click Browse next to Start in and navigate to game installation directory, then copy that path to Target and append `SittingDucks.exe`. Go to Compatibility and change Proton Experimental to the version of GE-Proton you downloaded.
9. You need to run the game at least once through `SittingDucks.exe` launcher and open Controls settings to set controls for game. You can also adjust graphic settings here. After running game once and ensuring it works, you can go back to Steam Properties and change Target to `OVERLAY.exe`

## Patching the game
TODO: This is an older version of the patcher, new patched exes are on the Discord server. These are untested against LibreSplit autosplitter yet.

1. Download `patcher.py` from https://github.com/SansForSSBU/SittingDucks_Patcher/blob/7a380f38a4b3fe9389641f8e22359524ef3eb2b5/patcher.py to your game directory
2. Open the file, change `game_folder` to be `.`, ensure `instant_loading` and `speed_issue_fix` are set to true
3. Run with Python. You should get new `OVERLAY.exe` and `backup_overlay.exe`

## Framelimiter
You can use mangohud to lock your FPS to 60. Install mangohud through your package manager, go to your games Properties and update Launch options to `MANGOHUD_CONFIG='fps_limit=60' mangohud %command%`

## Playing in window

You can use gamescope to set the game to windowed mode. First set resolution through SittingDucks.exe to your preferred resolution, then update your games Launch option to `gamescope -W x -H y -w x -h y -b -- mangohud %command%` where `x` and `y` is your chosen resolution  
With mangohud framelimiter together it will look like `MANGOHUD_CONFIG='fps_limit=60' gamescope -W 1280 -H 1024 -w 1280 -h 1024 -b -- mangohud %command%`