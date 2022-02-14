"""This file is the primary file for "finding" mod conflicts.
Currently it spits out a text file."""
import os
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import ttk
from universal_functions import *
from error_checking_functions import *


def get_list_of_files(dir_name):
    # create a list of file and sub directories
    # names in the given directory
    list_of_files = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # print(full_path)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            full_path = full_path.split('\\')[-1]
            all_files.append(full_path)

    return all_files


# Get the user's mod directory.
mod_directory = askdirectory(title="Select the Darkest Dungeon mod directory (the folder which contains all of your mods).")  # shows dialog box and return the path
# mod_directory = r'D:\Games\steamapps\common\DarkestDungeon\mods'
all_mod_folders = next(os.walk(mod_directory))[1]

with open(rf'mod_conflicts.txt', 'w') as f:
    # Clears the text file.
    f.write(f'Results for Mod Conflict Finder!')


all_mods_and_mosters_as_dict = defaultdict(list)
all_files = []
all_files_dict = defaultdict(list)

for mod_folder in all_mod_folders:
    mod_path = rf'{mod_directory}\{mod_folder}'

    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write(f'\n\n\n!!***BEGIN MOD ERROR Results for Mod Folder: {mod_folder}***!!')
    check_dungeon_mashes(mod_path)
    check_monster_brains(mod_path)
    check_monster_effects(mod_path)
    check_inventory_item_images(mod_path)
    check_quirk_buffs(mod_path)
    check_quirk_evolutions(mod_path)
    check_quirk_incompatibilities(mod_path)
    check_trinkets(mod_path)
    with open(rf'mod_conflicts.txt', 'a') as f:
        f.write(f'\n\n\n!!***END MOD ERROR Results for Mod Folder: {mod_folder}***!!')
    if len(get_list_of_files(rf'{mod_path}')) == 0:
        continue
    all_files = all_files + get_list_of_files(rf'{mod_path}')
    # print(all_files)
    all_files_dict[mod_folder] = get_list_of_files(rf'{mod_directory}\{mod_folder}')
    if 'monsters' in os.listdir(mod_path):
        mod_monster_variants = get_mod_monster_variants(mod_path)
        for monster_variant in mod_monster_variants:
            all_mods_and_mosters_as_dict[mod_folder].append(monster_variant)
    else:
        continue


# Find files that are duplicates.
dict_of_file_conflicts = {}
for mod in list(all_files_dict):
    # print(mod)
    list_of_files = all_files_dict[mod]
    list_of_files = set(list_of_files)
    # print(list_of_files[-1])
    del all_files_dict[mod]
    for other_mod in list(all_files_dict):
        if other_mod == mod:
            continue
        print(other_mod)
        list_of_other_mod_files = all_files_dict[other_mod]
        list_of_other_mod_files = set(list_of_other_mod_files)
        # print(set(list_of_files).intersection(list_of_other_mod_files))
        dict_of_file_conflicts[f'{mod} & {other_mod}'] = list(set(list_of_files).intersection(list_of_other_mod_files))
        # print(list_of_file_conflicts)


# Find monster file conflicts.
conflicting_monster_statements = []
for mod in all_mods_and_mosters_as_dict:
    all_mod_monsters = all_mods_and_mosters_as_dict[mod]
    for mod_monster in all_mod_monsters:
        for l2_mod in all_mods_and_mosters_as_dict:
            if l2_mod == mod:
                continue
            elif mod_monster in all_mods_and_mosters_as_dict[l2_mod]:
                conflicting_monster_statements.append(
                    f"MAJOR CONFLICT: {l2_mod} AND {mod}! A monster with an ID of {mod_monster} is found in both mods!"
                    + " Resolve this conflict or do not activate these mods together as this could cause a CTD!")

# Create the error file.
# These "ignorable conflicts" are what the finder may think are conflicts but are expected and can be ignored.
ignorable_file_conflicts = ['tint.png', 'modfiles.txt', 'project.xml', 'eqp_weapon_0.png', 'eqp_weapon_1.png',
                            'eqp_weapon_2.png', 'eqp_weapon_3.png', 'eqp_weapon_4.png', 'eqp_armour_0.png',
                            'eqp_armour_1.png', 'eqp_armour_2.png', 'eqp_armour_3.png', 'eqp_armour_4.png',
                            'missing_files.txt', 'steam_workshop_uploader.log', 'fmod.dll', 'preview_icon.png',
                            'glew32.dll', 'SDL2.dll', 'steam_api.dll', 'fmodstudio.dll', 'missing_strings.csv',
                            'png_alpha_colour_remover.exe', 'mask_trim_png.exe', 'localization.bat', 'Thumbs.db']
with open(rf'mod_conflicts.txt', 'a') as f:
    f.write('\n\n**START FILE CONFLICT ERRORS**\n')
    for folder in dict_of_file_conflicts:
        for file_conflict in dict_of_file_conflicts[folder]:
            if file_conflict in ignorable_file_conflicts:
                continue
            f.write(f'\n POTENTIAL CONFLICT: {file_conflict} exists in {folder}')
    f.write('\n\n**CONFLICTING MONSTER ERRORS**\n')
    f.writelines('\n'.join(conflicting_monster_statements))

