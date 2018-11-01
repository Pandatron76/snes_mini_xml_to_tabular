__author__ = "Pandatron76"
__email__ = "Pandatron76@gmail.com"
__description__ = "Translates the SNES Minis XML file structure format to the command line and tab delimited txt file"

# TODO: Add support for Sega CD, NeoGeo, Mame and Sega Saturn

import xml.etree.ElementTree as Et
from entertainment_console import EntertainmentConsole


# For each console, check the game-code to see which console the game is associated to and add it to the console's list
def add_game_information(console, current_location, tree_level):
    expected_consoles = []

    # Build a list of expected consoles to compare against
    for console_gcode_pair in console_list():
        for console_name in console_gcode_pair.keys():
            expected_consoles.append(console_name)

    # Check the name of the console, see if it has a 'code' tag, make sure the code tag matches the expected name
    for expected_console in expected_consoles:
        if expected_console == console.console_name and \
            tree_level.get('code') is not None and \
                console.game_code in tree_level.get('code') and \
                expected_console != 'File/Folder Name':

            # Store the game name and its location in a dict
            console.add_game_location_dict(tree_level.get('name'), current_location)

        if 'File/Folder Name' == console.console_name and tree_level.get('code') is None:
            # Store the game name and its location in a dict
            console.add_game_location_dict(tree_level.get('name'), current_location)


# List of all the consoles. Will create an EntertainmentConsole object for each one
def console_list():
    return [{'NES': 'CLV-H'},
            {'SNES': 'CLV-U'},
            {'Gameboy': 'CLV-B'},
            {'Gameboy Color': 'CLV-C'},
            {'Gameboy Advance': 'CLV-A'},
            {'Nintendo 64': 'CLV-6'},
            {'Genesis': 'CLV-I'},
            {'Playstation': 'CLV-F'},
            {'Preloaded': 'CLV-P-S'},
            {'File/Folder Name': ''}]


#  Creates a tab delimited header with two columns, each row has the name of the console and the game's name/title
#  TODO: Add support to indicate where the game is located (example: Series/MainStream/Mario)
def output_to_txt(all_consoles_1, file_name):
    final_string = 'Console Name\tTitle\tFile/Folder Name\n'

    for console in all_consoles_1:
        for game_name, games_location in sorted(console.game_location_dict.items()):
            # Folders do not have game names and as such the name of the game for the folder should not be included
            if console.console_name == 'File/Folder Name':
                final_string += "%s\t\t%s\n" % (console.console_name, games_location)
            else:
                final_string += "%s\t%s\t%s\n" % (console.console_name, game_name, games_location)

    with open(file_name, 'w') as file:
        file.write(final_string)


#  Looks through all the consoles, prints the name of the console and then all games underneath it
def print_to_cli(all_consoles_1):

    for console in all_consoles_1:
        print(console.console_name)
        # Folders do not have game names and as such the name of the game for the folder should not be included
        for game_name, games_location in sorted(console.game_location_dict.items()):
            if console.console_name == 'File/Folder Name':
                print("  %s\n" % games_location)
            else:
                print("  %s\t%s\n" % (game_name, games_location))


# TODO: Consolidate main, it should consist primarily/only function calls if possible
def main():

    # Create a place to store the xml data in memory
    xml_data = ''

    # Create Entertainment Console List
    # TODO: Convert this into an object and allow the object to store attribute for folder location
    # all_consoles = [EntertainmentConsole(x) for x in console_list()]
    all_consoles = []

    for console_gcode_dict in console_list():
        for console_name, game_code in console_gcode_dict.items():
            temp_console = EntertainmentConsole(console_name)
            temp_console.add_game_code(game_code)
            all_consoles.append(temp_console)

    # This file can be found in '..\hakchi2-ce\hakchi2-ce-x.y.z-debug\config\'
    with open('large_sample_folders_snes_usa.xml', 'r') as file:
        for line in file:
            xml_data += line

    # XML Parser
    xmlp = Et.XMLParser(encoding="utf-16")

    # Setup root location of the XML
    root = Et.fromstring(xml_data, parser=xmlp)

    # Loop through each level of the XML
    # TODO: Make this dynamic, right now it stops after 3 levels deep
    # My personal library is HOME Menu(root) > Series/Standalone(DIR) > Genre(DIR) > GamesSeries(DIR) > Game(FILE)

    # Directly under root is series and standalone
    for top_level in root:
        # This level covers series genre OR if standalone what system it is on
        for category in top_level:
            # Series name if upper level is series OR genre if Standalone
            for genre in category:

                # Names of games in the series OR name of individual game
                current_location = str(top_level.get('name') + '\\' +
                                       category.get('name') + '\\' +
                                       genre.get('name'))
                for console in all_consoles:
                    add_game_information(console, current_location, genre)

                # Names of games in the series folder. This cover the last depth
                for genre_name in genre:
                    current_location = str(top_level.get('name') + '\\' +
                                           category.get('name') + '\\' +
                                           genre.get('name') + '\\' +
                                           genre_name.get('name'))
                    for console in all_consoles:
                        add_game_information(console, current_location, genre_name)

    # Print to the Command Line/Terminal
    print_to_cli(all_consoles)
    # Save output to a tab delimited CSV
    output_to_txt(all_consoles, 'mini_games_tab_delimited.txt')


main()
