"""This holds all of the functions used to check for mod conflicts and issues."""
import re
from universal_functions import *
from base_game_variables import *

# mod_directory = r'D:\Games\steamapps\common\DarkestDungeon\mods\mod_folder'


def start_check(mod_directory):
    with open(rf'mod_conflicts.txt', 'w') as f:
        # Clears the text file.
        mod_folder_name = mod_directory.split("\\")[-1]
        f.write(f'Results for Mod Folder: {mod_folder_name}')


def check_dungeon_mashes(mod_directory):
    all_available_monsters = get_mod_monster_variants(mod_directory) + base_monster_variant_ids
    dungeon_mash_monster_ids = get_dungeon_mash_monster_ids(mod_directory)
    with open(rf'mod_conflicts.txt', 'a') as f:
        if len(dungeon_mash_monster_ids[0]) > 0:
            f.write('\n\n**DUNGEON MASH ERRORS**\n')
        for monster in dungeon_mash_monster_ids[0]:
            if monster not in all_available_monsters:
                if monster == '':
                    continue
                f.write(f'\nMINOR DEFECT: Monster of ID {monster} does not exist. Mash exists in the following folder(s):')
                for folder in dungeon_mash_monster_ids[1][monster]:
                    f.write('\n')
                    f.write(folder)


def check_inventory_item_images(mod_directory):
    all_mod_inventory_items_by_file = get_mod_inventory_items_by_type(mod_directory)

    # Check for images.
    missing_images = []
    for item_type in all_mod_inventory_items_by_file:
        item_type_items = all_mod_inventory_items_by_file[item_type]
        item_type = item_type
        if item_type not in os.listdir(fr'{mod_directory}\panels\icons_equip'):
            available_images = []
        else:
            available_images = os.listdir(fr'{mod_directory}\panels\icons_equip\{item_type}')
        for item in item_type_items:
            if item.isnumeric():
                continue
            if f'inv_{item_type}+{item}.png' not in available_images:
                missing_images.append(f'MINOR DEFECT: {item_type} Item with ID {item} is missing an image.')

    with open(rf'mod_conflicts.txt', 'a') as f:
        if len(missing_images) > 0:
            f.write('\n\n**INVENTORY IMAGE ERRORS**\n')
        f.writelines('\n'.join(missing_images))


def check_monster_brains(mod_directory):
    with open(rf'mod_conflicts.txt', 'a') as f:
        """Scripts to check the monsters START"""
        if 'monsters' in os.listdir(mod_directory):
            all_monsters_folders = os.listdir(f"{mod_directory}/monsters")
        else:
            all_monsters_folders = []
        list_of_monsters = []
        for monster in all_monsters_folders:
            list_of_monsters.append(monster)

        """Scripts to check if the monsters brains are throwing any errors. START"""
        list_of_monsters_brains = []
        # Gets a list of all of the monster variants brain names and appends them to a list.
        for monster in list_of_monsters:
            monster_variants = os.listdir(f"{mod_directory}/monsters/{monster}")
            for variant in monster_variants:
                if os.path.isdir(f"{mod_directory}/monsters/{monster}/{variant}"):
                    pass
                else:
                    continue
                if variant not in os.listdir(f"{mod_directory}/monsters/{monster}"):
                    continue
                if f'{variant}.info.darkest' not in os.listdir(f"{mod_directory}/monsters/{monster}/{variant}"):
                    continue
                if monster in variant:
                    with open(f"{mod_directory}/monsters/{monster}/{variant}/{variant}.info.darkest", "r") as variant_info_file:
                        variant_info_string = variant_info_file.readlines()
                        monster_brain_obj = filter(lambda a: 'monster_brain' in a, variant_info_string)
                        monster_brain_line = list(monster_brain_obj)[0]
                        monster_brain_line = monster_brain_line.split('.id ')[1]
                        monster_brain_line = monster_brain_line.replace('\n', '')
                        monster_brain = monster_brain_line.strip()
                        list_of_monsters_brains.append(monster_brain)
                else:
                    continue
        list_of_monsters_brains = list(set(list_of_monsters_brains))

        if 'raid' in os.listdir(mod_directory):
            if 'ai' in os.listdir(f"{mod_directory}/raid"):
                monster_brain_files = os.listdir(f"{mod_directory}/raid/ai")
            else:
                monster_brain_files = []
                # monster_brain_files = []
        else:
            monster_brain_files = []
        all_ai_names = []
        # Gets all of the available monster brains within the mod's ai file and appends them to a list.
        for monster_brain_file_name in monster_brain_files:
            with open(f"{mod_directory}/raid/ai/{monster_brain_file_name}") as monster_brain_file:
                monster_brain_dicts = json.load(monster_brain_file)
                for monster_brain_dict in monster_brain_dicts['monster_brains']:
                    all_ai_names.append(monster_brain_dict['id'])
        # Gets all of the available monster brains from the base game and appends them to the same list.

        all_ai_names = all_ai_names + base_ai_names

        # Checks if any of the brains are missing.
        missing_brains = []
        for monsters_brain in list_of_monsters_brains:
            if monsters_brain not in all_ai_names:
                missing_brains.append(monsters_brain)

        if len(missing_brains) > 0:
            f.write('\n\n**MONSTER BRAIN ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following monster brains do not exist: {missing_brains}')


