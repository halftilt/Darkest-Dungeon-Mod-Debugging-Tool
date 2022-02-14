import os
from tkinter import simpledialog
from tkinter.filedialog import askdirectory
path = askdirectory(title='Choose Folder')  # shows dialog box and return the path

"""This script renames all of the files in a folder.
This is primarily used for making duplicates of monsters with a different ID."""


def rename_files(initial_string='', new_string=''):
    if initial_string == '':
        ask_initial_filename = simpledialog.askstring('Previous String', 'What is the previous string name?')
    else:
        ask_initial_filename = initial_string

    if new_string == '':
        ask_new_file_name = simpledialog.askstring('New String',
                                                   'What is the new string name you wish to update your files to?')
    else:
        ask_new_file_name = new_string
    i = 0

    for filename in os.listdir(path):
        new_string_name = filename.replace(ask_initial_filename, ask_new_file_name)
        source_file = path + '/' + filename
        new_filename_and_directory = path + '/' + new_string_name

        # rename() function will
        # rename all the files
        os.rename(source_file, new_filename_and_directory)
        i += 1


rename_files()
