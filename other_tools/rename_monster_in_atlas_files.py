import os
from tkinter import simpledialog
from tkinter.filedialog import askdirectory

"""This files renames the monster name in all .atlas files in a given folder.
This is primarily used for making duplicates of monsters with a different ID."""

path = askdirectory(title='Choose Folder')  # shows dialog box and return the path


def rename_atlas(initial_string='', new_string=''):
    if initial_string == '':
        ask_initial_string = simpledialog.askstring('Previous String', 'What is the previous string name?')
    else:
        ask_initial_string = initial_string

    if new_string == '':
        ask_new_string = simpledialog.askstring('New String',
                                                   'What is the new string name you wish to update your files to?')
    else:
        ask_new_string = new_string
    for filename in os.listdir(path):
        if '.atlas' in filename:
            # Read in the file
            with open((path + '/' + filename), 'r') as file:
                filedata = file.read()

            # Replace the target string
            filedata = filedata.replace((ask_initial_string + '.'), (ask_new_string + '.'))

            # Write the file out again
            with open((path + '/' + filename), 'w') as file:
                file.write(filedata)


rename_atlas()
