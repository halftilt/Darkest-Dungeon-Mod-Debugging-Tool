import re
from tkinter.filedialog import askopenfilename

"""This file is used to create a text file that has all of the language localizations for a given .XML file.
This is primarily used for english only modders that do not have translations in other languages but want the 
non-english players to at least see something instead of blue error text."""

languages = ['english', 'french', "german", "spanish", "brazilian", "russian", "polish", "czech", "italian", "schinese",
             "japanese", "koreanb", "koreana"]

path = askopenfilename(title='Choose an XML File')  # shows dialog box and return the path
"""with open(path, 'r', encoding="utf8") as xml_string_table:
    start = '<language id="english">'
    end = '</language>'
    english_text = xml_string_table.read()
    pattern = r'<language id="english">(.+?)</language>'
    pattern = r'<language(.)id="english">(.+?)</language>'
    m = re.search('id="english">((.|\n)*?)</language>', english_text).group(1)
    with open("temp_xml.txt", "a", encoding="utf8") as temp_xml:
        temp_xml.truncate(0)
        temp_xml.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<root>\n')
        for language in languages:
            temp_xml.write(f'<language id="{language}">\n{m}\n</language>\n')
        temp_xml.write('</root>')
        temp_xml.close()"""


with open(path, 'r', encoding="utf8") as xml_string_table:
    # Read the chosen XML file.
    all_text = xml_string_table.read()
    # Set up the dictionary to capture all of the language XML entries with their sub entries.
    all_language_xml_entries = {}
    english_lang_m = re.search('id="english">((.|\n)*?)</language>', all_text).group(1)
    all_english_entry_ids = re.findall(f'id="(.*?)"', english_lang_m)
    all_english_entries_dict = {}
    i = 0
    for english_entry_id in all_english_entry_ids:
        # Creates a dictionary for all english entries and makes it a cool thing based off its id, I guess.
        print(english_entry_id)
        if '+' in english_entry_id:
            english_entry_id = english_entry_id.replace('+', r'\+')
        english_entry = re.search(f'<entry id="{english_entry_id}">((.|\n)*?)</entry>', english_lang_m).group()
        all_english_entries_dict[english_entry_id] = english_entry
    for language in languages:
        # Iterates through each available language to create their entry to append to the all XML dictionary.
        current_lang_m = re.search(f'id="{language}">((.|\n)*?)</language>', all_text)
        if current_lang_m is None or language == 'english':
            """Checks if there isn't a language or if the language is english and does what it's gotta do by putting
            english in its place and move onto the next language."""
            # temp_xml.write(f'<language id="{language}">\n{m}\n</language>\n')
            all_language_xml_entries[language] = f'<language id="{language}">\n{english_lang_m}\n</language>\n'
            continue
        # If it isn't None, then we "Group it"; whatever that does. It was needed at one point.
        current_lang_m = current_lang_m.group(1)
        new_english_entries = []
        # Finds all the entry ids and stores them into an array.
        all_entry_ids = re.findall(f'id="(.*?)"', current_lang_m)
        for english_entry_key in all_english_entries_dict.keys():
            # Iterates through the English entries, if it exists in English but not in this language, add it. Otherwise
            # take the current language's version better.
            if english_entry_key not in all_entry_ids:
                new_english_entries.append(all_english_entries_dict[english_entry_key])
            continue
        for new_english_entry in new_english_entries:
            # Adds all of the new entries to the current language translation.
            current_lang_m = current_lang_m + f'\n{new_english_entry}'
        all_language_xml_entries[language] = f'<language id="{language}">\n{current_lang_m}\n</language>\n'
        # print(all_language_xml_entries[language])

    with open("temp_xml.txt", "a", encoding="utf8") as temp_xml:
        # Opens the temporary XML file.
        temp_xml.truncate(0)
        temp_xml.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<root>\n')
        for language in all_language_xml_entries.keys():
            temp_xml.write(f'\n{all_language_xml_entries[language]}\n\n')
        temp_xml.write('</root>')
        temp_xml.close()

# alt_language_pattern = rf'<language(.)id="{"french"}">(.+?)</language>'
# m = re.search('id="english">((.|\n)*?)</language>', english_text).group(1)

