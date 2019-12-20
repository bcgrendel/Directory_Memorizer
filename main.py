import json
import sys
import os
import re

import fuzzy_string_comparison

storage_file_path = os.path.dirname(os.path.realpath(__file__)) + "/storage.json"

dir_map = {}
with open(storage_file_path, "r+") as f:
    dir_map = json.load(f)

shortcut_print_length = 20

max_shortcut_len = 1
shortcuts = [x for x in dir_map.keys()]
for shortcut in shortcuts:
    shortcut_len = len(shortcut)
    if shortcut_len > max_shortcut_len:
        max_shortcut_len = shortcut_len

shortcut_print_length = max_shortcut_len + 4
shortcut_param = "%-" + str(shortcut_print_length) + "s"

def add_directory_shortcut(shortcut_name, dir_path):
    global dir_map
    global storage_file_path
    dir_map[shortcut_name] = dir_path
    with open(storage_file_path, "w+") as f:
        print(f"\n  Added: {shortcut_name}    {dir_path}")
        json.dump(dir_map, f)

def remove_directory_shortcut(shortcut_name):
    global dir_map
    global storage_file_path
    if shortcut_name in dir_map.keys():
        dir_path = dir_map[shortcut_name]
        del dir_map[shortcut_name]
        print(f"\n  Deleted: {shortcut_name}    {dir_path}")
        with open(storage_file_path, "w+") as f:
            json.dump(dir_map, f)

def list_directory_shortcuts():
    global dir_map
    global shortcut_param
    shortcuts = sorted([x for x in dir_map.keys()])
    print("")
    for shortcut in shortcuts:
        directory_path = dir_map[shortcut]
        print(("  " + shortcut_param + " %s") % (shortcut, directory_path))

def search_directory_shortcuts(term):
    global dir_map
    global shortcut_param
    search_term = term
    if "%" not in search_term:
        search_term = r".*" + search_term + r".*"
    else:
        search_term = search_term.replace("%", r".*")
    search_term = search_term + r"$"
    shortcuts = sorted([x for x in dir_map.keys()])
    print("")
    for shortcut in shortcuts:
        directory_path = dir_map[shortcut]
        #Check if the search matches this shortcut
        if re.match(search_term, shortcut) != None:
            print(("  " + shortcut_param + " %s") % (shortcut, directory_path))
    

def lookup_directory(shortcut_name):
    global dir_map
    shortcuts = [x for x in dir_map.keys()]
    if shortcut_name in shortcuts:
        sys.stdout.write(dir_map[shortcut_name])
    else:
        closest_shortcut = fuzzy_string_comparison.get_closest_match(shortcut_name, shortcuts)
        sys.stdout.write(dir_map[closest_shortcut])


if __name__ == "__main__":
    first_param = sys.argv[1]
    if first_param.lower() == "-a":
        add_directory_shortcut(sys.argv[2], sys.argv[3])
    elif first_param.lower() == "-r":
        remove_directory_shortcut(sys.argv[2])
    elif first_param.lower() == "-l":
        list_directory_shortcuts()
    elif first_param.lower() == "-s":
        search_directory_shortcuts(sys.argv[2])
    else:
        lookup_directory(first_param)