def check_monster_effects(mod_directory):
    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write('\n\n**MONSTER EFFECTS ERRORS**\n')
        """Scripts to check the monsters START"""
        if 'monsters' in os.listdir(mod_directory):
            all_monsters_folders = os.listdir(f"{mod_directory}/monsters")
        else:
            all_monsters_folders = []
        list_of_monsters = []
        for monster in all_monsters_folders:
            list_of_monsters.append(monster)

        """Scripts to check if the monsters effects are throwing any errors. START"""
        list_of_monsters_effects = []
        dict_of_monsters_with_effects = defaultdict(list)
        # Gets a list of all of the monster variants effect names and appends them to a list.
        for monster in list_of_monsters:
            monster_variants = os.listdir(f"{mod_directory}/monsters/{monster}")
            for variant in monster_variants:
                if os.path.isdir(f"{mod_directory}/monsters/{monster}/{variant}"):
                    pass
                else:
                    continue
                if variant not in os.listdir(f"{mod_directory}/monsters/{monster}"):
                    continue
                if f'{variant}.info.darkest' not in os.listdir(f"{mod_directory}/monsters/{monster}/{variant}"):
                    continue
                if monster in variant:
                    with open(f"{mod_directory}/monsters/{monster}/{variant}/{variant}.info.darkest", "r") as variant_info_file:
                        variant_info_string = variant_info_file.readlines()
                        variant_monster_effects = []
                        ability_effects_obj = filter(lambda a: 'skill:' in a, variant_info_string)
                        capture_effects_obj = filter(lambda a: 'captor_full:' in a, variant_info_string)
                        capture_effects_lines = list(capture_effects_obj)
                        monster_effects_lines = list(ability_effects_obj)
                        for monster_effects_line in monster_effects_lines:
                            if '.effect' in monster_effects_line:
                                monster_effects_line = monster_effects_line.split('.effect')[1]
                                monster_effects_line = monster_effects_line.split(' .')[0]
                                all_variant_effects = re.findall(r'"(.*?)"', monster_effects_line)
                                for effect in all_variant_effects:
                                    list_of_monsters_effects.append(effect)
                                    dict_of_monsters_with_effects[variant].append(effect)
                        for capture_effects_line in capture_effects_lines:
                            if '.release_effects' in capture_effects_line:
                                capture_effects_line = capture_effects_line.split('.release_effects')[1]
                                capture_effects_line = capture_effects_line.split(' .')[0]
                                all_variant_effects = re.findall(r'"(.*?)"', capture_effects_line)
                                for effect in all_variant_effects:
                                    list_of_monsters_effects.append(effect)
                                    dict_of_monsters_with_effects[variant].append(effect)

                else:
                    continue

        all_available_effects = get_mod_effects(mod_directory) + base_effect_names

        for monster_variant in dict_of_monsters_with_effects:
            for effect in dict_of_monsters_with_effects[monster_variant]:
                if effect not in all_available_effects:
                    f.write(f'\nMINOR DEFECT: {monster_variant} has effect {effect} which does not exist.')


