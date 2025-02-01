import os
import random
import struct
import re
import datetime
import shutil

GLOBAL_SEED = None
LOG_FILE = None

def log_print(msg):
    global LOG_FILE
    print(msg)
    if LOG_FILE is not None:
        LOG_FILE.write(msg + "\n")

def read_lines(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def read_important_npcs(file_path):
    with open(file_path, 'r') as file:
        return {f'"{line.strip()}"' for line in file}
    
def read_big_npcs():
    return {f'"{line.strip()}"' for line in read_lines("big_npcs.txt")}

def read_concrete_models():
    return {f'"{line.strip()}"' for line in read_lines("concrete.txt")}

def read_npc_map_files():
    npc_files = [
        "npc_antlion.txt",
        "npc_citizen.txt",
        "npc_combine_s.txt",
        "npc_combinedropship.txt",
        "npc_combinegunship.txt",
        "npc_headcrab.txt",
        "npc_manhack.txt",
        "npc_metropolice.txt",
        "npc_rollermine.txt",
        "npc_sniper.txt",
        "npc_strider.txt",
        "npc_turret_floor.txt",
        "npc_zombie.txt"
    ]
    npc_map_dict = {}
    for npc_file in npc_files:
        npc_name = f'"{os.path.splitext(npc_file)[0]}"'
        npc_map_dict[npc_name] = read_lines(npc_file)
    return npc_map_dict

def randomize_file(file_path, replacements, check_next_line=False, important_npcs=None, npc_map_dict=None, npc_model_dict=None, is_weapon=False, prompt=None):
    with open(file_path, 'rb') as file:
        content = file.read()

    # Create a dictionary to track what should be excluded from randomization
    excluded_positions = set()

    # First pass - mark positions that should be excluded
    if important_npcs:
        important_pattern = re.compile(b'|'.join(re.escape(npc.encode('utf-8').strip()) for npc in important_npcs), re.IGNORECASE)
        for match in important_pattern.finditer(content):
            start, end = match.span()
            excluded_positions.update(range(start, end))
            log_print(f"Detected important NPC '{match.group(0).decode('utf-8').strip()}' at position {start}-{end} in {file_path}. Will skip randomization.")

    if npc_map_dict:
        for npc, maps in npc_map_dict.items():
            map_name = os.path.basename(file_path)
            if map_name in maps:
                npc_pattern = re.compile(re.escape(npc.encode('utf-8').strip()), re.IGNORECASE)
                for match in npc_pattern.finditer(content):
                    start, end = match.span()
                    excluded_positions.update(range(start, end))
                    log_print(f"Detected troublesome map '{map_name}' for NPC '{npc}' at position {start}-{end}. Will skip randomization.")

    # Handle stunstick special case
    if is_weapon and os.path.basename(file_path) == "d1_trainstation_04_l_0.lmp":
        stunstick_pattern = re.compile(b'"weapon_stunstick"', re.IGNORECASE)
        for match in stunstick_pattern.finditer(content):
            start, end = match.span()
            excluded_positions.update(range(start, end))
            log_print(f"Found 'weapon_stunstick' in 'd1_trainstation_04_l_0.lmp'. Will skip randomization as it's needed for progression.")

    # Create the combined pattern for replacements
    if replacements:
        combined_pattern = re.compile(b'|'.join(re.escape(original.encode('utf-8').strip()) for original in replacements.keys()), re.IGNORECASE)

        def replacer(match):
            start, end = match.span()
            
            # Check if this position should be excluded
            if any(pos in excluded_positions for pos in range(start, end)):
                return match.group(0)

            original_bytes = match.group(0)
            original = original_bytes.decode('utf-8').strip().lower()
            line_start = content.rfind(b'\n', 0, start) + 1
            line_end = content.find(b'\n', end)
            line = content[line_start:line_end]

            if b"excludednpc" in line:
                log_print(f"Skipping randomization for '{original}' at position {start}-{end} in {file_path} due to 'excludednpc' tag in line.")
                return match.group(0)
            if b"filterclass" in line:
                log_print(f"Skipping randomization for '{original}' at position {start}-{end} in {file_path} due to 'filterclass' tag in line.")
                return match.group(0)

            # Initialize replacement outside of conditionals
            replacement = random.choice(replacements[original]).strip()
            replacement_bytes = replacement.encode('utf-8').strip()

            map_name = os.path.basename(file_path)
            big_maps = set(read_lines("big_maps.txt"))
            big_npcs = read_big_npcs()
    
            if map_name in big_maps and replacement in big_npcs:
                log_print(f"Got big NPC '{replacement}' in big map '{map_name}', retrying randomization...")
                while replacement in big_npcs:
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()

            if check_next_line:
                # Check the next line's text
                next_line_start = content.find(b'\n', end) + 1
                next_line_end = content.find(b'\n', next_line_start)
                next_line = content[next_line_start:next_line_end]
                log_print(f"Checking next line: {next_line}")

                while replacement == '"weapon_crossbow"' and (b"npc" in next_line):
                    log_print(f"Tried randomizing weapon_crossbow onto an NPC. Original weapon: '{original}' Position: {start}-{end} File: {file_path}")
                    log_print(f"Retrying randomization for '{original}' as killing an NPC with a crossbow will crash the game.")
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()

            # Check for "d1_canals_01a_l_0.lmp" and "d1_canals_02_l_0.lmp"
            if os.path.basename(file_path) == "d1_canals_01a_l_0.lmp" or os.path.basename(file_path) == "d1_canals_02_l_0.lmp":
                if replacement in ['"npc_combine_camera"', '"npc_rollermine"', '"npc_poisonzombie"', '"npc_fastzombie_torso"', '"npc_ichthyosaur"', '"npc_turret_ceiling"']:
                    log_print(f"Retrying randomization for '{original}' at {start}-{end} in '{os.path.basename(file_path)}' because these npcs crash the game if a barnacle eats them and there are a lot of barnacles here.")
                    while replacement in ['"npc_combine_camera"', '"npc_rollermine"', '"npc_poisonzombie"', '"npc_fastzombie_torso"', '"npc_ichthyosaur"', '"npc_turret_ceiling"']:
                        replacement = random.choice(replacements[original]).strip()
                        replacement_bytes = replacement.encode('utf-8').strip()

            # Check for "d2_prison_07_l_0.lmp", "d2_prison_08_l_0.lmp" and "d3_c17_11_l_0.lmp"
            if os.path.basename(file_path) == "d2_prison_07_l_0.lmp" or os.path.basename(file_path) == "d2_prison_08_l_0.lmp" or os.path.basename(file_path) == "d3_c17_11_l_0.lmp":
                if replacement in ['"weapon_357"', '"weapon_alyxgun"', '"weapon_bugbait"', '"weapon_frag"', '"weapon_physcannon"', '"weapon_crowbar"', '"weapon_stunstick"', '"weapon_crossbow"', '"weapon_pistol"', '"weapon_rpg"']:
                    log_print(f"Retrying randomization for '{original}' at {start}-{end} in '{os.path.basename(file_path)}' because these weapons prevent the combine soldiers from moving.")
                    while replacement in ['"weapon_357"', '"weapon_alyxgun"', '"weapon_bugbait"', '"weapon_frag"', '"weapon_physcannon"', '"weapon_crowbar"', '"weapon_stunstick"', '"weapon_crossbow"', '"weapon_pistol"', '"weapon_rpg"']:
                        replacement = random.choice(replacements[original]).strip()
                        replacement_bytes = replacement.encode('utf-8').strip()

            # Check for "d1_trainstation_06_l_0.lmp"
            if os.path.basename(file_path) == "d1_trainstation_06_l_0.lmp" and original == '"weapon_crowbar"' and replacement in ['"weapon_bugbait"', '"weapon_pistol"', '"weapon_frag"', '"weapon_stunstick"']:
                log_print(f"Tried randomizing 'weapon_crowbar' to '{replacement}' in 'd1_trainstation_06_l_0.lmp'. Retrying with a different weapon as this weapon will cause you to not be able to continue.")
                while replacement in ['"weapon_bugbait"', '"weapon_pistol"', '"weapon_frag"', '"weapon_stunstick"']:
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()

            # Check for "d2_coast_05_l_0.lmp"
            if os.path.basename(file_path) == "d2_coast_05_l_0.lmp" and replacement in ['"models/props_buildings/row_corner_1_fullscale.mdl"']:
                log_print(f"Tried randomizing '{original}' to '{replacement}' in 'd2_coast_05_l_0.lmp'. Retrying with a different prop as it will block your way.")
                while replacement in ['"models/props_buildings/row_corner_1_fullscale.mdl"']:
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()

            # Check for "d2_coast_07_l_0.lmp"
            if os.path.basename(file_path) == "d2_coast_07_l_0.lmp" and replacement in ['"models/props_buildings/row_res_1_fullscale.mdl"']:
                log_print(f"Tried randomizing '{original}' to '{replacement}' in 'd2_coast_07_l_0.lmp'. Retrying with a different prop as it will block your way.")
                while replacement in ['"models/props_buildings/row_res_1_fullscale.mdl"']:
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()

            # Check for "d3_breen_01_l_0.lmp"
            if os.path.basename(file_path).lower() == "d3_breen_01_l_0.lmp" and original == '"weapon_physcannon"':
                log_print(f"Skipping randomization for '{original}' in '{os.path.basename(file_path)}' because it's needed here.")
                while original == '"weapon_physcannon"':
                    return match.group(0)

            # Check for NPCType lines to avoid npc_grenade_frag
            if b"NPCType" in line and replacement == '"npc_grenade_frag"':
                log_print(f"Retrying randomization for '{original}' because 'npc_grenade_frag' can't be used with NPCType.")
                while replacement == '"npc_grenade_frag"':
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()

            # Check for citizens and antlions
            if original == '"npc_citizen"' and replacement == '"npc_antlion"':
                log_print(f"Retrying randomization for '{original}' in '{os.path.basename(file_path)}' because antlions like to not preacache when replacing citizens.")
                while replacement == '"npc_antlion"':
                    replacement = random.choice(replacements[original]).strip()
                    replacement_bytes = replacement.encode('utf-8').strip()
                
            # Check for "d1_trainstation_01_l_0.lmp", "d3_c17_10a_l_0.lmp" and "d1_trainstation_03_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_trainstation_01_l_0.lmp" or os.path.basename(file_path).lower() == "d3_c17_10a_l_0.lmp" or os.path.basename(file_path).lower() == "d1_trainstation_03_l_0.lmp":
                log_print(f"Skipping randomization for '{os.path.basename(file_path)}' because these maps are way too sensitive for any changes to allow progression.")
                while os.path.basename(file_path).lower() == "d1_trainstation_01_l_0.lmp" or os.path.basename(file_path).lower() == "d3_c17_10a_l_0.lmp" or os.path.basename(file_path).lower() == "d1_trainstation_03_l_0.lmp":
                    return match.group(0)
                
            # Check for "d1_trainstation_04_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_trainstation_04_l_0.lmp" and original in ['"models/props_lab/powerbox02b.mdl"', '"models/props_lab/pipesystem01a.mdl"', '"models/props_lab/pipesystem02a.mdl"', '"models/props_c17/door01_left.mdl"', '"models/props_lab/keypad.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_trainstation_04_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_lab/powerbox02b.mdl"', '"models/props_lab/pipesystem01a.mdl"', '"models/props_lab/pipesystem02a.mdl"', '"models/props_c17/door01_left.mdl"', '"models/props_lab/keypad.mdl"']:
                    return match.group(0)

            # Check for "d1_trainstation_05_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_trainstation_05_l_0.lmp" and original in ['"models/props_interiors/vendingmachinesoda01a_door.mdl"', '"models/props_c17/door01_left.mdl"', '"models/props_lab/keypad.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_trainstation_05_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_interiors/vendingmachinesoda01a_door.mdl"', '"models/props_c17/door01_left.mdl"', '"models/props_lab/keypad.mdl"']:
                    return match.group(0)

            # Check for "d1_trainstation_06_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_trainstation_06_l_0.lmp" and original in ['"models/props_c17/door01_left.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_trainstation_06_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_c17/door01_left.mdl"']:
                    return match.group(0)
                
            # Check for "d1_canals_01_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_01_l_0.lmp" and original in ['"models/props_trainstation/train001.mdl"', '"models/props_trainstation/train002.mdl"', '"models/props_trainstation/train003.mdl"', '"models/props_interiors/furniture_couch02a.mdl"', '"models/props_junk/metalbucket01a.mdl"', '"models/props_c17/furnituredrawer002a.mdl"', '"models/props_c17/tv_monitor01.mdl"', '"models/props_junk/meathook001a.mdl"', '"models/props_wasteland/light_spotlight02_lamp.mdl"', '"models/props_c17/furnituremattress001a.mdl"', '"models/props_junk/garbage_takeoutcarton001a.mdl"', '"models/props_junk/cardboard_box004a.mdl"', '"models/props_junk/metal_paintcan001a.mdl"', '"models/props_c17/chair_office01a.mdl"', '"models/props_junk/garbage_milkcarton002a.mdl"', '"models/props_canal/boxcar_door.mdl"', '"models/props_c17/oildrum001.mdl"', '"models/props_c17/oildrum001_explosive.mdl"', '"models/props_c17/tv_monitor01_screen.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_canals_01_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_trainstation/train001.mdl"', '"models/props_trainstation/train002.mdl"', '"models/props_trainstation/train003.mdl"', '"models/props_interiors/furniture_couch02a.mdl"', '"models/props_junk/metalbucket01a.mdl"', '"models/props_c17/furnituredrawer002a.mdl"', '"models/props_c17/tv_monitor01.mdl"', '"models/props_junk/meathook001a.mdl"', '"models/props_wasteland/light_spotlight02_lamp.mdl"', '"models/props_c17/furnituremattress001a.mdl"', '"models/props_junk/garbage_takeoutcarton001a.mdl"', '"models/props_junk/cardboard_box004a.mdl"', '"models/props_junk/metal_paintcan001a.mdl"', '"models/props_c17/chair_office01a.mdl"', '"models/props_junk/garbage_milkcarton002a.mdl"', '"models/props_canal/boxcar_door.mdl"', '"models/props_c17/oildrum001.mdl"', '"models/props_c17/oildrum001_explosive.mdl"', '"models/props_c17/tv_monitor01_screen.mdl"']:
                    return match.group(0)

            # Remove wood pallets from "d1_canals_01_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_01_l_0.lmp" and original in ['"models/props_junk/wood_pallet001a.mdl"']:
                log_print(f"Replacing '{original}' with blank model to prevent progression issues.")
                return match.group(0).replace(original.encode('utf-8'), b'"models/error.mdl"')
                
            # Check for "d1_canals_01a_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_01a_l_0.lmp" and original in ['"models/props_c17/oildrum001_explosive.mdl"', '"models/props_canal/canal_bars002.mdl"', '"models/props_canal/canal_bars002b.mdl"', '"models/props_junk/cinderblock01a.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_canals_01a_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_c17/oildrum001_explosive.mdl"', '"models/props_canal/canal_bars002.mdl"', '"models/props_canal/canal_bars002b.mdl"', '"models/props_junk/cinderblock01a.mdl"']:
                    return match.group(0)

            # Check for "d1_canals_02_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_02_l_0.lmp" and original in ['"models/props_junk/cinderblock01a.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_canals_02_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_junk/cinderblock01a.mdl"']:
                    return match.group(0)
                
            # Check for "d1_canals_06_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_06_l_0.lmp" and original in ['"models/props_borealis/bluebarrel002.mdl"', '"models/props_canal/canal_bars003.mdl"', '"models/props_c17/oildrum001.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_canals_06_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_borealis/bluebarrel002.mdl"', '"models/props_canal/canal_bars003.mdl"', '"models/props_c17/oildrum001.mdl"']:
                    return match.group(0)
                
            # Check for "d1_canals_11_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_11_l_0.lmp" and original in ['"models/props_c17/furniturewashingmachine001a.mdl"', '"models/props_junk/cinderblock01a.mdl"', '"models/props_c17/furniturechair001a.mdl"', '"models/props_c17/oildrum001.mdl"', '"models/props_vehicles/carparts_tire01a.mdl"', '"models/props_wasteland/tram_lever01.mdl"', '"models/props_wasteland/tram_leverbase01.mdl"', '"models/props_c17/metalladder002.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_canals_11_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_c17/furniturewashingmachine001a.mdl"', '"models/props_junk/cinderblock01a.mdl"', '"models/props_c17/furniturechair001a.mdl"', '"models/props_c17/oildrum001.mdl"', '"models/props_vehicles/carparts_tire01a.mdl"', '"models/props_wasteland/tram_lever01.mdl"', '"models/props_wasteland/tram_leverbase01.mdl"', '"models/props_c17/metalladder002.mdl"']:
                    return match.group(0)
                
            # Check for "d1_canals_12_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_canals_12_l_0.lmp" and original in ['"models/props_c17/oildrum001_explosive.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_canals_12_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_c17/oildrum001_explosive.mdl"']:
                    return match.group(0)

            # Check for "d1_eli_01_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_eli_01_l_0.lmp" and original in ['"models/props_lab/blastdoor001a.mdl"', '"models/props_lab/blastdoor001b.mdl"', '"models/props_lab/blastdoor001c.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_eli_01_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_lab/blastdoor001a.mdl"', '"models/props_lab/blastdoor001b.mdl"', '"models/props_lab/blastdoor001c.mdl"']:
                    return match.group(0)

            # Check for "d1_eli_02_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_eli_02_l_0.lmp" and original in ['"models/props_lab/dogobject_wood_crate001a_damagedmax.mdl"', '"models/props_c17/oildrum001.mdl"', '"models/props_lab/blastdoor001a.mdl"', '"models/props_lab/blastdoor001b.mdl"', '"models/props_lab/blastdoor001c.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_eli_02_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_lab/dogobject_wood_crate001a_damagedmax.mdl"', '"models/props_c17/oildrum001.mdl"', '"models/props_lab/blastdoor001a.mdl"', '"models/props_lab/blastdoor001b.mdl"', '"models/props_lab/blastdoor001c.mdl"']:
                    return match.group(0)
                
            # Check for "d1_town_01_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_town_01_l_0.lmp" and original in ['"models/props_vehicles/car004a_physics.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_town_01_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_vehicles/car004a_physics.mdl"']:
                    return match.group(0)
                
            # Check for "d1_town_02_l_0.lmp"
            if os.path.basename(file_path).lower() == "d1_town_02_l_0.lmp" and original in ['"models/props_wasteland/tram_lever01.mdl"', '"models/props_c17/pulleywheels_small01.mdl"', '"models/props_c17/pulleywheels_large01.mdl"', '"models/props_wasteland/tram_bracket01.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd1_town_02_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_wasteland/tram_lever01.mdl"', '"models/props_c17/pulleywheels_small01.mdl"', '"models/props_c17/pulleywheels_large01.mdl"', '"models/props_wasteland/tram_bracket01.mdl"']:
                    return match.group(0)

            # Check for "d2_coast_03_l_0.lmp"
            if os.path.basename(file_path).lower() == "d2_coast_03_l_0.lmp" and original in ['"models/props_wasteland/barricade002a.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd2_coast_03_l_0.lmp' to prevent crashing issue.")
                while original in ['"models/props_wasteland/barricade002a.mdl"']:
                    return match.group(0)

            # Check for "d2_coast_11_l_0.lmp"
            if os.path.basename(file_path).lower() == "d2_coast_11_l_0.lmp" and original in ['"models/props_borealis/borealis_door001a.mdl"', '"models/props_wasteland/exterior_fence003b.mdl"', '"models/props_foliage/driftwood_01a.mdl"', '"models/props_debris/rebar_cluster001b.mdl"', '"models/props_junk/wood_pallet001a.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd2_coast_11_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_borealis/borealis_door001a.mdl"', '"models/props_wasteland/exterior_fence003b.mdl"', '"models/props_foliage/driftwood_01a.mdl"', '"models/props_debris/rebar_cluster001b.mdl"', '"models/props_junk/wood_pallet001a.mdl"']:
                    return match.group(0)

            # Check for "d2_prison_05_l_0.lmp"
            if os.path.basename(file_path).lower() == "d2_prison_05_l_0.lmp" and original in ['"models/props_c17/oildrum001.mdl"', '"models/props_junk/wood_crate001a_damaged.mdl"', '"models/props_junk/cardboard_box002a.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd2_prison_05_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_c17/oildrum001.mdl"', '"models/props_junk/wood_crate001a_damaged.mdl"', '"models/props_junk/cardboard_box002a.mdl"']:
                    return match.group(0)
                
            # Check for "d2_prison_07_l_0.lmp"
            if os.path.basename(file_path).lower() == "d2_prison_07_l_0.lmp" and original in ['"models/props_borealis/bluebarrel001.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd2_prison_07_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_borealis/bluebarrel001.mdl"']:
                    return match.group(0)
                
            # Check for "d3_c17_08_l_0.lmp"
            if os.path.basename(file_path).lower() == "d3_c17_08_l_0.lmp" and original in ['"models/props_c17/oildrum001.mdl"', '"models/props_c17/oildrum001_explosive.mdl"', '"models/props_c17/handrail04_long.mdl"', '"models/props_c17/handrail04_brokenlong.mdl"', '"models/props_c17/utilityconnecter005.mdl"']:
                log_print(f"Skipping randomization for '{original}' in 'd3_c17_08_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_c17/oildrum001.mdl"', '"models/props_c17/oildrum001_explosive.mdl"', '"models/props_c17/handrail04_long.mdl"', '"models/props_c17/handrail04_brokenlong.mdl"', '"models/props_c17/utilityconnecter005.mdl"']:
                    return match.group(0)

            # Check for "d3_breen_01_l_0.lmp"
            if os.path.basename(file_path).lower() == "d3_breen_01_l_0.lmp" and prompt == "props":
                log_print(f"Skipping prop randomization in 'd3_breen_01_l_0.lmp' because it causes progression issues.")
                return match.group(0)
                
            # Check for "d3_c17_06a_l_0.lmp"
            concrete_models = read_concrete_models()
            if os.path.basename(file_path).lower() == "d3_c17_06a_l_0.lmp" and original in concrete_models:
                log_print(f"Skipping randomization for '{original}' in 'd3_c17_06a_l_0.lmp' because randomizing these props cause potential progression issues.")
                while original in concrete_models:
                    return match.group(0)
                    
            # Replace boards and vents with blank model
            if original in ['"models/props_debris/wood_board01a.mdl"', '"models/props_debris/wood_board02a.mdl"', '"models/proprs_debris/wood_board03a.mdl"', '"models/props_debris/wood_board04a.mdl"', '"models/props_debris/wood_board05a.mdl"', '"models/props_debris/wood_board06a.mdl"', '"models/props_debris/wood_board07a.mdl"', '"models/props_junk/vent001.mdl"']:
                if os.path.basename(file_path).lower() == "d1_canals_03_l_0.lmp":
                    log_print(f"Skipping randomization for '{original}' in d1_canals_03_l_0.lmp because randomizing these props cause potential progression issues.")
                    return match.group(0)
                else:
                    log_print(f"Replacing '{original}' with blank model in {file_path} to prevent progression issues")
                    return match.group(0).replace(original.encode('utf-8'), b'"models/error.mdl"')

            # Check for cranes and locks
            if original in ['"models/props_wasteland/cranemagnet01a.mdl"', '"models/props_wasteland/prison_padlock001a.mdl"']:
                log_print(f"Skipping randomization for '{original}' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_wasteland/cranemagnet01a.mdl"', '"models/props_wasteland/prison_padlock001a.mdl"']:
                    return match.group(0)
                
            # Check for elevator stuff
            if original in ['"models/props_lab/elevatordoor.mdl"', '"models/props_lab/freightelevator.mdl"', '"models/props_lab/freightelevatorbutton.mdl"']:
                log_print(f"Skipping randomization for '{original}' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_lab/elevatordoor.mdl"', '"models/props_lab/freightelevator.mdl"', '"models/props_lab/freightelevatorbutton.mdl"']:
                    return match.group(0)

            # Check for teleporter stuff
            if original in ['"models/props_lab/teleportgate.mdl"', '"models/props_lab/teleplatform.mdl"', '"models/props_lab/teleportring.mdl"', '"models/props_lab/teleportbulk.mdl"', '"models/props_lab/lab_flourescentlight001b.mdl"']:
                log_print(f"Skipping randomization for '{original}' because randomizing these props cause potential progression issues.")
                while original in ['"models/props_lab/teleportgate.mdl"', '"models/props_lab/teleplatform.mdl"', '"models/props_lab/teleportring.mdl"', '"models/props_lab/lab_flourescentlight001b.mdl"']:
                    return match.group(0)
                
            log_print(f"Replacing '{original}' with '{replacement}' at position {start}-{end} in {file_path}")
            return replacement_bytes

        content = combined_pattern.sub(replacer, content)

    # Remove all hexadecimal bytes of 0D past byte 20
    content = content[:20] + content[20:].replace(b'\x0D', b'')

    if npc_model_dict:
        for npc, models in npc_model_dict.items():
            log_print(f"Processing NPC: {npc}")
            # Skip model replacement for npc_citizen in maps listed in npc_citizen.txt
            if npc == '"npc_citizen"':
                map_name = os.path.basename(file_path)
                citizen_maps = read_lines("npc_citizen.txt")
                if map_name in citizen_maps:
                    log_print(f"Skipping model replacement for '{npc}' in map '{map_name}' as it's listed in npc_citizen.txt")
                    continue
            npc_bytes = npc.encode('utf-8').strip()
            npc_pattern = re.compile(re.escape(npc_bytes), re.IGNORECASE)
            for match in npc_pattern.finditer(content):
                start = match.start()
                end = match.end()
                log_print(f"Match found for '{npc}' at position {start}-{end}")
                brace_pos = content.rfind(b'{', 0, start)
                closing_brace_pos = content.find(b'}', end)
                log_print(f"Brace positions: {brace_pos}, {closing_brace_pos}")
                if brace_pos != -1 and closing_brace_pos != -1:
                    line_start = content.rfind(b'\n', 0, brace_pos) + 1
                    line_end = content.find(b'\n', closing_brace_pos)
                    line = content[line_start:line_end]
                    log_print(f"Line content: {line}")

                    if b"excludednpc" in line:
                        log_print(f"Skipping model replacement for '{npc}' at position {start}-{end} in {file_path} due to 'excludednpc' tag in line.")
                        continue
                    if b"filterclass" in line:
                        log_print(f"Skipping model replacement for '{npc}' at position {start}-{end} in {file_path} due to 'filterclass' tag in line.")
                        continue

                    model_pos = content.find(b'"model"', brace_pos, closing_brace_pos)
                    log_print(f"Model position: {model_pos}")
                    if model_pos != -1:
                        model_line_end = content.find(b'\n', model_pos)
                        original_model_line = content[model_pos:model_line_end].decode('utf-8').strip()
                        log_print(f"Original model line: {original_model_line}")
                        if '*' in original_model_line:
                            log_print(f"Aborting model replacement for '{npc}' at position {start}-{end} due to '*' in original model line '{original_model_line}'")
                            continue
                        replacement_model = random.choice(models).strip()
                        replacement_model_line = f'"model" "{replacement_model}"'
                        log_print(f"Replacing model for '{npc}' at {start}-{end} with '{replacement_model}' at position {model_pos}-{model_line_end} in {file_path}")
                        content = content[:model_pos] + replacement_model_line.encode('utf-8') + content[model_line_end:]
                    else:
                        log_print(f"No model found for '{npc}' at position {start}-{end} in {file_path}")

    with open(file_path, 'wb') as file:
        file.write(content)

def calculate_length_and_update(file_path):
    with open(file_path, 'r+b') as file:
        file.seek(0x14)
        length = len(file.read())
        file.seek(0x0C)
        file.write(struct.pack('<I', length))

def read_props_and_big_maps():
    # Read props and identify which ones are "big"
    big_props = set()
    regular_props = set()
    with open("props.txt", 'r') as file:
        for line in file:
            prop = line.strip()
            if prop.endswith('*'):
                big_props.add(f'"{prop[:-1]}"')  # Remove * and add quotes
            else:
                regular_props.add(f'"{prop}"')
    
    # Read big maps
    big_maps = set(read_lines("big_maps.txt"))
    
    return regular_props, big_props, big_maps

def get_replacements(file_name, file_path=None):
    if file_name == "props.txt":
        regular_props, big_props, big_maps = read_props_and_big_maps()
        map_name = os.path.basename(file_path) if file_path else ""
        
        replacements = {}
        all_props = regular_props | big_props
        message_log_printed = False
        
        for prop in all_props:
            if map_name in big_maps:
                # In big maps, only use regular props
                replacements[prop.lower()] = list(regular_props)
                if file_path and not message_log_printed:
                    log_print(f"Using only regular props in {map_name}")
                    message_log_printed = True
            else:
                # In regular maps, can use all props
                replacements[prop.lower()] = list(all_props)
                if file_path and not message_log_printed:
                    log_print(f"Using all props in {map_name}")
                    message_log_printed = True
        return replacements

    lines = read_lines(file_name)
    replacements = {}
    for line in lines:
        line = line.strip()
        quoted_line = f'"{line}"'  # Ensure the line is quoted
        if quoted_line.lower() not in replacements:
            replacements[quoted_line.lower()] = [f'"{item}"' for item in lines]  # Ensure all items are quoted
    return replacements

def get_dynamic_resupply_replacements(allow_traps=False):
    items = [f'"{line.strip()}"' for line in read_lines("items.txt")]
    weapons = [f'"{line.strip()}"' for line in read_lines("weapons.txt")]
    replacements = items + weapons
    
    if allow_traps:
        npcs = [f'"{line.strip()}"' for line in read_lines("npcs.txt")]
        replacements.extend(npcs)
    
    return replacements

def get_safe_replacement(replacements, file_path):
    while True:
        replacement = random.choice(replacements)
        if replacement == '"npc_barnacle"' or replacement == '"npc_turret_floor"':
            log_print(f"Got {replacement} in {file_path}, retrying randomization to prevent crash...")
            continue
        return replacement

def randomize_dynamic_resupply(file_path, item_min, item_max, allow_traps=False):
    with open(file_path, 'rb') as file:
        content = file.read()
    
    replacements = get_dynamic_resupply_replacements(allow_traps)
    combined_pattern = re.compile(b'"ItemCount"\s+"[^"]*"[^\n]*\n[^\n]*"item_dynamic_resupply"', re.IGNORECASE)
    
    def replace_both(match):
        original = match.group(0).decode('utf-8')
        new_count = random.randint(item_min, item_max)
        replacement = get_safe_replacement(replacements, file_path)
        
        count_line, resupply_line = original.split('\n')
        new_count_line = f'"ItemCount" "{new_count}"'
        new_resupply_line = resupply_line.replace('"item_dynamic_resupply"', replacement)
        
        log_print(f"Replacing item_dynamic_resupply with {replacement} with a count of {new_count} in {file_path}")
        return f"{new_count_line}\n{new_resupply_line}".encode('utf-8')
    
    content = combined_pattern.sub(replace_both, content)
    
    with open(file_path, 'wb') as file:
        file.write(content)

def randomize_sounds(file_path, sounds_dict, music_list=None):
    with open(file_path, 'rb') as file:
        content = file.read()

    # Pattern for sound fields
    field_names = b'|'.join([
        b'message', b'shootsound', b'noise1', b'noise2',
        b'soundopenoverride', b'StopSound', b'StartSound', b'MoveSound', b'soundclose', b'soundlocked', b'soundmove', b'soundunlocked',
        b'SoundClose', b'SoundLocked', b'SoundMove', b'SoundUnlocked'  # Add uppercase variants
    ])
    sound_pattern = re.compile(b'"(' + field_names + b')"\s+"([^"]*)"', re.IGNORECASE)
    
    def sound_replacer(match):
        field = match.group(1).decode('utf-8')
        original = match.group(2).decode('utf-8')
        
        # Skip if this is a music file and we're in sounds-only mode
        if music_list and original in music_list:
            log_print(f"Skipping music '{original}' in {file_path} as it's in sounds-only mode")
            return match.group(0)
            
        replacement = random.choice(sounds_dict['sounds'])
        log_print(f"Replacing {field} sound '{original}' with '{replacement}' in {file_path}")
        return f'"{field}" "{replacement}"'.encode('utf-8')

    content = sound_pattern.sub(sound_replacer, content)

    # Pattern for soundscapes
    soundscape_pattern = re.compile(b'"soundscape"\s+"([^"]*)"', re.IGNORECASE)
    
    def soundscape_replacer(match):
        original = match.group(1).decode('utf-8')
        replacement = random.choice(sounds_dict['soundscapes'])
        log_print(f"Replacing soundscape '{original}' with '{replacement}' in {file_path}")
        return f'"soundscape" "{replacement}"'.encode('utf-8')

    content = soundscape_pattern.sub(soundscape_replacer, content)

    with open(file_path, 'wb') as file:
        file.write(content)

def randomize_music(file_path, music_list):
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Create quoted music list
    quoted_music = [f'"{music}"' for music in music_list]
    
    # Create a single pattern from all music entries
    music_pattern = re.compile(b'|'.join(re.escape(music.encode('utf-8')) for music in quoted_music), re.IGNORECASE)
    
    def music_replacer(match):
        original = match.group(0).decode('utf-8')
        replacement = f'"{random.choice(music_list)}"'
        log_print(f"Replacing music '{original}' with '{replacement}' in {file_path}")
        return replacement.encode('utf-8')
        
    content = music_pattern.sub(music_replacer, content)
    
    with open(file_path, 'wb') as file:
        file.write(content)

def randomize_lights(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Pattern for "_light" fields
    light_pattern = re.compile(b'"_light"\s+"([0-9]+\s+[0-9]+\s+[0-9]+)\s+([0-9]+)"', re.IGNORECASE)
    
    def light_replacer(match):
        # Generate random RGB values (0-255) and intensity (0-1000)
        new_rgb = f"{random.randint(0, 255)} {random.randint(0, 255)} {random.randint(0, 255)}"
        new_intensity = str(random.randint(0, 1000))
        log_print(f"Replacing light '{match.group(1).decode('utf-8')} {match.group(2).decode('utf-8')}' with '{new_rgb} {new_intensity}' in {file_path}")
        return f'"_light" "{new_rgb} {new_intensity}"'.encode('utf-8')

    content = light_pattern.sub(light_replacer, content)

    # Pattern for "color" fields
    color_pattern = re.compile(b'"color"\s+"([0-9]+\s+[0-9]+\s+[0-9]+)"', re.IGNORECASE)
    
    def color_replacer(match):
        # Generate random RGB values (0-255)
        new_rgb = f"{random.randint(0, 255)} {random.randint(0, 255)} {random.randint(0, 255)}"
        log_print(f"Replacing color '{match.group(1).decode('utf-8')}' with '{new_rgb}' in {file_path}")
        return f'"color" "{new_rgb}"'.encode('utf-8')

    content = color_pattern.sub(color_replacer, content)

    # Pattern for "rendercolor" fields
    rendercolor_pattern = re.compile(b'"rendercolor"\s+"([0-9]+\s+[0-9]+\s+[0-9]+)"', re.IGNORECASE)

    def rendercolor_replacer(match):
        # Generate random RGB values (0-255)
        new_rgb = f"{random.randint(0, 255)} {random.randint(0, 255)} {random.randint(0, 255)}"
        log_print(f"Replacing rendercolor '{match.group(1).decode('utf-8')}' with '{new_rgb}' in {file_path}")
        return f'"rendercolor" "{new_rgb}"'.encode('utf-8')
    
    content = rendercolor_pattern.sub(rendercolor_replacer, content)

    with open(file_path, 'wb') as file:
        file.write(content)

def randomize_ammo_crates(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    
    # Pattern for ammo type fields (matches full line containing AmmoType and a number 0-9)
    ammo_pattern = re.compile(b'"AmmoType"\s+"[0-9]"', re.IGNORECASE)
    
    def ammo_replacer(match):
        original = match.group(0).decode('utf-8')
        new_type = str(random.randint(0, 9))
        new_line = f'"AmmoType" "{new_type}"'
        log_print(f"Replacing ammo type '{original}' with '{new_line}' in {file_path}")
        return new_line.encode('utf-8')

    content = ammo_pattern.sub(ammo_replacer, content)
    
    with open(file_path, 'wb') as file:
        file.write(content)

def remove_coast_11_blockers(file_path):
    if os.path.basename(file_path).lower() != "d2_coast_11_l_0.lmp":
        return

    with open(file_path, 'rb') as file:
        content = file.read()

    # These are the props/entities to remove from d2_coast_11_l_0.lmp
    entity_names = [
        b'"gate_mover_blocker"', 
        b'"gate_mover"', 
        b'"camp_door_blocker"', 
        b'"camp_door"', 
        b'"antlion_cage_door"',
        b'"models/props_borealis/borealis_door001a.mdl"',
        b'"models/props_wasteland/exterior_fence003b.mdl"',
        b'"models/props_foliage/driftwood_01a.mdl"',
        b'"models/props_debris/rebar_cluster001b.mdl"',
        b'"models/props_junk/wood_pallet001a.mdl"'
    ]

    for entity_name in entity_names:
        while True:
            pattern = re.compile(re.escape(entity_name))
            match = pattern.search(content)
            if not match:
                break

            pos = match.start()
            start_brace = content.rfind(b'{', 0, pos)
            if start_brace != -1:
                end_brace = content.find(b'}', pos)
                if end_brace != -1:
                    prev_char = start_brace - 1
                    while prev_char >= 0 and content[prev_char:prev_char+1] in [b'\n', b'\r', b' ', b'\t']:
                        prev_char -= 1
                    next_char = end_brace + 1
                    while next_char < len(content) and content[next_char:next_char+1] in [b'\n', b'\r', b' ', b'\t']:
                        next_char += 1

                    # Remove the entire entity block
                    content = content[:prev_char+1] + b'\n' + content[next_char:]
                    log_print(f"Removed entity or prop block {entity_name.decode('utf-8')} from {file_path}")

    with open(file_path, 'wb') as file:
        file.write(content)

def remove_boards_and_vents(file_path):
    if os.path.basename(file_path).lower() == "d1_canals_03_l_0.lmp":
        return

    with open(file_path, 'rb') as file:
        content = file.read()

    # These are the props/entities to remove
    entity_names = [
        b'"models/props_debris/wood_board01a.mdl"', 
        b'"models/props_debris/wood_board02a.mdl"', 
        b'"models/props_debris/wood_board03a.mdl"', 
        b'"models/props_debris/wood_board04a.mdl"', 
        b'"models/props_debris/wood_board05a.mdl"',
        b'"models/props_debris/wood_board06a.mdl"',
        b'"models/props_debris/wood_board07a.mdl"',
        b'"models/props_junk/vent001.mdl"',
    ]

    for entity_name in entity_names:
        while True:
            pattern = re.compile(re.escape(entity_name))
            match = pattern.search(content)
            if not match:
                break

            pos = match.start()
            start_brace = content.rfind(b'{', 0, pos)
            if start_brace != -1:
                end_brace = content.find(b'}', pos)
                if end_brace != -1:
                    prev_char = start_brace - 1
                    while prev_char >= 0 and content[prev_char:prev_char+1] in [b'\n', b'\r', b' ', b'\t']:
                        prev_char -= 1
                    next_char = end_brace + 1
                    while next_char < len(content) and content[next_char:next_char+1] in [b'\n', b'\r', b' ', b'\t']:
                        next_char += 1

                    # Remove the entire entity block
                    content = content[:prev_char+1] + b'\n' + content[next_char:]
                    log_print(f"Removed entity or prop block {entity_name.decode('utf-8')} from {file_path}")

    with open(file_path, 'wb') as file:
        file.write(content)

def main():
    print("Checking 'backup' directory...")
    if not os.path.exists("backup"):
        os.makedirs("backup")
        print("Created 'backup' directory.")

    for root, _, files in os.walk('.'):
        if "backup" in root:
            continue

        for file in files:
            if file.endswith('.lmp'):
                backup_path = os.path.join("backup", file)
                original_path = os.path.join(root, file)

                if os.path.exists(backup_path):
                    shutil.copy2(backup_path, original_path)
                    print(f"Restored '{original_path}' from '{backup_path}'.")
                else:
                    shutil.copy2(original_path, backup_path)
                    print(f"Copied '{original_path}' to '{backup_path}' for backup.")
    
    global GLOBAL_SEED
    global LOG_FILE

    seed_input = input("Enter a seed (optional): ").strip()
    if seed_input == "":
        GLOBAL_SEED = random.randint(0, 2**31 - 1)
    else:
        GLOBAL_SEED = int(seed_input)

    random.seed(GLOBAL_SEED)
    date_str = datetime.datetime.now().strftime("%m/%d/%Y at %I:%M%p")
    LOG_FILE = open(f"{GLOBAL_SEED}.txt", "a")
    LOG_FILE.write(f"Randomization started on {date_str} with seed {GLOBAL_SEED}\n")

    log_print(f"Using seed {GLOBAL_SEED}")

    prompts = [
        ("npcs", "npcs.txt"),
        ("items", "items.txt"),
        ("weapons", "weapons.txt"),
        ("props", "props.txt"),
        ("skyboxes", "skyboxes.txt"),
        ("decals", "decals.txt"),
        ("chargers", "chargers.txt"),
    ]

    important_npcs = read_important_npcs("important_npcs.txt")
    npc_map_dict = read_npc_map_files()

    npc_model_dict = {
        '"npc_alyx"': ["models/alyx.mdl"],
        '"npc_antlion"': ["models/antlion.mdl"],
        '"npc_antlionguard"': ["models/antlion_guard.mdl"],
        '"npc_barnacle"': ["models/barnacle.mdl"],
        '"npc_barney"': ["models/barney.mdl"],
        '"npc_breen"': ["models/breen.mdl"],
        '"npc_citizen"': [
            "models/humans/group01/female_01.mdl", "models/humans/group01/female_02.mdl",
            "models/humans/group01/female_03.mdl", "models/humans/group01/female_04.mdl",
            "models/humans/group01/female_06.mdl", "models/humans/group01/female_07.mdl",
            "models/humans/group01/male_01.mdl", "models/humans/group01/male_02.mdl",
            "models/humans/group01/male_03.mdl", "models/humans/group01/male_04.mdl",
            "models/humans/group01/male_05.mdl", "models/humans/group01/male_06.mdl",
            "models/humans/group01/male_07.mdl", "models/humans/group01/male_08.mdl",
            "models/humans/group01/male_09.mdl", "models/humans/group01/male_cheaple.mdl",
            "models/humans/group02/female_01.mdl", "models/humans/group02/female_02.mdl",
            "models/humans/group02/female_03.mdl", "models/humans/group02/female_04.mdl",
            "models/humans/group02/female_06.mdl", "models/humans/group02/female_07.mdl",
            "models/humans/group02/male_01.mdl", "models/humans/group02/male_02.mdl",
            "models/humans/group02/male_03.mdl", "models/humans/group02/male_04.mdl",
            "models/humans/group02/male_05.mdl", "models/humans/group02/male_06.mdl",
            "models/humans/group02/male_07.mdl", "models/humans/group02/male_08.mdl",
            "models/humans/group02/male_09.mdl", "models/humans/group03/female_01.mdl",
            "models/humans/group03/female_01_bloody.mdl", "models/humans/group03/female_02.mdl",
            "models/humans/group03/female_02_bloody.mdl", "models/humans/group03/female_03.mdl",
            "models/humans/group03/female_03_bloody.mdl", "models/humans/group03/female_04.mdl",
            "models/humans/group03/female_04_bloody.mdl", "models/humans/group03/female_06.mdl",
            "models/humans/group03/female_06_bloody.mdl", "models/humans/group03/female_07.mdl",
            "models/humans/group03/female_07_bloody.mdl", "models/humans/group03/male_01.mdl",
            "models/humans/group03/male_01_bloody.mdl", "models/humans/group03/male_02.mdl",
            "models/humans/group03/male_02_bloody.mdl", "models/humans/group03/male_03.mdl",
            "models/humans/group03/male_03_bloody.mdl", "models/humans/group03/male_04.mdl",
            "models/humans/group03/male_04_bloody.mdl", "models/humans/group03/male_05.mdl",
            "models/humans/group03/male_05_bloody.mdl", "models/humans/group03/male_06.mdl",
            "models/humans/group03/male_06_bloody.mdl", "models/humans/group03/male_07.mdl",
            "models/humans/group03/male_07_bloody.mdl", "models/humans/group03/male_08.mdl",
            "models/humans/group03/male_08_bloody.mdl", "models/humans/group03/male_09.mdl",
            "models/humans/group03/male_09_bloody.mdl", "models/humans/group03m/female_01.mdl",
            "models/humans/group03m/female_02.mdl", "models/humans/group03m/female_03.mdl",
            "models/humans/group03m/female_04.mdl", "models/humans/group03m/female_06.mdl",
            "models/humans/group03m/female_07.mdl", "models/humans/group03m/male_01.mdl",
            "models/humans/group03m/male_02.mdl", "models/humans/group03m/male_03.mdl",
            "models/humans/group03m/male_04.mdl", "models/humans/group03m/male_05.mdl",
            "models/humans/group03m/male_06.mdl", "models/humans/group03m/male_07.mdl",
            "models/humans/group03m/male_08.mdl", "models/humans/group03m/male_09.mdl"
        ],
        '"npc_combine_camera"': ["models/combine_camera/combine_camera.mdl"],
        '"npc_combine_s"': ["models/combine_soldier.mdl", "models/combine_soldier_prisonguard.mdl", "models/combine_super_soldier.mdl"],
        '"npc_combinedropship"': ["models/combine_dropship.mdl"],
        '"npc_combinegunship"': ["models/gunship.mdl"],
        '"npc_crow"': ["models/crow.mdl"],
        '"npc_cscanner"': ["models/shield_scanner.mdl", "models/combine_scanner.mdl"],
        '"npc_dog"': ["models/dog.mdl"],
        '"npc_eli"': ["models/eli.mdl"],
        '"npc_fastzombie"': ["models/zombie/fast.mdl"],
        '"npc_fastzombie_torso"': ["models/gibs/fast_zombie_torso.mdl"],
        '"npc_gman"': ["models/gman.mdl"],
        '"npc_grenade_frag"': ["models/items/grenadeammo.mdl"],
        '"npc_headcrab_black"': ["models/headcrabblack.mdl"],
        '"npc_headcrab_fast"': ["models/headcrab.mdl"],
        '"npc_headcrab"': ["models/headcrabclassic.mdl"],
        '"npc_helicopter"': ["models/combine_helicopter.mdl"],
        '"npc_ichthyosaur"': ["models/ichthyosaur.mdl"],
        '"npc_kleiner"': ["models/kleiner.mdl"],
        '"npc_manhack"': ["models/manhack.mdl"],
        '"npc_metropolice"': ["models/police_cheaple.mdl", "models/police.mdl"],
        '"npc_monk"': ["models/monk.mdl"],
        '"npc_mossman"': ["models/mossman.mdl"],
        '"npc_pigeon"': ["models/pigeon.mdl"],
        '"npc_poisonzombie"': ["models/zombie/poison.mdl"],
        '"npc_rollermine"': ["models/roller.mdl"],
        '"npc_seagull"': ["models/seagull.mdl"],
        '"npc_sniper"': ["models/combine_soldier.mdl"],
        '"npc_stalker"': ["models/stalker.mdl"],
        '"npc_strider"': ["models/combine_strider.mdl"],
        '"npc_turret_ceiling"': ["models/combine_turrets/ceiling_turret.mdl"],
        '"npc_turret_floor"': ["models/combine_turrets/floor_turret.mdl"],
        '"npc_turret_ground"': ["models/combine_turrets/ground_turret.mdl"],
        '"npc_vortigaunt"': ["models/vortigaunt.mdl"],
        '"npc_zombie"': ["models/zombie/classic.mdl"],
        '"npc_zombie_torso"': ["models/zombie/classic_torso.mdl"]
    }

    for prompt, txt_file in prompts:
        while True:
            response = input(f"Do you want to randomize {prompt}? (y/n): ").strip().lower()
            if response in ['y', 'n']:
                break
            log_print("Please enter 'y' or 'n'")
            
        if response == 'y':
            # Get replacements without file path initially 
            replacements = get_replacements(txt_file)
            check_next_line = (prompt == "weapons")
            is_weapon = (prompt == "weapons")

            # Walk through files and apply replacements
            for root, _, files in os.walk('.'):
                if "backup" in root:
                    continue
                for file in files:
                    if file.endswith('.lmp'):
                        if prompt == "props":
                            replacements = get_replacements(txt_file, os.path.join(root, file))
                
                        randomize_file(os.path.join(root, file), replacements, check_next_line,
                                    important_npcs if prompt == "npcs" else None,
                                    npc_map_dict if prompt == "npcs" else None, 
                                    npc_model_dict if prompt == "models" else None,
                                    is_weapon,
                                    prompt)
                        calculate_length_and_update(os.path.join(root, file))
                        
                        if prompt == "weapons":
                            remove_coast_11_blockers(os.path.join(root, file))
                            remove_boards_and_vents(os.path.join(root, file))
                            calculate_length_and_update(os.path.join(root, file))

    while True:
        response = input("Do you want to randomize dynamic resupplies? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            break
        log_print("Please enter 'y' or 'n'")

    if response == 'y':
        while True:
            allow_traps = input("Do you want to allow random NPC traps? (y/n): ").strip().lower()
            if allow_traps in ['y', 'n']:
                break
            log_print("Please enter 'y' or 'n'")
    
        allow_traps = allow_traps == 'y'
    
        while True:
            item_range = input("Enter item count range (min-max, e.g. 1-5): ").strip()
            try:
                item_min, item_max = map(int, item_range.split('-'))
                break
            except ValueError:
                log_print("Invalid range format. Please try again.")
    
        for root, _, files in os.walk('.'):
            if "backup" in root:
                continue
            for file in files:
                if file.endswith('.lmp'):
                    randomize_dynamic_resupply(os.path.join(root, file), item_min, item_max, allow_traps)
                    calculate_length_and_update(os.path.join(root, file))

    while True:
        response = input("Do you want to randomize sounds and/or music? (sounds/music/both/none): ").strip().lower()
        if response in ['sounds', 'music', 'both', 'none']:
            break
        log_print("Please enter 'sounds', 'music', 'both', or 'none'")

    if response != 'none':
        if response == 'sounds':
            # Load sounds and music lists for filtering
            sounds_list = [line.strip() for line in read_lines("sounds.txt")]
            music_list = [line.strip() for line in read_lines("music.txt")]
            sounds_dict = {
                'sounds': sounds_list,
                'soundscapes': [line.strip() for line in read_lines("soundscapes.txt")]
            }
        elif response == 'music':
            # Only load music list
            music_list = [line.strip() for line in read_lines("music.txt")]
        else:  # both
            # Load combined sounds and music list
            combined_list = [line.strip() for line in read_lines("sounds&music.txt")]
            sounds_dict = {
                'sounds': combined_list,
                'soundscapes': [line.strip() for line in read_lines("soundscapes.txt")]
            }

        for root, _, files in os.walk('.'):
            if "backup" in root:
                continue
            for file in files:
                if file.endswith('.lmp'):
                    if response == 'music':
                        randomize_music(os.path.join(root, file), music_list)
                    else:
                        randomize_sounds(os.path.join(root, file), sounds_dict, 
                                   music_list if response == 'sounds' else None)
                    calculate_length_and_update(os.path.join(root, file))

    while True:
        response = input("Do you want to randomize lights and colors? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            break
        log_print("Please enter 'y' or 'n'")

    if response == 'y':
        for root, _, files in os.walk('.'):
            if "backup" in root:
                continue
            for file in files:
                if file.endswith('.lmp'):
                    randomize_lights(os.path.join(root, file))
                    calculate_length_and_update(os.path.join(root, file))

    while True:
        response = input("Do you want to randomize ammo crates? (y/n): ").strip().lower()
        if response in ['y', 'n']:
            break
        log_print("Please enter 'y' or 'n'")

    if response == 'y':
        for root, _, files in os.walk('.'):
            if "backup" in root:
                continue
            for file in files:
                if file.endswith('.lmp'):
                    randomize_ammo_crates(os.path.join(root, file))
                    calculate_length_and_update(os.path.join(root, file))

    while True:
        response = input("Do you want to fix models? (This is only needed if you randomized NPCs.) (y/n): ").strip().lower()
        if response in ['y', 'n']:
            break
        log_print("Please enter 'y' or 'n'")

    if response == 'y':
        for root, _, files in os.walk('.'):
            if "backup" in root:
                continue
            for file in files:
                if file.endswith('.lmp'):
                    randomize_file(os.path.join(root, file), {}, False, None, None, npc_model_dict)
                    calculate_length_and_update(os.path.join(root, file))
    elif response == 'n':
        log_print("Your funeral. (If you did randomize NPCs.)")

    if LOG_FILE:
        LOG_FILE.close()

if __name__ == "__main__":
    main()