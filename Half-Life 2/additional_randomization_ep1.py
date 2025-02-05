from pathlib import Path
import shutil
import random
import re

from pathlib import Path

def extract_vpk_stuff():
    """Extracts data from EP1 VPK to new files"""
    
    vpk_path = Path("./episodic/ep1_pak_001.vpk")
    output_dir = Path("./hl2_complete/scripts")
    
    # Define extraction targets
    extractions = [
        {
            "name": "game sounds weapons",
            "output": output_dir / "game_sounds_weapons_episodic.txt",
            "start": 0x4428969,
            "end": 0x44293CA
        },
        {
            "name": "level sounds aftermath",
            "output": output_dir / "level_sounds_aftermath_episodic.txt", 
            "start": 0x448EB04,
            "end": 0x44964C6
        },
        {
            "name": "level sounds c17_02a",
            "output": output_dir / "level_sounds_c17_02a.txt", 
            "start": 0x44964C7,
            "end": 0x4496AEA
        },
        {
            "name": "level sounds music",
            "output": output_dir / "level_sounds_music_episodic.txt", 
            "start": 0x4496AEB,
            "end": 0x4497E4C
        },
        {
            "name": "level sounds outland",
            "output": output_dir / "level_sounds_outland_episodic.txt", 
            "start": 0x4497E4D,
            "end": 0x4498E06
        },
        {
            "name": "level voices episode 01",
            "output": output_dir / "level_voices_episode_01.txt", 
            "start": 0x4498E07,
            "end": 0x44ED292
        },
        {
            "name": "level voices episode 02",
            "output": output_dir / "level_voices_episode_02.txt", 
            "start": 0x44ED293,
            "end": 0x44EDC47
        },
        {
            "name": "npc sounds advisor",
            "output": output_dir / "npc_sounds_advisor.txt", 
            "start": 0x44EDCBC,
            "end": 0x44EF01C
        },
        {
            "name": "npc sounds alyx",
            "output": output_dir / "npc_sounds_alyx_episodic.txt", 
            "start": 0x44EF01D,
            "end": 0x450A1A6
        },
        {
            "name": "npc sounds antlion",
            "output": output_dir / "npc_sounds_antlion_episodic.txt", 
            "start": 0x450A1A7,
            "end": 0x450A8FF
        },
        {
            "name": "npc sounds antlion guard",
            "output": output_dir / "npc_sounds_antlionguard_episodic.txt", 
            "start": 0x450A900,
            "end": 0x450B17C
        },
        {
            "name": "npc sounds citizen ep1",
            "output": output_dir / "npc_sounds_citizen_ep1.txt", 
            "start": 0x450B17D,
            "end": 0x45172A8
        },
        {
            "name": "npc sounds citizen episodic",
            "output": output_dir / "npc_sounds_citizen_episodic.txt", 
            "start": 0x45172A9,
            "end": 0x451819F
        },
        {
            "name": "npc sounds combine ball",
            "output": output_dir / "npc_sounds_combine_ball_episodic.txt", 
            "start": 0x45181A0,
            "end": 0x451859A
        },
        {
            "name": "npc sounds dog",
            "output": output_dir / "npc_sounds_dog_episodic.txt", 
            "start": 0x451859B,
            "end": 0x451A94A
        },
        {
            "name": "npc sounds ministrider",
            "output": output_dir / "npc_sounds_ministrider_episodic.txt", 
            "start": 0x451A94B,
            "end": 0x451B7B3
        },
        {
            "name": "npc sounds roller",
            "output": output_dir / "npc_sounds_roller_episodic.txt", 
            "start": 0x451B7B4,
            "end": 0x451B894
        },
        {
            "name": "npc sounds soldier",
            "output": output_dir / "npc_sounds_soldier_episodic.txt", 
            "start": 0x451B895,
            "end": 0x451BCEE
        },
        {
            "name": "npc sounds stalker",
            "output": output_dir / "npc_sounds_stalker.txt", 
            "start": 0x451BCEF,
            "end": 0x451D6D4
        },
        {
            "name": "npc sounds strider",
            "output": output_dir / "npc_sounds_strider_episodic.txt", 
            "start": 0x451D6D5,
            "end": 0x451D99E
        },
        {
            "name": "npc sounds turret",
            "output": output_dir / "npc_sounds_turret_episodic.txt", 
            "start": 0x451D99F,
            "end": 0x451DA4E
        },
        {
            "name": "npc sounds zombine",
            "output": output_dir / "npc_sounds_zombine.txt", 
            "start": 0x451DA4F,
            "end": 0x451E384
        },
        {
            "name": "weapon alyxgun",
            "output": output_dir / "weapon_alyxgun.txt", 
            "start": 0x455A963,
            "end": 0x455AE99
        }
    ]
    
    try:
        if not vpk_path.exists():
            raise FileNotFoundError("ep1_pak_001.vpk not found")
            
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract each target
        with open(vpk_path, 'rb') as vpk:
            for extract in extractions:
                num_bytes = extract["end"] - extract["start"] + 1
                vpk.seek(extract["start"])
                data = vpk.read(num_bytes)
                
                with open(extract["output"], 'wb') as f:
                    f.write(data)
                    
                print(f"Successfully extracted {extract['name']} to {extract['output']}")
            
    except FileNotFoundError:
        print("Error: ep1_pak_001.vpk not found")
    except PermissionError:
        print("Error: No permission to read/write files") 
    except Exception as e:
        print(f"Error extracting sounds: {str(e)}")

def restore_backups():
    """Restores all backup files to their original locations"""
    
    directories = [
        Path("./hl2/cfg"),
        Path("./episodic/cfg"),
        Path("./episodic/scripts"),
        Path("./hl2/scripts"),
        Path("./hl2_complete/scripts"),
        Path("./hl2_complete/bin")
    ]
    
    restored = False
    
    try:
        for directory in directories:
            if not directory.exists():
                continue
                
            # Find all .backup files
            backup_files = directory.glob("*.backup")
            
            for backup in backup_files:
                try:
                    # Get original filename by removing .backup extension
                    original_name = backup.name.rsplit('.backup', 1)[0]
                    original = directory / original_name
                    
                    # Restore backup
                    shutil.copy2(backup, original)
                    print(f"Restored {original.name} from backup")
                    restored = True
                    
                except Exception as e:
                    print(f"Error restoring {backup.name}: {str(e)}")
                    
        if restored:
            print("Backup restoration complete!")
        else:
            print("No backup files found to restore")
            
    except Exception as e:
        print(f"Error during restoration: {str(e)}")

