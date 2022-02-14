import re
from tkinter.filedialog import askopenfilename

"""This file is used to create a text file that has all of the language localizations for a given .XML file.
This is primarily used for english only modders that do not have translations in other languages but want the 
non-english players to at least see something instead of blue error text."""

languages = ['english', 'french', "german", "spanish", "brazilian", "russian", "polish", "czech", "italian", "schinese",
             "japanese", "koreanb", "koreana"]

path = askopenfilename(title='Choose an XML File')  # shows dialog box and return the path
with open(path, 'r', encoding="utf8") as xml_string_table:
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
            # print(f'<language id="{language}">\n{m}\n</language>')
            # f = open("temp_xml.xml", "a")
            temp_xml.write(f'<language id="{language}">\n{m}\n</language>\n')
        temp_xml.write('</root>')
        temp_xml.close()
