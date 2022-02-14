"""These are functions used to grab variables from a given mod folder."""
import json
import os
from collections import defaultdict


def remove_duplicates_from_list(given_list):
    return list(dict.fromkeys(given_list))


def get_mod_inventory_items_by_type(mod_directory):
    all_items_by_category = defaultdict(list)
    if 'inventory' in os.listdir(mod_directory):
        all_inventory_darkest_files = os.listdir(f"{mod_directory}/inventory")
    else:
        all_inventory_darkest_files = []

    for darkest_inventory_file in all_inventory_darkest_files:
        if '.items.darkest' in darkest_inventory_file:
            item_type = darkest_inventory_file.split('.inventory.items.darkest')[0]
            item_type = item_type.split('.')[-1]
            items_file_path = f'{mod_directory}/inventory/{darkest_inventory_file}'
            with open(items_file_path, "r") as inventory_file:
                inventory_string = inventory_file.readlines()
                inventory_obj = filter(lambda a: 'inventory_item:' in a, inventory_string)
                inventory_lines = list(inventory_obj)
                for inventory_line in inventory_lines:
                    inventory_line = inventory_line.split('.id')[1]
                    inventory_line = inventory_line.split('"')[1]
                    inventory_line = inventory_line.split('"')[0]
                    all_items_by_category[item_type].append(inventory_line)
    return all_items_by_category


def get_mod_buffs(mod_directory):
    """Returns a list of buff ids from the mod folder."""
    all_mod_buff_ids = []
    if 'shared' in os.listdir(mod_directory):
        if 'buffs' in os.listdir(f'{mod_directory}/shared'):
            all_buff_json_files = os.listdir(f"{mod_directory}/shared/buffs")
        else:
            all_buff_json_files = []
    else:
        all_buff_json_files = []
    for buff_json_file in all_buff_json_files:
        if '.buffs.json' in buff_json_file:
            json_file_path = f'{mod_directory}/shared/buffs/{buff_json_file}'
            with open(json_file_path) as json_file:
                dicts = json.load(json_file)
                for given_dict in dicts['buffs']:
                    all_mod_buff_ids.append(given_dict['id'])
    return all_mod_buff_ids


def get_mod_quirk_ids(mod_directory):
    """Returns a list of buff ids from the mod folder."""
    all_mod_quirk_ids = []
    if 'shared' in os.listdir(mod_directory):
        if 'quirk' in os.listdir(f'{mod_directory}/shared'):
            all_quirk_json_files = os.listdir(f"{mod_directory}/shared/quirk")
        else:
            all_quirk_json_files = []
    else:
        all_quirk_json_files = []
    for quirk_json_file in all_quirk_json_files:
        if '.quirk_library.json' in quirk_json_file:
            json_file_path = f'{mod_directory}/shared/quirk/{quirk_json_file}'
            with open(json_file_path) as json_file:
                dicts = json.load(json_file)
                for given_dict in dicts['quirks']:
                    all_mod_quirk_ids.append(given_dict['id'])
    return all_mod_quirk_ids


def get_mod_effects(mod_directory):
    """Returns a list of effect names from the mod folder."""
    all_mod_effect_ids = []
    if 'effects' in os.listdir(mod_directory):
        all_effects_darkest_files = os.listdir(f"{mod_directory}/effects")
    else:
        all_effects_darkest_files = []
    for effects_darkest_file in all_effects_darkest_files:
        if '.effects.darkest' in effects_darkest_file:
            effects_file_path = f'{mod_directory}/effects/{effects_darkest_file}'
            with open(effects_file_path, "r") as effects_file:
                effects_darkest_string = effects_file.readlines()
                effect_obj = filter(lambda a: 'effect:' in a, effects_darkest_string)
                effect_lines = list(effect_obj)
                for effect_line in effect_lines:
                    effect_line = effect_line.split('.name')[1]
                    effect_line = effect_line.split('"')[1]
                    effect_line = effect_line.split('"')[0]
                    all_mod_effect_ids.append(effect_line)
    return all_mod_effect_ids


def get_mod_monster_variants(mod_directory):
    all_mod_monsters = []
    print(os.listdir(mod_directory))
    if 'monsters' not in os.listdir(mod_directory):
        return []
    all_monsters_folders = os.listdir(f"{mod_directory}/monsters")

    # Get a list of all base monsters.
    list_of_monsters = []
    for monster in all_monsters_folders:
        list_of_monsters.append(monster)

    # Get a list of all monster variants.
    for monster in list_of_monsters:
        monster_variants = os.listdir(f"{mod_directory}/monsters/{monster}")
        for variant in monster_variants:
            if variant == 'anim' or variant == 'fx' or variant == 'ui':
                continue
            all_mod_monsters.append(variant)
    return all_mod_monsters


def get_dungeon_mash_monster_ids(mod_directory):
    """Returns a list of dungeon mash monster names from the mod folder."""
    mash_conditions = ['hall', 'room', 'boss', 'named']
    all_mod_mash_monster_ids = []
    all_monsters_and_mash_files = defaultdict(list)
    if 'dungeons' in os.listdir(f"{mod_directory}"):
        all_dungeon_folders = os.listdir(f"{mod_directory}/dungeons")
    else:
        all_dungeon_folders = []
    all_mash_file_paths = []
    for dungeon in all_dungeon_folders:
        dungeon_files = os.listdir(f"{mod_directory}/dungeons/{dungeon}")
        for dungeon_file in dungeon_files:
            if '.mash.darkest' in dungeon_file:
                dungeon_mash_path = f"{mod_directory}/dungeons/{dungeon}/{dungeon_file}"
                all_mash_file_paths.append(dungeon_mash_path)
    for mash_darkest_file in all_mash_file_paths:
        with open(mash_darkest_file, "r") as mash_file:
            mash_darkest_string = mash_file.readlines()
            # print(mash_darkest_string)
            for mash_condition in mash_conditions:
                mash_obj = filter(lambda a: f'{mash_condition}:' in a, mash_darkest_string)
                mash_lines = list(mash_obj)
                for mash_line in mash_lines:
                    mash_line = mash_line.split('.types')[1]
                    mash_line = mash_line.split('.')[0]
                    all_monsters = mash_line.split(' ')
                    for monster in all_monsters:
                        if monster == '':
                            continue
                        elif monster == ' ':
                            continue
                        if '\n' in monster:
                            monster = monster.replace('\n', '')
                        all_mod_mash_monster_ids.append(monster)
                        all_monsters_and_mash_files[monster].append(mash_darkest_file)
    return [all_mod_mash_monster_ids, all_monsters_and_mash_files]


def get_mod_loot_tables(mod_directory):
    """Returns a dict with multiple loot tables and their ids from within a mod."""