def check_quirk_buffs(mod_directory):
    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write('\n\n**QUIRK BUFF ERRORS**\n')
        # Get all needed available variables to check against.
        if 'shared' in os.listdir(mod_directory):
            if 'quirk' in os.listdir(f'{mod_directory}/shared'):
                all_quirk_json_files = os.listdir(f"{mod_directory}/shared/quirk")
            else:
                all_quirk_json_files = []
        else:
            all_quirk_json_files = []
        all_available_buffs = get_mod_buffs(mod_directory) + base_buff_names

        # Check Quirk Buffs
        all_mod_quirk_buffs = []
        for quirk_json_file in all_quirk_json_files:
            # Gets all Mod Quirk Buffs
            if '.quirk_library.json' in quirk_json_file:
                json_file_path = f'{mod_directory}/shared/quirk/{quirk_json_file}'
                with open(json_file_path) as json_file:
                    dicts = json.load(json_file)
                    for given_dict in dicts['quirks']:
                        quirk_buffs = given_dict['buffs']
                        for buff in quirk_buffs:
                            all_mod_quirk_buffs.append(buff)

        # Error Checking
        for mod_quirk_buff in all_mod_quirk_buffs:
            if mod_quirk_buff not in all_available_buffs:
                f.write(f'\nMAJOR DEFECT: Buff {mod_quirk_buff} does not exist as a buff.')


def check_quirk_evolutions(mod_directory):
    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write('\n\n**QUIRK EVOLUTION ERRORS**\n')
        # Get all needed available variables to check against.
        if 'shared' in os.listdir(mod_directory):
            if 'quirk' in os.listdir(f"{mod_directory}/shared"):
                all_quirk_json_files = os.listdir(f"{mod_directory}/shared/quirk")
            else:
                all_quirk_json_files = []
        else:
            all_quirk_json_files = []
        all_available_quirks = get_mod_quirk_ids(mod_directory) + base_quirk_names

        # Check Quirk Evolutions
        all_mod_quirk_evolutions = []
        for quirk_json_file in all_quirk_json_files:
            # Gets all Mod Quirk Buffs
            if '.quirk_library.json' in quirk_json_file:
                json_file_path = f'{mod_directory}/shared/quirk/{quirk_json_file}'
                with open(json_file_path) as json_file:
                    dicts = json.load(json_file)
                    for given_dict in dicts['quirks']:
                        if 'evolution_class_id' in given_dict:
                            all_mod_quirk_evolutions.append(given_dict['evolution_class_id'])

        # Error Checking
        for mod_quirk_evololution in all_mod_quirk_evolutions:
            if mod_quirk_evololution not in all_available_quirks:
                f.write(f'\nMAJOR DEFECT: Evolution Quirk {mod_quirk_evololution} does not exist as a quirk.')


def check_quirk_incompatibilities(mod_directory):
    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write('\n\n**QUIRK INCOMPATIBILITY ERRORS**\n')
        if 'shared' in os.listdir(mod_directory):
            if 'quirk' in os.listdir(f'{mod_directory}/shared'):
                all_quirk_json_files = os.listdir(f"{mod_directory}/shared/quirk")
            else:
                all_quirk_json_files = []
        else:
            all_quirk_json_files = []
        # Get all needed available variables to check against.
        all_available_quirks = get_mod_quirk_ids(mod_directory) + base_quirk_names

        # Check Incompatible Quirks
        all_mod_incompatible_quirks = []
        for quirk_json_file in all_quirk_json_files:
            # Gets all Mod Quirk Buffs
            if '.quirk_library.json' in quirk_json_file:
                json_file_path = f'{mod_directory}/shared/quirk/{quirk_json_file}'
                with open(json_file_path) as json_file:
                    dicts = json.load(json_file)
                    for given_dict in dicts['quirks']:
                        incompatible_quirks = given_dict['incompatible_quirks']
                        for incompatible_quirk in incompatible_quirks:
                            all_mod_incompatible_quirks.append(incompatible_quirk)

        # Error Checking
        for incompatible_quirk in all_mod_incompatible_quirks:
            if incompatible_quirk not in all_available_quirks:
                f.write(f'\nMINOR DEFECT: Quirk {incompatible_quirk} does not exist as an incompatible quirk. This can be ignored (quirk may exist elsewhere and this will not cause crashes).')


