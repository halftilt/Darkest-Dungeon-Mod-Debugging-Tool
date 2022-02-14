# Darkest Dungeon Mod Debugging Tool

A mod debugging tool for Darkest Dungeon
(Currently identifies potential conflicts between all mods in your mod folder).

In its current state, this debugging tool prints out a simple text file which
lists all of the potential conflicts between **every** mod in your mod folder. 

There are plans to make the tool more robust
in the future and more user friendly.

****

A simple way to read it is as such:

The tool will go into each mod folder and currently looks issues for with following categories:

Dungeon Mashes, Inventory Items, Monster Brains, Effects, Buffs, Quirks and trinkets.

Next, the tool will check for conflicts ***between*** each folder and then print out those potential conflicts.
****
#Download
You can **download** the current version of this tool here:
https://www.patreon.com/posts/61690056
# Using the Debugger
Simply run the file and select your folder which stores all of your Darkest Dungeon mods.
That folder would likely be located at 
**"D:\Games\steamapps\common\DarkestDungeon\mods"**

Once it is finished running, the program will create a text file named "mod_conflicts.txt".
You can simply scan through the file and look for any potential conflicts within.

***Note:***
*Any files you've download via the Steam Workshop will not be scanned unless you drag them into your mod folder.*
# (For Developers) Creating the Executable
Simply use pyinstaller and select the "mod_conflict_finder.py" file as your executable.