def randomize_health_values():
    """Randomizes health values in skill.cfg within user specified range"""

    user_choice = input("Do you want to randomize health values? (y/n): ").lower()
    if user_choice != 'y':
        print("Health randomization cancelled.")
        return
    
    cfg_paths = [
        Path("./episodic/cfg/skill_episodic.cfg"),
        Path("./hl2/cfg/skill.cfg")
    ]
    excluded = ["vial", "kit", "charger", "increments"]
    
    try:
        # Check if any config exists
        if not any(path.exists() for path in cfg_paths):
            raise FileNotFoundError("No skill.cfg files found")

        # Process each config file
        for cfg_path in cfg_paths:
            if not cfg_path.exists():
                continue

            # Create backup if it doesn't exist
            backup_path = cfg_path.with_suffix('.cfg.backup')
            if not backup_path.exists():
                shutil.copy2(cfg_path, backup_path)
                print(f"Created backup of {cfg_path.name}")

            # Get range from user (only once)
            if 'min_val' not in locals():
                range_input = input("Enter health range (min-max) or press Enter for default 10-750: ").strip()
                if range_input:
                    min_val, max_val = map(int, range_input.split('-'))
                else:
                    min_val, max_val = 10, 750

            # Read and process file
            with open(cfg_path, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if "health" in line.lower() and not any(x in line.lower() for x in excluded):
                    match = re.search(r'"(\d+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = random.randint(min_val, max_val)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized health value in {cfg_path.name}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(cfg_path, 'w') as f:
                f.writelines(modified)
                
            print(f"Health values randomization complete for {cfg_path.name}!")

    except FileNotFoundError:
        print("Error: No skill.cfg files found")
    except PermissionError:
        print("Error: No permission to modify/backup skill.cfg files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 10-750)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_damage_values():
    """Randomizes damage values in skill.cfg within user specified range"""

    user_choice = input("Do you want to randomize damage values? (y/n): ").lower()
    if user_choice != 'y':
        print("Damage randomization cancelled.")
        return
    
    cfg_paths = [
        Path("./episodic/cfg/skill_episodic.cfg"),
        Path("./hl2/cfg/skill.cfg")
    ]
    excluded = ["scale"]
    damage_keywords = ["dmg", "shock", "kick", "damage"]
    
    try:
        # Check if any config exists
        if not any(path.exists() for path in cfg_paths):
            raise FileNotFoundError("No skill.cfg files found")

        # Process each config file
        for cfg_path in cfg_paths:
            if not cfg_path.exists():
                continue

            # Create backup if it doesn't exist
            backup_path = cfg_path.with_suffix('.cfg.backup')
            if not backup_path.exists():
                shutil.copy2(cfg_path, backup_path)
                print(f"Created backup of {cfg_path.name}")

            # Get range from user (only once)
            if 'min_val' not in locals():
                range_input = input("Enter damage range (min-max) or press Enter for default 2-150: ").strip()
                if range_input:
                    min_val, max_val = map(int, range_input.split('-'))
                else:
                    min_val, max_val = 2, 150

            # Read and process file
            with open(cfg_path, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if any(keyword in line.lower() for keyword in damage_keywords) and not any(x in line.lower() for x in excluded):
                    if "strider" in line.lower():
                        match = re.search(r'\s(\d+)\s*$', line)
                    else:
                        match = re.search(r'"(\d+)"', line)
                    
                    if match:
                        old_val = match.group(1)
                        new_val = random.randint(min_val, max_val)
                        if "strider" in line.lower():
                            line = re.sub(r'\s\d+\s*$', f' {new_val}\n', line)
                        else:
                            line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized damage value in {cfg_path.name}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(cfg_path, 'w') as f:
                f.writelines(modified)
                
            print(f"Damage values randomization complete for {cfg_path.name}!")

    except FileNotFoundError:
        print("Error: No skill.cfg files found")
    except PermissionError:
        print("Error: No permission to modify/backup skill.cfg files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 2-150)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_max_ammo():
    """Randomizes max ammo values in skill.cfg within user specified range"""

    user_choice = input("Do you want to randomize max ammo values? (y/n): ").lower()
    if user_choice != 'y':
        print("Ammo randomization cancelled.")
        return
    
    cfg_paths = [
        Path("./episodic/cfg/skill_episodic.cfg"),
        Path("./hl2/cfg/skill.cfg")
    ]
    excluded = ["armor"]
    ammo_keywords = ["max"]
    
    try:
        if not any(path.exists() for path in cfg_paths):
            raise FileNotFoundError("No skill.cfg files found")

        # Get range from user (only once)
        range_input = input("Enter max ammo range (min-max) or press Enter for default 3-255: ").strip()
        if range_input:
            min_val, max_val = map(int, range_input.split('-'))
        else:
            min_val, max_val = 3, 255

        # Process each config file
        for cfg_path in cfg_paths:
            if not cfg_path.exists():
                continue
                
            # Create backup if it doesn't exist
            backup_path = cfg_path.with_suffix('.cfg.backup')
            if not backup_path.exists():
                shutil.copy2(cfg_path, backup_path)
                print(f"Created backup of {cfg_path.name}")

            # Read and process file
            with open(cfg_path, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if any(keyword in line.lower() for keyword in ammo_keywords) and not any(x in line.lower() for x in excluded):
                    match = re.search(r'"(\d+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = random.randint(min_val, max_val)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized max ammo value in {cfg_path.name}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(cfg_path, 'w') as f:
                f.writelines(modified)
                
            print(f"Max ammo randomization complete for {cfg_path.name}!")

    except FileNotFoundError:
        print("Error: No skill.cfg files found")
    except PermissionError:
        print("Error: No permission to modify/backup skill.cfg files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 3-255)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_chargers_and_pickups():
    """Randomizes charger and pickup values in skill.cfg within user specified range"""

    user_choice = input("Do you want to randomize charger and pickup values? (y/n): ").lower()
    if user_choice != 'y':
        print("Charger and pickup randomization cancelled.")
        return
    
    cfg_paths = [
        Path("./episodic/cfg/skill_episodic.cfg"),
        Path("./hl2/cfg/skill.cfg")
    ]
    keywords = ["battery", "charger", "kit", "vial"]
    
    try:
        # Check if any config exists
        if not any(path.exists() for path in cfg_paths):
            raise FileNotFoundError("No skill.cfg files found")

        # Get range from user (only once)
        if 'min_val' not in locals():
            range_input = input("Enter charger and pickup range (min-max) or press Enter for default 15-500: ").strip()
            if range_input:
                min_val, max_val = map(int, range_input.split('-'))
            else:
                min_val, max_val = 15, 500

        # Process each config file
        for cfg_path in cfg_paths:
            if not cfg_path.exists():
                continue

            # Create backup if it doesn't exist
            backup_path = cfg_path.with_suffix('.cfg.backup')
            if not backup_path.exists():
                shutil.copy2(cfg_path, backup_path)
                print(f"Created backup of {cfg_path.name}")

            # Read and process file
            with open(cfg_path, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if any(keyword in line.lower() for keyword in keywords):
                    match = re.search(r'"(\d+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = random.randint(min_val, max_val)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized charger and pickup value in {cfg_path.name}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(cfg_path, 'w') as f:
                f.writelines(modified)
                
            print(f"Charger and pickup randomization complete for {cfg_path.name}!")

    except FileNotFoundError:
        print("Error: No skill.cfg files found")
    except PermissionError:
        print("Error: No permission to modify/backup skill.cfg files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 15-500)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_damage_adjusters():
    """Randomizes damage multiplier values in skill.cfg for body parts"""

    user_choice = input("Do you want to randomize damage adjusters? (y/n): ").lower()
    if user_choice != 'y':
        print("Damage adjuster randomization cancelled.")
        return
    
    cfg_paths = [
        Path("./episodic/cfg/skill_episodic.cfg"),
        Path("./hl2/cfg/skill.cfg")
    ]
    body_parts = ["head", "chest", "stomach", "arm", "leg"]
    
    try:
        if not any(path.exists() for path in cfg_paths):
            raise FileNotFoundError("No skill.cfg files found")

        # Get range from user (only once)
        range_input = input("Enter damage adjuster range (min-max) or press Enter for default 0-3: ").strip()
        if range_input:
            min_val, max_val = map(float, range_input.split('-'))
        else:
            min_val, max_val = 0.0, 3.0

        # Process each config file
        for cfg_path in cfg_paths:
            if not cfg_path.exists():
                continue

            # Create backup if it doesn't exist
            backup_path = cfg_path.with_suffix('.cfg.backup')
            if not backup_path.exists():
                shutil.copy2(cfg_path, backup_path)
                print(f"Created backup of {cfg_path.name}")

            # Read and process file
            with open(cfg_path, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if any(re.search(rf'(^|[\s_]){part}([\s_]|$)', line.lower()) for part in body_parts):
                    match = re.search(r'"([\d.]+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = round(random.uniform(min_val, max_val), 1)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized damage adjuster in {cfg_path.name}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(cfg_path, 'w') as f:
                f.writelines(modified)
                
            print(f"Damage adjuster randomization complete for {cfg_path.name}!")

    except FileNotFoundError:
        print("Error: No skill.cfg files found")
    except PermissionError:
        print("Error: No permission to modify/backup skill.cfg files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 0-3)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_weapon_clips():
    """Randomizes weapon clip sizes and default clips in weapon scripts"""
    
    user_choice = input("Do you want to randomize weapon clip sizes? (y/n): ").lower()
    if user_choice != 'y':
        print("Weapon clip randomization cancelled.")
        return
    
    source_dir = Path("./hl2/scripts")
    target_dir = Path("./hl2_complete/scripts")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Files to copy and modify in new directory
    weapon_files = ["weapon_smg1.txt", "weapon_rpg.txt", "weapon_crossbow.txt", "weapon_annabelle.txt", "weapon_alyxgun.txt"]
    
    try:
        # Get range from user
        range_input = input("Enter clip size range (min-max) or press Enter for default 2-45: ").strip()
        if range_input:
            min_val, max_val = map(int, range_input.split('-'))
        else:
            min_val, max_val = 2, 45

        # First pass - handle non-listed weapon files in original directory
        for file in source_dir.glob("weapon_*.txt"):
            if file.name not in weapon_files:
                # Create backup
                backup_path = file.with_suffix('.txt.backup')
                if not backup_path.exists():
                    shutil.copy2(file, backup_path)
                    print(f"Created backup of {file.name}")
                
                # Modify original
                with open(file, 'r') as f:
                    lines = f.readlines()
                
                modified = []
                clip_size_new = None
                
                for line in lines:
                    if "clip_size" in line.lower() and file.name not in weapon_files:
                        match = re.search(r'"(\d+)"', line)
                        if match:
                            old_val = int(match.group(1))
                            if old_val > 1:
                                new_val = random.randint(min_val, max_val)
                                clip_size_new = new_val
                                line = line.replace(f'"{old_val}"', f'"{new_val}"')
                                print(f"Randomized clip size in {file.name}: {old_val} -> {new_val}")
                    elif "default_clip" in line.lower() and clip_size_new:
                        match = re.search(r'"(\d+)"', line)
                        if match:
                            old_val = int(match.group(1))
                            if old_val > 1:
                                line = line.replace(f'"{old_val}"', f'"{clip_size_new}"')
                                print(f"Updated default clip in {file.name}: {old_val} -> {clip_size_new}")
                    modified.append(line)
                
                with open(file, 'w') as f:
                    f.writelines(modified)

        # Second pass - handle listed files in target directory
        for filename in weapon_files:
            source_file = source_dir / filename
            target_file = target_dir / filename
            
            # Copy file if it doesn't exist in target
            if source_file.exists() and not target_file.exists():
                shutil.copy2(source_file, target_file)
                print(f"Copied {filename} to {target_dir}")
            
            # Process target file if it exists
            if target_file.exists():
                # Create backup in target directory
                backup_path = target_file.with_suffix('.txt.backup')
                if not backup_path.exists():
                    shutil.copy2(target_file, backup_path)
                    print(f"Created backup of {filename} in {target_dir}")
            
            # Modify copy
            with open(target_file, 'r') as f:
                lines = f.readlines()
            
            modified = []
            clip_size_new = None
            
            for line in lines:
                if "clip_size" in line.lower():
                    match = re.search(r'"(\d+)"', line)
                    if match:
                        old_val = int(match.group(1))
                        if old_val > 1:
                            new_val = random.randint(min_val, max_val)
                            clip_size_new = new_val
                            line = line.replace(f'"{old_val}"', f'"{new_val}"')
                            print(f"Randomized clip size in copied {filename}: {old_val} -> {new_val}")
                elif "default_clip" in line.lower() and clip_size_new:
                    match = re.search(r'"(\d+)"', line)
                    if match:
                        old_val = int(match.group(1))
                        if old_val > 1:
                            line = line.replace(f'"{old_val}"', f'"{clip_size_new}"')
                            print(f"Updated default clip in copied {filename}: {old_val} -> {clip_size_new}")
                modified.append(line)
            
            with open(target_file, 'w') as f:
                f.writelines(modified)
                
        print("Weapon clip randomization complete!")
        
    except FileNotFoundError:
        print("Error: Weapon script files not found")
    except PermissionError:
        print("Error: No permission to modify files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 2-45)")
    except Exception as e:
        print(f"Error: {str(e)}")

def shuffle_ammo_types():
    """shuffles ammo type strings in weapon scripts"""
    
    user_choice = input("Do you want to shuffle ammo types? (y/n): ").lower()
    if user_choice != 'y':
        print("Ammo type shuffle cancelled.")
        return

    source_dir = Path("./hl2/scripts")
    target_dir = Path("./hl2_complete/scripts")
    target_dir.mkdir(parents=True, exist_ok=True)
    
    weapon_files = ["weapon_smg1.txt", "weapon_rpg.txt", "weapon_crossbow.txt", "weapon_annabelle.txt", "weapon_alyxgun.txt"]
    
    ammo_types = [
        "357", "AlyxGun", "AR2", "AR2AltFire", "XBowBolt",
        "grenade", "Pistol", "rpg_round", "Buckshot", 
        "SMG1", "SMG1_Grenade"
    ]

    try:
        # Create master shuffle of ammo types
        shuffled_types = ammo_types.copy()
        random.shuffle(shuffled_types)
        ammo_map = dict(zip(ammo_types, shuffled_types))
        
        # Create regex pattern for exact matches
        ammo_pattern = re.compile('|'.join(f'"{re.escape(ammo)}"' for ammo in ammo_types))

        # Process non-listed files first
        for file in source_dir.glob("weapon_*.txt"):
            if file.name not in weapon_files:
                # Create backup
                backup_path = file.with_suffix('.txt.backup')
                if not backup_path.exists():
                    shutil.copy2(file, backup_path)
                    print(f"Created backup of {file.name}")

                # Read file and replace ammos
                with open(file, 'r') as f:
                    content = f.read()
                
                # Replace ammos using consistent mapping
                result = []
                last_end = 0
                for match in ammo_pattern.finditer(content):
                    orig_ammo = match.group(0)[1:-1]  # Strip quotes
                    new_ammo = ammo_map[orig_ammo]
                    result.append(content[last_end:match.start()])
                    result.append(f'"{new_ammo}"')
                    last_end = match.end()
                    print(f"In {file.name}: {orig_ammo} -> {new_ammo}")
                result.append(content[last_end:])
                modified = ''.join(result)

                with open(file, 'w') as f:
                    f.write(modified)

        # Process listed files in target dir
        for filename in weapon_files:
            source_file = source_dir / filename
            target_file = target_dir / filename
            
            # Copy if needed
            if source_file.exists() and not target_file.exists():
                shutil.copy2(source_file, target_file)
                print(f"Copied {filename} to {target_dir}")
            
            if target_file.exists():
                # Create backup
                backup_path = target_file.with_suffix('.txt.backup')
                if not backup_path.exists():
                    shutil.copy2(target_file, backup_path)
                    print(f"Created backup of {filename} in {target_dir}")

                # Read and process using same ammo mapping
                with open(target_file, 'r') as f:
                    content = f.read()

                result = []
                last_end = 0
                for match in ammo_pattern.finditer(content):
                    orig_ammo = match.group(0)[1:-1]  # Strip quotes
                    new_ammo = ammo_map[orig_ammo]
                    result.append(content[last_end:match.start()])
                    result.append(f'"{new_ammo}"')
                    last_end = match.end()
                    print(f"In {filename}: {orig_ammo} -> {new_ammo}")
                result.append(content[last_end:])
                modified = ''.join(result)

                with open(target_file, 'w') as f:
                    f.write(modified)

        print("Ammo type shuffle complete!")

    except FileNotFoundError:
        print("Error: Weapon script files not found") 
    except PermissionError:
        print("Error: No permission to modify/backup weapon scripts")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_weapon_sounds():
    """Randomizes weapon sound references in weapon scripts"""
    
    user_choice = input("Do you want to randomize weapon sounds? (y/n): ").lower()
    if user_choice != 'y':
        print("Weapon sound randomization cancelled.")
        return

    source_dir = Path("./hl2/scripts")
    target_dir = Path("./hl2_complete/scripts")
    target_dir.mkdir(parents=True, exist_ok=True)
    sounds_file = Path("./weaponsounds_ep1.txt")
    weapon_files = ["weapon_smg1.txt", "weapon_rpg.txt", "weapon_crossbow.txt", "weapon_annabelle.txt", "weapon_alyxgun.txt"]

    if not sounds_file.exists():
        print("Error: weaponsounds.txt not found")
        return

    try:
        # Load available sounds
        with open(sounds_file, 'r') as f:
            sounds = [line.strip() for line in f if line.strip()]
            
        if not sounds:
            print("No sounds found in weaponsounds.txt")
            return

        sound_pattern = re.compile('|'.join(f'"{re.escape(sound)}"' for sound in sounds))
        replacements_made = set()

        # First pass - handle non-listed files
        for file in source_dir.glob("weapon_*.txt"):
            if file.name not in weapon_files:
                # Create backup
                backup_path = file.with_suffix('.txt.backup')
                if not backup_path.exists():
                    shutil.copy2(file, backup_path)
                    print(f"Created backup of {file.name}")
                
                # Modify original
                with open(file, 'r') as f:
                    content = f.read()

                def replacer(match):
                    original = match.group(0)[1:-1]
                    remaining = [x for x in sounds if x != original]
                    if remaining:
                        new_sound = random.choice(remaining)
                        replacement = f"{original} -> {new_sound}"
                        if replacement not in replacements_made:
                            print(f"Randomized sound: {replacement}")
                            replacements_made.add(replacement)
                        return f'"{new_sound}"'
                    return match.group(0)

                modified = sound_pattern.sub(replacer, content)

                if modified != content:
                    with open(file, 'w') as f:
                        f.write(modified)

        # Second pass - handle listed files in target directory
        for filename in weapon_files:
            source_file = source_dir / filename
            target_file = target_dir / filename
            
            # Copy file if it doesn't exist in target
            if source_file.exists() and not target_file.exists():
                shutil.copy2(source_file, target_file)
                print(f"Copied {filename} to {target_dir}")
            
            # Process target file if it exists
            if target_file.exists():
                # Create backup in target directory
                backup_path = target_file.with_suffix('.txt.backup')
                if not backup_path.exists():
                    shutil.copy2(target_file, backup_path)
                    print(f"Created backup of {filename} in {target_dir}")
            
            # Modify copy
            with open(target_file, 'r') as f:
                content = f.read()

            modified = sound_pattern.sub(replacer, content)

            if modified != content:
                with open(target_file, 'w') as f:
                    f.write(modified)

        if replacements_made:
            print("Weapon sound randomization complete!")
        else:
            print("No sounds found to randomize")

    except FileNotFoundError:
        print("Error: Required files not found")
    except PermissionError:
        print("Error: No permission to modify/backup files")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_surface_density():
    """Randomizes surface density values in surfaceproperties.txt/surfaceproperties_hl2.txt within user specified range"""

    user_choice = input("Do you want to randomize surface density values? (y/n): ").lower()
    if user_choice != 'y':
        print("Surface density randomization cancelled.")
        return
    
    scripts_dir = Path("./hl2/scripts/")
    surface_files = list(scripts_dir.glob("surfaceproperties*.txt"))

    if not surface_files:
        print("No surface properties files found")
        return
    
    try:
        # Get range from user
        range_input = input("Enter surface density range (min-max) or press Enter for default 150-2700: ").strip()
        if range_input:
            min_val, max_val = map(int, range_input.split('-'))
        else:
            min_val, max_val = 150, 2700

        # Process each surface file
        for surface_file in surface_files:
            backup_path = surface_file.with_suffix('.txt.backup')
            
            # Create backup if it doesn't exist
            if not backup_path.exists():
                shutil.copy2(surface_file, backup_path)
                print(f"Created backup of {surface_file.name}")

            # Read and process file
            with open(surface_file, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if "density" in line.lower():
                    # Extract number without quotes
                    match = re.search(r'"(\d+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = random.randint(min_val, max_val)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized density value for {line.strip()}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(surface_file, 'w') as f:
                f.writelines(modified)
            
        print("Surface density randomization complete!")

    except FileNotFoundError:
        print("Error: Surface properties files not found")
    except PermissionError:
        print("Error: No permission to modify/backup surface properties files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 150-2700)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_surface_dampening():
    """Randomizes surface dampening values in surfaceproperties.txt/surfaceproperties_hl2.txt within user specified range"""

    user_choice = input("Do you want to randomize surface dampening values? (y/n): ").lower()
    if user_choice != 'y':
        print("Surface dampening randomization cancelled.")
        return
    
    scripts_dir = Path("./hl2/scripts/")
    surface_files = list(scripts_dir.glob("surfaceproperties*.txt"))

    if not surface_files:
        print("No surface properties files found")
        return
    
    try:
        # Get range from user
        range_input = input("Enter surface dampening range (min-max) or press Enter for default 0-200: ").strip()
        if range_input:
            min_val, max_val = map(float, range_input.split('-'))
        else:
            min_val, max_val = 0.0, 200.0

        # Process each surface file
        for surface_file in surface_files:
            backup_path = surface_file.with_suffix('.txt.backup')
            
            if not backup_path.exists():
                shutil.copy2(surface_file, backup_path)
                print(f"Created backup of {surface_file.name}")

            with open(surface_file, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if "dampening" in line.lower():
                    # Extract float number from quotes
                    match = re.search(r'"([\d.]+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = round(random.uniform(min_val, max_val))
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized dampening value for {line.strip()}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(surface_file, 'w') as f:
                f.writelines(modified)
            
        print("Surface dampening randomization complete!")

    except FileNotFoundError:
        print("Error: Surface properties files not found")
    except PermissionError:
        print("Error: No permission to modify/backup surface properties files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 0-200)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_surface_elasticity():
    """Randomizes surface elasticity values in surfaceproperties.txt/surfaceproperties_hl2.txt within user specified range"""

    user_choice = input("Do you want to randomize surface elasticity values? (y/n): ").lower()
    if user_choice != 'y':
        print("Surface elasticity randomization cancelled.")
        return
    
    scripts_dir = Path("./hl2/scripts/")
    surface_files = list(scripts_dir.glob("surfaceproperties*.txt"))

    if not surface_files:
        print("No surface properties files found")
        return
    
    try:
        # Get range from user
        range_input = input("Enter surface elasticity range (min-max) or press Enter for default 0.001-1.000: ").strip()
        if range_input:
            min_val, max_val = map(float, range_input.split('-'))
        else:
            min_val, max_val = 0.001, 1.000

        # Process each surface file
        for surface_file in surface_files:
            backup_path = surface_file.with_suffix('.txt.backup')
            
            if not backup_path.exists():
                shutil.copy2(surface_file, backup_path)
                print(f"Created backup of {surface_file.name}")

            with open(surface_file, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if "elasticity" in line.lower():
                    # Extract float number from quotes
                    match = re.search(r'"([\d.]+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = round(random.uniform(min_val, max_val), 3)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized elasticity value for {line.strip()}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(surface_file, 'w') as f:
                f.writelines(modified)
            
        print("Surface elasticity randomization complete!")

    except FileNotFoundError:
        print("Error: Surface properties files not found")
    except PermissionError:
        print("Error: No permission to modify/backup surface properties files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 0.001-1.000)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_surface_friction():
    """Randomizes surface friction values in surfaceproperties.txt/surfaceproperties_hl2.txt within user specified range"""

    user_choice = input("Do you want to randomize surface friction values? (y/n): ").lower()
    if user_choice != 'y':
        print("Surface friction randomization cancelled.")
        return
    
    scripts_dir = Path("./hl2/scripts/")
    surface_files = list(scripts_dir.glob("surfaceproperties*.txt"))

    if not surface_files:
        print("No surface properties files found")
        return
    
    try:
        # Get range from user
        range_input = input("Enter surface friction range (min-max) or press Enter for default 0.000-1.337: ").strip()
        if range_input:
            min_val, max_val = map(float, range_input.split('-'))
        else:
            min_val, max_val = 0.000, 1.337

        # Process each surface file
        for surface_file in surface_files:
            backup_path = surface_file.with_suffix('.txt.backup')
            
            if not backup_path.exists():
                shutil.copy2(surface_file, backup_path)
                print(f"Created backup of {surface_file.name}")

            with open(surface_file, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if "friction" in line.lower():
                    # Extract float number from quotes
                    match = re.search(r'"([\d.]+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = round(random.uniform(min_val, max_val), 3)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized friction value for {line.strip()}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(surface_file, 'w') as f:
                f.writelines(modified)
            
        print("Surface friction randomization complete!")

    except FileNotFoundError:
        print("Error: Surface properties files not found")
    except PermissionError:
        print("Error: No permission to modify/backup surface properties files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 0.000-1.337)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_surface_thickness():
    """Randomizes surface thickness values in surfaceproperties.txt/surfaceproperties_hl2.txt within user specified range"""

    user_choice = input("Do you want to randomize surface thickness values? (y/n): ").lower()
    if user_choice != 'y':
        print("Surface thickness randomization cancelled.")
        return
    
    scripts_dir = Path("./hl2/scripts/")
    surface_files = list(scripts_dir.glob("surfaceproperties*.txt"))

    if not surface_files:
        print("No surface properties files found")
        return
    
    try:
        # Get range from user
        range_input = input("Enter surface thickness range (min-max) or press Enter for default 0.04-1.00: ").strip()
        if range_input:
            min_val, max_val = map(float, range_input.split('-'))
        else:
            min_val, max_val = 0.04, 1.00

        # Process each surface file
        for surface_file in surface_files:
            backup_path = surface_file.with_suffix('.txt.backup')
            
            if not backup_path.exists():
                shutil.copy2(surface_file, backup_path)
                print(f"Created backup of {surface_file.name}")

            with open(surface_file, 'r') as f:
                lines = f.readlines()

            # Process lines
            modified = []
            for line in lines:
                if "thickness" in line.lower():
                    # Extract float number from quotes
                    match = re.search(r'"([\d.]+)"', line)
                    if match:
                        old_val = match.group(1)
                        new_val = round(random.uniform(min_val, max_val), 2)
                        line = line.replace(f'"{old_val}"', f'"{new_val}"')
                        print(f"Randomized thickness value for {line.strip()}: {old_val} -> {new_val}")
                modified.append(line)

            # Write back
            with open(surface_file, 'w') as f:
                f.writelines(modified)
            
        print("Surface thickness randomization complete!")

    except FileNotFoundError:
        print("Error: Surface properties files not found")
    except PermissionError:
        print("Error: No permission to modify/backup surface properties files")
    except ValueError:
        print("Error: Invalid range format. Use min-max (e.g. 0.04-1.00)")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_surface_sounds():
    """Randomizes surface sound references in surface scripts"""
    
    user_choice = input("Do you want to randomize surface sounds? (y/n): ").lower()
    if user_choice != 'y':
        print("Surface sound randomization cancelled.")
        return

    # Paths setup
    sounds_file = Path("./surfacesounds.txt")
    scripts_dir = Path("./hl2/scripts")
    surface_files = list(scripts_dir.glob("surfaceproperties*.txt"))
    
    if not surface_files:
        print("No surface script files found")
        return
        
    if not sounds_file.exists():
        print("Error: surfacesounds.txt not found")
        return

    try:
        # Load available sounds
        with open(sounds_file, 'r') as f:
            sounds = [line.strip() for line in f if line.strip()]
            
        if not sounds:
            print("No sounds found in surfacesounds.txt")
            return

        # Create regex pattern for exact matches
        sound_pattern = re.compile('|'.join(f'"{re.escape(sound)}"' for sound in sounds))
        replacements_made = set()

        # Process each surface file
        for surface_file in surface_files:
            backup_path = surface_file.with_suffix('.txt.backup')
            
            if not backup_path.exists():
                shutil.copy2(surface_file, backup_path)
                print(f"Created backup of {surface_file.name}")

            with open(surface_file, 'r') as f:
                content = f.read()

            def replacer(match):
                original = match.group(0)[1:-1]  # Remove quotes
                remaining = [x for x in sounds if x != original]
                if remaining:
                    new_sound = random.choice(remaining)
                    replacement = f"{original} -> {new_sound}"
                    if replacement not in replacements_made:
                        print(f"Randomized sound: {replacement}")
                        replacements_made.add(replacement)
                    return f'"{new_sound}"'
                return match.group(0)

            modified = sound_pattern.sub(replacer, content)

            if modified != content:
                with open(surface_file, 'w') as f:
                    f.write(modified)

        if replacements_made:
            print("Surface sound randomization complete!")
        else:
            print("No sounds found to randomize")

    except FileNotFoundError:
        print("Error: Required files not found")
    except PermissionError:
        print("Error: No permission to modify/backup files")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_other_sounds():
    """Randomizes sound references in NPC, level and game sound scripts"""
    
    user_choice = input("Do you want to randomize other sound files (NPC, level and game sounds) (This may overwrite some of the previous sound randomization options.)? (y/n): ").lower()
    if user_choice != 'y':
        print("Other sound randomization cancelled.")
        return

    # Paths setup
    sounds_file = Path("./hl2_complete/maps/sounds&music.txt")
    script_dirs = [
        Path("./hl2/scripts"),
        Path("./hl2_complete/scripts")
    ]
    sound_files = []
    
    # Gather all relevant sound files from both directories
    patterns = ["npc_sounds*.txt", "level_sounds*.txt", "game_sounds*.txt"]
    for script_dir in script_dirs:
        for pattern in patterns:
            sound_files.extend(script_dir.glob(pattern))
    
    if not sound_files:
        print("No sound script files found")
        return
        
    if not sounds_file.exists():
        print("Error: sounds&music.txt not found")
        return

    try:
        # Load available sounds
        with open(sounds_file, 'r') as f:
            sounds = [line.strip() for line in f if line.strip()]
            
        if not sounds:
            print("No sounds found in sounds&music.txt")
            return

        # Create regex pattern for exact matches
        sound_pattern = re.compile('|'.join(f'"{re.escape(sound)}"' for sound in sounds))
        replacements_made = set()

        # Process each sound file
        for sound_file in sound_files:
            backup_path = sound_file.with_suffix('.txt.backup')
            
            if not backup_path.exists():
                shutil.copy2(sound_file, backup_path)
                print(f"Created backup of {sound_file.name}")

            with open(sound_file, 'r') as f:
                content = f.read()

            def replacer(match):
                original = match.group(0)[1:-1]  # Remove quotes
                remaining = [x for x in sounds if x != original]
                if remaining:
                    new_sound = random.choice(remaining)
                    replacement = f"{original} -> {new_sound}"
                    if replacement not in replacements_made:
                        print(f"Randomized sound: {replacement}")
                        replacements_made.add(replacement)
                    return f'"{new_sound}"'
                return match.group(0)

            modified = sound_pattern.sub(replacer, content)

            if modified != content:
                with open(sound_file, 'w') as f:
                    f.write(modified)

        if replacements_made:
            print("Other sound randomization complete!")
        else:
            print("No sounds found to randomize")

    except FileNotFoundError:
        print("Error: Required files not found")
    except PermissionError:
        print("Error: No permission to modify/backup files")
    except Exception as e:
        print(f"Error: {str(e)}")

def kill_vital_npcs():
    """
    Modifies server.dll to toggle vital NPC protection.
    Creates backup before modification.
    """
    server_dll_path = Path("./hl2_complete/bin/server.dll")
    backup_path = server_dll_path.with_suffix('.dll.backup')
    
    try:
        # Validate file exists
        if not server_dll_path.exists():
            raise FileNotFoundError("server.dll not found")

        # Create backup
        if not backup_path.exists():
            shutil.copy2(server_dll_path, backup_path)
            print("Created backup of server.dll")

        while True:
            user_choice = input("Allow killing vital NPCs? (y/n): ").lower()
            if user_choice in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'")

        byte_value = b'\x01' if user_choice == 'y' else b'\x03'
        
        with open(server_dll_path, 'rb+') as f:
            f.seek(0x2DFDF1)
            f.write(byte_value)
            
        print(f"Successfully modified server.dll - Vital NPC protection: {'disabled' if user_choice == 'y' else 'enabled'}")
            
    except FileNotFoundError:
        print("Error: server.dll not found")
    except PermissionError:
        print("Error: No permission to modify server.dll")
    except Exception as e:
        print(f"Error: {str(e)}")

def fix_alyxgun_viewmodel():
    """Fixes Alyx gun viewmodel by replacing model and animation references"""

    user_choice = input("Do you want to fix Alyx gun viewmodel? (y/n): ").lower()
    if user_choice != 'y':
        print("Alyx gun viewmodel fix cancelled.")
        return
    elif user_choice == 'y':
        print("Fixing Alyx gun viewmodel...")
    
    weapon_file = Path("./hl2_complete/scripts/weapon_alyxgun.txt")
    backup_path = weapon_file.with_suffix('.txt.backup')
    
    try:
        if not weapon_file.exists():
            raise FileNotFoundError("weapon_alyxgun.txt not found")

        # Create backup if it doesn't exist
        if not backup_path.exists():
            shutil.copy2(weapon_file, backup_path)
            print("Created backup of weapon_alyxgun.txt")

        # Read and process file
        with open(weapon_file, 'r') as f:
            lines = f.readlines()

        # Process lines
        modified = []
        for line in lines:
            if "viewmodel" in line.lower() and "models/weapons/W_Alyx_Gun.mdl" in line:
                old_line = line
                line = line.replace("models/weapons/W_Alyx_Gun.mdl", "models/weapons/v_pistol.mdl")
                print(f"Updated viewmodel reference from: {old_line.strip()} to: {line.strip()}")
            elif "anim_prefix" in line.lower() and "alyxgun" in line.lower():
                old_line = line
                line = line.replace("alyxgun", "pistol")
                print(f"Updated animation prefix from: {old_line.strip()} to: {line.strip()}")
            modified.append(line)

        # Write back
        with open(weapon_file, 'w') as f:
            f.writelines(modified)
            
        print("Alyx gun viewmodel fix complete!")

    except FileNotFoundError:
        print("Error: weapon_alyxgun.txt not found")
    except PermissionError:
        print("Error: No permission to modify/backup weapon_alyxgun.txt")
    except Exception as e:
        print(f"Error: {str(e)}")

def lift_heavy_objects():
    """
    Modifies server.dll to allow lifting heavier objects.
    Creates backup before modification.
    """
    server_dll_path = Path("./hl2_complete/bin/server.dll")
    backup_path = server_dll_path.with_suffix('.dll.backup')
    
    try:
        # Validate file exists
        if not server_dll_path.exists():
            raise FileNotFoundError("server.dll not found")

        # Create backup
        if not backup_path.exists():
            shutil.copy2(server_dll_path, backup_path)
            print("Created backup of server.dll")

        while True:
            user_choice = input("Enable lifting heavy objects? (y/n): ").lower()
            if user_choice in ['y', 'n']:
                break
            print("Please enter 'y' or 'n'")

        if user_choice == 'y':
            with open(server_dll_path, 'rb+') as f:
                # First value // Max Mass (Player)
                f.seek(0x518DD8)
                f.write(bytes.fromhex('F0237449'))
                # Second value // Max Size (Player) (doesn't seem to do anything but I wanted to includde it anyway just in case)
                f.seek(0x518DDC)
                f.write(bytes.fromhex('F0237449'))
                # Third value // Max Mass (Gravity Gun)
                f.seek(0x19DB3)
                f.write(bytes.fromhex('24AF5D'))
                # Fourth value // Tracelength (Gravity Gun)
                f.seek(0x19F03)
                f.write(bytes.fromhex('24AF5D'))
            
            print("Successfully modified server.dll - Heavy object lifting enabled")
        else:
            print("Heavy object lifting modification cancelled")
            
    except FileNotFoundError:
        print("Error: server.dll not found")
    except PermissionError:
        print("Error: No permission to modify server.dll")
    except Exception as e:
        print(f"Error: {str(e)}")

def randomize_drops():
    """Randomizes what items various entities drop"""
    
    user_choice = input("Do you want to randomize entity drops? (y/n): ").lower()
    if user_choice != 'y':
        print("Drop randomization cancelled.")
        return

    server_dll_path = Path("./hl2_complete/bin/server.dll")
    asm_file = Path("./asm_ents_ep1.txt")
    asm_models_file = Path("./asm_npc_models_ep1.txt")
    backup_path = server_dll_path.with_suffix('.dll.backup')

    # Offset pairs that must match
    linked_pairs = [
        (0x36629E, 0x366860),  # Combine drop pair
        (0x366565, 0x366854),  # Combine drop pair
        (0x366493, 0x366848),  # Combine drop pair
        (0x3A0051, 0x3A06AD),  # Manhack pair
        (0x3E7F61, 0x3E6201),  # NPC pair
        (0x374441, 0x374451),  # NPC pair
        (0x671F90, 0x671F94)   # Headcrab pair
    ]
    
    # Track which pairs use model replacements
    model_linked_pairs = {
        0x3E7F61: "npc",
        0x374441: "npc",
        0x671F90: "headcrab"
    }
    
    # Single offsets
    any_entity_offsets = [0x3BBE1B]
    headcrab_offsets = [0x65F188, 0x65F184, 0x65F180]
    
    # Add manhack pairs to track NPC-only replacements
    manhack_primary_offsets = {0x3A0051}
    
    try:
        if not all(p.exists() for p in [server_dll_path, asm_file, asm_models_file]):
            raise FileNotFoundError("Required files not found")

        # Create backup
        if not backup_path.exists():
            shutil.copy2(server_dll_path, backup_path)
            print("Created backup of server.dll")

        # Parse asm files
        entities = {}
        npc_entities = {}
        headcrab_entities = {}
        model_values = {}
        
        # Read models file first to maintain line correspondence
        with open(asm_models_file, 'r') as f:
            for i, line in enumerate(f):
                if '|' in line:
                    hex_val, name = line.strip().split('|')
                    model_values[i] = bytes.fromhex(hex_val)[::-1]  # Convert to little endian

        # Read entities file
        with open(asm_file, 'r') as f:
            for i, line in enumerate(f):
                if '|' in line:
                    hex_val, name = line.strip().split('|')
                    le_hex = bytes.fromhex(hex_val)[::-1]
                    entities[le_hex] = (name, i)  # Store line number
                    if 'npc' in name.lower():
                        npc_entities[le_hex] = (name, i)
                    if 'headcrab' in name.lower():
                        headcrab_entities[le_hex] = (name, i)

        with open(server_dll_path, 'rb+') as f:
            # Handle linked pairs
            for primary, secondary in linked_pairs:
                f.seek(primary)
                current_hex = f.read(3)
                current_name = entities.get(current_hex, ("Unknown", -1))[0]
                
                if primary in model_linked_pairs:
                    # Use appropriate entity list
                    if model_linked_pairs[primary] == "npc":
                        new_hex = random.choice(list(npc_entities.keys()))
                        new_name, line_num = npc_entities[new_hex]
                    else:  # headcrab
                        new_hex = random.choice(list(headcrab_entities.keys()))
                        new_name, line_num = headcrab_entities[new_hex]
                    
                    # Update model value writing
                    model_hex = model_values[line_num]
                    
                    f.seek(primary)
                    f.write(new_hex)
                    f.seek(secondary)
                    f.write(model_hex)
                    print(f"Changed {model_linked_pairs[primary]} entity/model pair at {hex(primary)}: {current_name} -> {new_name}")
                    
                elif primary in manhack_primary_offsets:
                    new_hex = random.choice(list(npc_entities.keys()))
                    new_name = npc_entities[new_hex][0]
                    f.seek(primary)
                    f.write(new_hex)
                    f.seek(secondary)
                    f.write(new_hex)
                    print(f"Changed NPC-only linked drop at {hex(primary)}: {current_name} -> {new_name}")
                    
                else:
                    new_hex = random.choice(list(entities.keys()))
                    new_name = entities[new_hex][0]
                    f.seek(primary)
                    f.write(new_hex)
                    f.seek(secondary)
                    f.write(new_hex)
                    print(f"Changed linked drop at {hex(primary)}: {current_name} -> {new_name}")

            # Handle any-entity offsets
            for offset in any_entity_offsets:
                f.seek(offset)
                current_hex = f.read(3)
                current_name = entities.get(current_hex, "Unknown")
                new_hex = random.choice(list(entities.keys()))
                new_name = entities[new_hex]
                
                f.seek(offset)
                f.write(new_hex)
                print(f"Changed entity drop at {hex(offset)}: {current_name} -> {new_name}")

            # Handle headcrab-only offsets
            for offset in headcrab_offsets:
                f.seek(offset)
                current_hex = f.read(3)
                current_name = entities.get(current_hex, "Unknown")
                new_hex = random.choice(list(headcrab_entities.keys()))
                new_name = headcrab_entities[new_hex]
                
                f.seek(offset)
                f.write(new_hex)
                print(f"Changed headcrab entity at {hex(offset)}: {current_name} -> {new_name}")

            # Modify float load
            f.seek(0x3BBE07)
            f.write(bytes.fromhex('50'))
            print(f"Set battery drop rate at {hex(0x3BBE07)} to be 100%")

        print("Drop randomization complete!")
            
    except FileNotFoundError:
        print("Error: Required files not found")
    except PermissionError:
        print("Error: No permission to modify files")
    except Exception as e:
        print(f"Error: {str(e)}")

def shuffle_firerates():
    """Shuffles weapon firerate values between weapons"""
    
    user_choice = input("Do you want to shuffle weapon firerates? (y/n): ").lower()
    if user_choice != 'y':
        print("Firerate shuffle cancelled.")
        return

    server_dll_path = Path("./hl2_complete/bin/server.dll")
    backup_path = server_dll_path.with_suffix('.dll.backup')
    
    # Map offsets to weapon names
    firerate_offsets = {
        0x40E2C2: "AR2/Alyx Gun",
        0x340122: "Crowbar",
        0x40E9B2: "Annabelle",
        0x4288E2: "SMG",
        0x2B3C62: "Pistol"
    }
    
    try:
        if not server_dll_path.exists():
            raise FileNotFoundError("server.dll not found")

        # Create backup
        if not backup_path.exists():
            shutil.copy2(server_dll_path, backup_path)
            print("Created backup of server.dll")

        # First read all original values
        original_values = {}
        with open(server_dll_path, 'rb') as f:
            for offset in firerate_offsets:
                f.seek(offset)
                original_values[offset] = f.read(3)

        # Create shuffled mapping ensuring no value goes back to same offset
        while True:
            shuffled_offsets = list(firerate_offsets.keys())
            random.shuffle(shuffled_offsets)
            if not any(a == b for a, b in zip(firerate_offsets.keys(), shuffled_offsets)):
                break

        # Create mapping of where each value should go
        new_locations = {}
        for orig_offset, new_offset in zip(firerate_offsets.keys(), shuffled_offsets):
            new_locations[new_offset] = original_values[orig_offset]
            print(f"{firerate_offsets[new_offset]}'s firerate is now {firerate_offsets[orig_offset]}'s firerate")

        # Write all values to their new locations
        with open(server_dll_path, 'rb+') as f:
            for offset, value in new_locations.items():
                f.seek(offset)
                f.write(value)

        # Make the crowbar a ranged weapon for the funny
        with open(server_dll_path, 'rb+') as f:
            f.seek(0x340222)
            f.write(bytes.fromhex('38'))

        print("Firerate shuffle complete!")
            
    except FileNotFoundError:
        print("Error: server.dll not found")
    except PermissionError:
        print("Error: No permission to modify server.dll")
    except Exception as e:
        print(f"Error: {str(e)}")

def remove_sprint_usage():
    """Removes suit sprint energy usage"""
    
    user_choice = input("Do you want to remove suit sprint energy usage? (y/n): ").lower()
    if user_choice != 'y':
        print("Sprint energy usage modification cancelled.")
        return

    server_dll_path = Path("./hl2_complete/bin/server.dll")
    backup_path = server_dll_path.with_suffix('.dll.backup')
    
    try:
        if not server_dll_path.exists():
            raise FileNotFoundError("server.dll not found")

        # Create backup
        if not backup_path.exists():
            shutil.copy2(server_dll_path, backup_path)
            print("Created backup of server.dll")

        with open(server_dll_path, 'rb+') as f:
            f.seek(0x663C9C)
            f.write(bytes.fromhex('00000000'))
            
        print("Successfully modified server.dll - Sprint energy usage disabled")
            
    except FileNotFoundError:
        print("Error: server.dll not found")
    except PermissionError:
        print("Error: No permission to modify server.dll")
    except Exception as e:
        print(f"Error: {str(e)}")

def remove_health_cap():
    """Removes health cap and sets max armor to 750"""
    
    user_choice = input("Do you want to remove health cap and increase max armor to 750? (I know this option seems weird at first but I promise it'll help balance things if you choose yes on the next four options.) (y/n): ").lower()
    if user_choice != 'y':
        print("Health cap modification cancelled.")
        return

    server_dll_path = Path("./hl2_complete/bin/server.dll")
    backup_path = server_dll_path.with_suffix('.dll.backup')
    
    try:
        if not server_dll_path.exists():
            raise FileNotFoundError("server.dll not found")

        # Create backup
        if not backup_path.exists():
            shutil.copy2(server_dll_path, backup_path)
            print("Created backup of server.dll")

        with open(server_dll_path, 'rb+') as f:
            # Remove health cap
            f.seek(0x4FF50)
            f.write(bytes.fromhex('909090909090'))
            
            # Set max battery pickup limit to 750
            f.seek(0x2E1D87)
            f.write(bytes.fromhex('341D4D'))
            
            # Set battery charge limit and fill amount to 750 (fill amount is a side effect, wontfix)
            f.seek(0x2E1DBA)
            f.write(bytes.fromhex('68EE0200009090'))
            
            # Set suit charger limit to 750
            f.seek(0x2CCB99)
            f.write(bytes.fromhex('EE02'))
            
            # Set suit charger incrementation to 750 (not respecting actual size of the charger is a side effect, wontfix)
            f.seek(0x2CCBB0)
            f.write(bytes.fromhex('EE02'))
            
            # Increase health charger speed
            f.seek(0x2F42E4)
            f.write(bytes.fromhex('D4'))
            
        print("Successfully modified server.dll - Health cap removed and max armor increased to 750")
            
    except FileNotFoundError:
        print("Error: server.dll not found")
    except PermissionError:
        print("Error: No permission to modify server.dll")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    extract_vpk_stuff()
    restore_backups()
    kill_vital_npcs()
    fix_alyxgun_viewmodel()
    lift_heavy_objects()
    randomize_drops()
    shuffle_firerates()
    remove_sprint_usage()
    remove_health_cap()
    randomize_health_values()
    randomize_damage_values()
    randomize_chargers_and_pickups()
    randomize_damage_adjusters()
    randomize_max_ammo()
    randomize_weapon_clips()
    shuffle_ammo_types()
    randomize_weapon_sounds()
    randomize_surface_density()
    randomize_surface_dampening()
    randomize_surface_elasticity()
    randomize_surface_friction()
    randomize_surface_thickness()
    randomize_surface_sounds()
    randomize_other_sounds()