__author__ = "Pandatron76"
__email__ = "Pandatron76@gmail.com"
__description__ = "Translates the SNES Minis XML file structure format to the command line and tab delimited txt file"

# TODO: Add support for Sega CD, NeoGeo, Mame and Sega Saturn

import xml.etree.ElementTree as Et


# Creates an object to store the name of the console, games on it and where they are located on the snes_mini
class EntertainmentConsole:
    def __init__(self, console_name):
        self.console_name = console_name
        self.list_of_games = []
        self.games_location = []

    def add_game_to_list(self, game):
        self.list_of_games.append(game)

    def add_game_location(self, location):
        self.games_location.append(location)


# For each console, check the game-code to see which console the game is associated to and add it to the consoles dict
def add_game_to_list(current_location, tree_level, all_consoles_1):

    for console in all_consoles_1:
        # Check the name of the console, see if it has a 'code' tag, make sure the code tag matches the expected name

        # Check for nes games
        if 'NES' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-H' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for snes games
        if 'SNES' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-U' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for gb games
        if 'Gameboy' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-B' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for gbc games
        if 'Gameboy Color' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-C' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for gba games
        if 'Gameboy Advance' == console.console_name and \
            tree_level.get('code') is not None and 'CLV-A' in tree_level.get(
                'code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for n64 games
        if 'Nintendo 64' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-6' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for genesis games
        if 'Genesis' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-I' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for playstation games
        if 'Playstation' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-F' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # Check for pre-loaded games
        if 'Preloaded' == console.console_name and \
                tree_level.get('code') is not None and 'CLV-P' in tree_level.get('code'):
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

        # In most cases if the code tag returns None, it is likely a folder
        if 'Folder Names' == console.console_name and tree_level.get('code') is None:
            console.add_game_to_list(tree_level.get('name'))
            console.add_game_location(current_location)

    return all_consoles_1


# List of all the consoles. Will create an EntertainmentConsole object for each one
def console_list():
    return ['NES',
            'SNES',
            'Gameboy',
            'Gameboy Color',
            'Gameboy Advance',
            'Nintendo 64',
            'Genesis',
            'Playstation',
            'Preloaded',
            'Folder Name']


#  Creates a tab delimited header with two columns, each row has the name of the console and the game's name/title
#  TODO: Add support to indicate where the game is located (example: Series/MainStream/Mario)
def output_to_txt(all_consoles_1, file_name):
    final_string = 'Console Name\tTitle\tFolder Location\n'

    for console in all_consoles_1:
        for game_name, games_location in sorted(zip(console.list_of_games, console.games_location)):
            final_string += "%s\t%s\t%s\n" % (console.console_name, game_name, games_location)

    with open(file_name, 'w') as file:
        file.write(final_string)


#  Looks through all the consoles, prints the name of the console and then all games underneath it
def print_to_cli(all_consoles_1):

    for console in all_consoles_1:
        print(console.console_name)
        for game_name, games_location in zip(console.list_of_games, console.games_location):
            print("  %s\t%s\n" % (game_name, games_location))


# TODO: Consolidate main, it should consist primarily/only function calls if possible
def main():

    # Create a place to store the xml data in memory
    xml_data = ''

    # Create Entertainment Console List
    # TODO: Convert this into an object and allow the object to store attribute for folder location
    all_consoles = [EntertainmentConsole(x) for x in console_list()]

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
                current_location = str(top_level.get('name') + '\\' + category.get('name') + '\\' + genre.get('name'))
                # print(str(top_level.get('name') + '\\' + category.get('name') + '\\' + genre.get('name')))
                add_game_to_list(current_location, genre, all_consoles)
                # Names of games in the series OR name of individual game
                for genre_name in genre:
                    add_game_to_list(current_location, genre_name, all_consoles)

    # Print to the Command Line/Terminal
    print_to_cli(all_consoles)
    # Save output to a tab delimited CSV
    output_to_txt(all_consoles, 'mini_games_tab_delimited.txt')


main()