def check_trinkets(mod_directory):
    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write('\n\n**TRINKET ERRORS BEGIN**\n')
        trinket_effect_triggers = ['attack_skill_additional_effects', 'friendly_skill_additional_effects',
                                   'kill_performer_additional_effects', 'kill_all_monsters_additional_effects',
                                   'kill_all_heroes_additional_effects', 'was_killed_all_heroes_additional_effects',
                                   'was_killed_all_monsters_additional_effects', 'was_hit_additional_effects',
                                   'was_hit_all_heroes_additional_effects', 'was_hit_all_monsters_additional_effects',
                                   'melee_attack_skill_additional_effects', 'ranged_attack_skill_additional_effects',
                                   'attack_crit_additional_effects', 'riposte_skill_additional_effects']

        # Gather all trinket files.
        if 'trinkets' in os.listdir(mod_directory):
            all_trinket_json_files = os.listdir(f"{mod_directory}/trinkets")
        else:
            all_trinket_json_files = []
        all_trinket_entries_files = []
        all_trinket_sets_files = []
        all_trinket_rarities_files = []
        for json_file in all_trinket_json_files:
            if '.entries.trinkets' in json_file:
                all_trinket_entries_files.append(json_file)
            elif '.rarities.trinkets' in json_file:
                all_trinket_rarities_files.append(json_file)
            elif '.sets.trinkets' in json_file:
                all_trinket_sets_files.append(json_file)

        # Get all trinket ids, sets, rarities, buffs and effects.
        all_trinket_ids = []
        all_trinket_buffs = []
        all_trinket_effects = []
        all_trinket_rarities = []
        all_trinket_sets = []

        for trinket_entry_file in all_trinket_entries_files:
            with open(f'{mod_directory}/trinkets/{trinket_entry_file}', "r") as json_file:
                dicts = json.load(json_file)
                for given_dict in dicts['entries']:
                    # Add ID.
                    all_trinket_ids.append(given_dict['id'])
                    # Add rarity.
                    all_trinket_rarities.append(given_dict['rarity'])
                    # Add Set.
                    if 'set_id' in given_dict:
                        all_trinket_sets.append(given_dict['set_id'])
                    # Add buffs
                    for buff in given_dict['buffs']:
                        all_trinket_buffs.append(buff)
                    # Add trinket effect trigger effects.
                    for trinket_effect_trigger in trinket_effect_triggers:
                        if trinket_effect_trigger in given_dict:
                            for effect in given_dict[trinket_effect_trigger]:
                                all_trinket_effects.append(effect)

        """
        Compare Buffs
        """""
        all_missing_buffs = []
        all_available_buffs = get_mod_buffs(mod_directory) + base_buff_names
        # Check for missing entries.
        for assigned_buff in all_trinket_buffs:
            if assigned_buff not in all_available_buffs:
                all_missing_buffs.append(assigned_buff)

        # Error Message Here.
        if len(all_missing_buffs) > 0:
            f.write('**TRINKET BUFFS ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following buffs are assigned to trinkets but do not exist:\n{all_missing_buffs}')

        """
        Compare Effects
        """
        all_missing_effects = []
        all_available_effects = get_mod_effects(mod_directory) + base_effect_names
        # Check for missing entries.
        for assigned_effect in all_trinket_effects:
            if assigned_effect not in all_available_effects:
                all_missing_effects.append(assigned_effect)

        # Error Message Here.
        if len(all_missing_effects) > 0:
            f.write('\n\n**TRINKET EFFECTS ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following effects are assigned to trinkets but do not exist:\n{all_missing_effects}')

        """
        Compare Rarities
        """
        # Get a list of all available rarities.
        all_missing_rarities = []
        all_mod_trinket_rarities = []
        for trinket_rarity_file in all_trinket_rarities_files:
            with open(f'{mod_directory}/trinkets/{trinket_rarity_file}', "r") as json_file:
                dicts = json.load(json_file)
                for given_dict in dicts['rarities']:
                    # Add ID.
                    all_mod_trinket_rarities.append(given_dict['id'])
        all_available_rarities = all_mod_trinket_rarities + base_trinket_rarities
        # Check for missing entries.
        for assigned_rarity in all_trinket_rarities:
            if assigned_rarity not in all_available_rarities:
                all_missing_rarities.append(assigned_rarity)

        # Error Message Here.
        if len(all_missing_rarities) > 0:
            f.write('\n\n**TRINKET RARITY ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following rarities are assigned to trinkets but do not exist:\n{all_missing_rarities}')

        """
        Compare Sets
        """
        all_missing_sets = []
        all_missing_set_buffs = []
        all_mod_trinket_sets = []
        all_set_buffs = []
        for trinket_set_file in all_trinket_sets_files:
            with open(f'{mod_directory}/trinkets/{trinket_set_file}', "r") as json_file:
                dicts = json.load(json_file)
                for given_dict in dicts['sets']:
                    # Add ID.
                    all_mod_trinket_sets.append(given_dict['id'])
                    # Add Buffs
                    for buff in given_dict['buffs']:
                        all_set_buffs.append(buff)
        all_available_sets = all_mod_trinket_sets + base_trinket_sets
        # !Available buffs are already set!
        # Check for missing set entries.
        for assigned_set in all_trinket_sets:
            if assigned_set not in all_available_sets:
                all_missing_sets.append(assigned_set)
        # Error Message 1 Here.
        if len(all_missing_sets) > 0:
            f.write('\n\n**TRINKET SET ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following sets are assigned to trinkets but do not exist:\n{all_missing_sets}')
        # Check for missing buff entries.
        for assigned_buff in all_set_buffs:
            if assigned_buff not in all_available_buffs:
                all_missing_set_buffs.append(assigned_buff)
        # Error Message 2 Here.
        if len(all_missing_set_buffs) > 0:
            f.write('\n\n**TRINKET SET BUFF ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following set buffs are assigned to trinkets but do not exist:\n{all_missing_set_buffs}')

        """
        Check Trinket & Rarity Pictures
        """
        all_missing_trinket_images = []
        all_missing_rarity_images = []
        if 'panels' in os.listdir(f"{mod_directory}"):
            if 'icons_equip' in os.listdir(f"{mod_directory}/panels"):
                if 'trinket' in os.listdir(f"{mod_directory}/panels/icons_equip"):
                    all_trinket_image_files = os.listdir(f"{mod_directory}/panels/icons_equip/trinket")
                else:
                    all_trinket_image_files = []
            else:
                all_trinket_image_files = []
        else:
            all_trinket_image_files = []
        # Check for missing trinket images.
        for trinket_id in all_trinket_ids:
            if f'inv_trinket+{trinket_id}.png' not in all_trinket_image_files:
                all_missing_trinket_images.append(trinket_id)
        # Error Message Here.
        if len(all_missing_trinket_images) > 0:
            f.write('\n\n**TRINKET IMAGE ERRORS**\n')
            f.write(f'\nMAJOR DEFECT: The following trinkets do not have images:\n{all_missing_trinket_images}')

        # Check for missing rarity images.
        for rarity_id in all_mod_trinket_rarities:
            if f'rarity_{rarity_id}.png' not in all_trinket_image_files:
                all_missing_rarity_images.append(rarity_id)
        # Error Message Here.
        if len(all_missing_rarity_images) > 0:
            f.write('\n\n**TRINKET RARITY IMAGE ERRORS**\n')
            f.write(f'\nMINOR DEFECT: The following rarities do not have images:\n{all_missing_rarity_images}')
