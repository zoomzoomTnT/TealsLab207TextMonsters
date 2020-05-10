# Game Env Vars
floors = None
visited = None
player = None
items = None
status = None
current_command = None


def init():
    global floors, visited, player, items, status, current_command

    floors = [["", "sword", "up-staircase", "sword", "monster"],
              ["magic-stone", "monster", "up-staircase", "monster", "down-staircase"],
              ["down-staircase", "", "sword", "", "boss-monster"]]
    visited = [[False, False, False, False, False],
               [False, False, False, False, False],
               [False, False, False, False, False]]
    player = [0, 0]
    items = []
    status = "in progress"
    current_command = ""

    return floors, visited, player, items, status, current_command
