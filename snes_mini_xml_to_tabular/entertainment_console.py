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
