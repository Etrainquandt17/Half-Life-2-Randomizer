# Half-Life 2 Randomzier
This is a randomizer for Half-Life 2. Currently, it supports base Half-Life 2 and Synergy. Support for the episodes and Black Mesa are planned. Target support is for Half-Life 2 20th Anniversary, but most features of the main randomizer will still work for Pre-Anniversary. The only thing missing should be some skyboxes added to 20th Anniversary. Additional randomization options will not work for Pre-Anniversary or Synergy and support is not planned.
## How to use
### Base Half-Life 2
Download the repo by clicking on "Code" and "Download ZIP". Extract the ZIP file. Go to the common folder in your steamapps folder. Copy the folder from the ZIP file for the game you want to randomize (currently Half-Life 2 and Synergy) into your common folder on the drive where you have the game installed. Everything should be put into the right place after that. Make sure you have Python installed, Python 3.10.4 is what was used to develop this, I'm unsure if anything else would work but it wouldn't hurt to try if you don't have that specific Python version installed. Once you ensure that you have python installed, if you're on Windows go to either the maps folder (for the main randomization, is in the ent_cache folder for Synergy) or the root Half-Life 2 folder for additional randomization options. Once you're in the folder, click the empty space to the *left* of the search bar, but *inside* the bar that shows the path. Type in "cmd" to open a command prompt window inside that path automatically. Type in "py extractlmp.py" in the maps folder to extract the entity lump from the bsp (or just type "py randomizer_bsp.py" if you don't want to extract the lumps, but I highly recommend that you just use the lump version, the bsp version is slow and may be filled with unintended crashes or bugs, it was just something I created to prove to myself I still could have done this if there wasn't an easier option.) After you extracted the entity lumps, type in "py randomizer.py" for the main randomization options. Follow the prompts. If you would like to randomize additional stuff, go to the root of the Half-Life 2 folder, open command prompt there and type "py additional_randomization.py" and follow the prompts and you should be good to go! If you're on Linux this should be baby stuff for you.
### Episode One
Go to the episodic maps folder and run extractlmp.py. Now go to the hl2_complete maps folder and do the same things as for base Half-Life 2. The reason it has to be done this way is because the EP1 vpk files have a bunch of lump files in them that overwrite the randomized lump files. To get around this we have to move the lump files to the hl2_complete folder in order to overwrite the lump files inside the vpk. Due to this, the bsp version of the randomizer will be unavailable. For additional randomization options just run additional_randomization_ep1.py instead.
### Synergy
Pretty much the same thing as base Half-Life 2, just the additional randomization options are unavailable due to complications with the binaries.
## Main Randomization Options
### Seed
Either enter a number, or just press enter for a random seed. ~~If you're playing Synergy, all users may need to use the same seed.~~ This does not seem to be the case, but keep it in mind in case any issues arise.
### Randomize NPCs
Randomizes NPCs, complete with a logic system to prevent softlocks to the best of its ability. Does not randomize specific important NPCs (Alyx, Barney, Eli, etc.), does not randomize other less important NPCs on specific maps to prevent softlocks (Combine Soldiers on d1_town_05 for example) and does not allow randomization of certain large NPCs on specific maps.
### Randomize Items
Randomizes items. No logic.
### Randomize Weapons
Randomizes weapons. Does not allow crossbows to be randomized onto NPCs as killing an NPC with the crossbow will crash the game. Also does not randomize weapons on some NPCs on specific maps to prevent softlocks. Breakable wood boards and vents are completely removed to prevent softlocks in earlier levels. The invisible walls and props blocking the entrance and exit to the cave in d2_coast_11 are also removed as having the bugbait before getting it where you're supposed to get it will softlock the game.
### Randomize Props
Randomizes props. Does not randomize things to certain large props on certain maps. Skips randomization for certain props in certain maps due to a high softlock probability if they're changed.
### Randomize Skyboxes
Randomizes skyboxes.
### Randomize Decals
Randomizes decals, those flat textures you see on the walls ground a ceiling sometimes.
### Randomize Chargers
Swaps around health and suit chargers randomly.
### Randomize Dynamic Resupplies
There's an item called "item_dynamic_resupply" in the game and sometimes it's found in resupply crates. This randomization option replaces these with a static item or weapon, or even an NPC trap if you decide you would like that. NPC traps cannot contain barancles or floor turrets to prevent crashes, however everything else is fair game, even NPCs that are normally too big to be in the map. Be wary...
### Randomize Sounds and/or Music
Randomizes all sounds and/or music the the map file. The sounds option will randomize sounds only, and keep the music in tact. The music option will randomize only the music. Both will randomize both of them together, meaning a sound effect can now be music or music can now be a sound effect. The sounds and both option also randomizes soundscapes.
### Randomize Lights and Colors
Randomizes lights and colors. Things affected are props, NPCs, the Sun, dynamic shadows and other various things.
### Randomize Ammo Crates
Randomizes the infinite resupply crates, usually containing RPG ammo or SMG ammo. Can be any ammo type other than the AlyxGun ammo type, however some may not have a model which makes them non functional. Be warned, this option can cause impossible situations or force you to backtrack really far for ammo.
### Fix Models
This option is only needed if you randomized NPCs. If you did randomize NPCs and decide you don't want to fix models, you're going to have a rough time with model caching issues.
## Additional Randomization Options
Please don't sleep on the first two options, one of them is considered in main logic and the other is just nice to have.
### Kill Vital NPCs
Makes the player have a hate relationship with vital NPCs. Useful for that one GMan who won't move out of the way even for a grenade, or if you're eyeing that Gravty Gun Alyx has...
### Fix AlyxGun Viewmodel
Makes the AlyxGun have the viewmodel and animation of the pistol so you can actually see.
### Lift Heavy Objects
Pick up things many times the weight of yourself with both your hands and the Gravity Gun. Also increases the Gravity Gun's trace length. Just... don't try to pick up the buggy, okay?
### Randomize Entity Drops
Randomizes various entity drops throughout the game currently randomizes all of the Combine Soldier drops, what Metrocops spawn in place of Manhacks, what NPCs zombies will spawn when dying, the battery from scanners and what headcrabs come out of headcrab canisters.
### Shuffle Firerates
Shuffles the firerates of specific guns and weapons in the game. There was no point in suffling the RPG's and Stunstick's firerate. The AlyxGun's and AR2's firerate are tied together in code. All other weapons not shuffled did not have a firerate for me to modify in the code. Also makes the crowbar a ranged weapon for the fun of it.
### Remove Suit Sprint Energy Usage
Does what it says and says what it does.
### Remove Max Health Cap and Set Max Armor to 750
Really helps to balance the next four options below...
### Randomize Health Values
Randomizes the health values of various NPCs in the game.
### Randomize Damage Values
Randomizes the damage values of various NPCs and the player.
### Randomize Charger and Pickup Values
Randomizes the amount juice health and suit chargers have as well as the values of various pickups in the game. 
### Randomize Damage Adjusters
Randomizes damage multipliers for various body parts, for both the player and NPCs.
### Randomize Max Ammo Values
Randomizes the maximum amount of ammo you can carry for various weapons in the game.
### Randomize Weapon Clip Sizes
Randomizes the weapon clip size for various weapons in the game.
### Shuffles Ammo Types
Shuffles the type of ammo weapons use in the game. Fun fact, the damage weapons do it based on the ammo type it uses, not the weapon itself.
### Randomize Weapon Sounds
Randomize the sounds of the various weapons in the game.
### Randomize Surface Density Values
Randomizes the surface density of all of the surfaces in the game. This is not considered in logic and can make some of the water puzzles impossible or require creative solutions, sometimes locked behind other randomization options.
### Randomize Surface Dampening Values
Randomizes the surface dampening values.
### Randomize Surface Elasticity Vlaues
Randomizes Surface elasticity values.
### Randomize Surface Friction Values
Randomizes surface friction values. Can make platforming sections really hard.
### Randomize Surface Thickness Values
Randomizes surface thickness values.
### Randomize Surface Sounds
Randomizes surface sounds.
### Randomize Other Sounds
Randomizes ohther various sound sources that are not in the map files. May overwrite previous sound randomization options.
## Reporting Issues
When reporting issues, make sure to include the seed txt file as well as tell me if you used the lump randomizer, the bsp randomizer or the Synergy randomizer as the seeds are different. Tell me what options you have enabled as well and tell me what additional randomization settings you had on.
## Known Issues
### In one of the Canal maps there was a massive building blocking the exit
Yeah uh... sorry about that. I knew about that, but somehow lost the things I needed to prevent that issue from happening again. If you come across that please let me know so I can patch it out.
### Antlions Have Model Caching Issues
I think I narrowed this down to citizens getting replaced with antlions, so I prevented it, however I may be wrong on that so report an issue if that happens.
### The Buggy Freaks Out
I have no clue what causes this and it only happened one time. If you happen to know why the buggy acts like this sometimes please let me know.
### Player Physics Get Screwed Up
Thanks Source Engine we love you! You'll be stuck like that until you go through a transition. Just don't bonk into any props and you'll get there.
### The return trip to d2_coast_07 from d2_coast_08 crashes the game a lot of the time
I really don't know what's happening here. It happens a lot and I cannot figure out how to fix it. If you know why please help out. For now, try to skip that map if you can.
### Fixing models doesn't work sometimes
I don't know why this happens, it's rare and only happens for like one model every randomization.
### Running over an ichthyosaur with either the jeep or airboat crashes the game
It's rare enough for me to not worry about this bug and honestly, it's kinda funny when the game crashes with way.
### Model preaching issue with zombies
For some reason, the model is not automatically pre-caching for headcrab replacements, despite me doing everything that I should have had to do to make the model precache. It prints in the console that the model name is null and I have no idea why. If you know why it would be nice if you could tell me, as I have no idea what could be happening. For now, just try killing the zombie so it either doesn't drop the ragdoll, or kill the zombie in a way where it will drop the headcrab alive, which will also precache the model so you can kill future zombies worry free.
## Q&A
### Why does the battery and suit charger always fill up to full when removing max health cap and setting max armor to 750?
x86 ASM is like that and required me to deleted the future instruction, which so happens to be the instructions that controls how much the battery should give. The suit charger was because there was no better option.
### Why shuffle firerate and not just purely randomize?
Another ASM moment, I can't just randomize the floats themselves because many other instructions access those floats. I'm sure you wouldn't enjoy being blinded by the RPG's lazer sight.
### The cart takes a really time to arrive in Ravenholm. Why?
I don't know why this happens or why where the cart takes you is visually unloaded. You can either wait a while for the cart or grenade jump to the other side.
### There was a prop in the way of the door to d2_coast_08 that I could get past, but when returning the prop is unpassable the other way. What do I do?
There's still some hope. If you have enough health and a rocket launcher, there is a small sliver a land to the far left of the door that is not blocked off by invisible walls. If you get over there, you can get to the transition zone from the other side. However, I would like it if you would report this as an issue as I consider this an issue.
### Alyx won't progress properly in the buildings prior to the standoff in c17. What do I do?
If you have prop randomization on, you can just run to where the standoff is supposed to be and jump over the gate with a well timed explosion from blowing yourself up with a hopper. All other randomization options should work properly in this section of the game.
### Why does Episode One feel a lot less randomized than base Half-Life 2?
Because it is. Valve decided that Episode One needed a lot of anti-fun checks, put massive invisible walls, hell, even decided that the antlion guard needed 99999 health before it kills the APC (the APC dying doesn't matter, that's why I removed it). Even Alyx not being able to pick up a shotgun would softlock the game. There's only like 4 maps where combine soldiers are able to be randomized. There's only so much I can do.
### In ep1_c17_01 Alyx won't climb up the stairs after cranking that thang. What do I do?
Just push her up the stairs and she will walk up automatically eventually. If for whatever reason she is stuck, she will eventually teleport after going past the crushing wall.
### In ep1_c17_02 Alyx won't jump down after killing the antlion guard. What do I do?
Not to worry, the combine wall to the next area will still open after plugging the antlion holes and Alyx will teleport after falling through the air vent.
### There are a lot of crashes and softlocks, did you even test this?
I promise that I tested this a lot, I have played the game pretty much over 5 times, and prevented all crashes and softlocks I could find. However, there were some crashes that I could not figure out to fix for the life of me. I tried my best to fix these crashes but I could not figure out what even caused it in the first place. If you happen to see an issue that has been open for a while with no solution, and you know your way around this game, it would be great if you could look into it to help figure out what exactly caused the crash, so I can prevent it in the future.
### What do I do if the game updates?
The main randomization options should be fine to use, however the ASM options in the additional randomization options may not be safe to use. If the game updates since you last use this randomizer please check this page to see if you should use the ASM options or not. Using the ASM options for a game update it's not made for can cause game crashes or cause the options to not work correctly.
## ASM Option Status
ASM options should be safe to use.