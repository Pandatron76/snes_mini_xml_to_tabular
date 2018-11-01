# Creates an object to store the name of the console, games on it and where they are located on the snes_mini
class EntertainmentConsole:
    def __init__(self, console_name):
        self.console_name = console_name
        self.game_code = ''
        self.game_location_dict = {}

    def add_game_code(self, code):
        self.game_code = code

    def add_game_location_dict(self, game, location):
        self.game_location_dict[game] = location
