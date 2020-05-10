hint = ""


def display_user_position(player):
    print("Current Floor:  " + str(player[0] + 1) + ", Current Room: " + str(player[1] + 1))
    return player


def display_user_items(items):
    print("Current items: " + str(items))
    return items


def is_invalidate_command(command, valid_commands):
    if command not in {"left", "right", "up", "down", "grab", "fight", "help"} or \
            command not in set(valid_commands):
        set_hint("Hint: Invalid command, try again!")
        return True
    return False


def update_user_position(command, valid_commands, player, floors):
    if is_invalidate_command(command, valid_commands) or command not in {"left", "right", "up", "down"}:
        return display_user_position(player)

    position_changed = True
    if command == "left" and player[1] - 1 >= 0:
        player[1] = player[1] - 1
    elif command == "right" and player[1] + 1 < len(floors[0]):
        player[1] = player[1] + 1
    elif command == "up" and player[0] + 1 < len(floors):
        player[0] = player[0] + 1
    elif command == "down" and player[0] - 1 >= 0:
        player[0] = player[0] - 1
    else:
        position_changed = False

    if not position_changed:
        set_hint("Hint: No more room in direction - " + command)

    return display_user_position(player)


def update_user_items(encounter, command, valid_commands, items, player, floors):
    if is_invalidate_command(command, valid_commands) or command not in {"grab", "fight"}:
        return display_user_items(items), "in progress", floors

    status = "in progress"

    if command == "grab":
        if len(items) >= 3:
            set_hint("Hint: Cannot grab. You can only hold maximum 3 items!")
            return display_user_items(items), status, floors
        items.append(encounter)
        floors[player[0]][player[1]] = ""
    else:
        status = "loss"
        if encounter == "monster":
            for i in items[:]:
                if i == "sword":
                    items.remove(i)
                    status = "success"
                    floors[player[0]][player[1]] = ""
                    break
        elif encounter == "boss-monster":
            for i in items[:]:
                if i == "sword":
                    items.remove(i)
                    break
            for i in items[:]:
                if i == "magic-stone":
                    items.remove(i)
                    status = "win"
                    floors[player[0]][player[1]] = ""
                    break

    return display_user_items(items), status, floors


def reverse(prev_command):
    res = ""
    if prev_command == "left":
        res = "right"
    elif prev_command == "right":
        res = "left"
    elif prev_command == "up":
        res = "down"
    elif prev_command == "down":
        res = "up"
    return res


# left, right, up, down, grab, fight, help.
def display_commands(encounter, prev_command):
    commands = []
    if encounter == "sword" or encounter == "magic-stone":
        commands.extend(["left", "right", "grab", "help"])
    elif encounter == "up-staircase":
        commands.extend(["left", "right", "up", "help"])
    elif encounter == "down-staircase":
        commands.extend(["left", "right", "down", "help"])
    elif encounter == "monster" or encounter == "boss-monster":
        if prev_command != "":
            commands.append(reverse(prev_command))
        commands.extend(["fight", "help"])
    else:
        commands.extend(["left", "right", "help"])

    print(commands)

    return commands


def help(encounter, command, valid_commands, items, player, floors):
    if is_invalidate_command(command, valid_commands) or command not in {"help"}:
        return items
    pass


def get_hint():
    global hint
    ret = hint
    set_hint("")
    return ret


def set_hint(str):
    global hint
    hint = str
    print(hint)
    pass


def game_cli():
    floors = [["", "sword", "up-staircase", "sword", "monster"],
              ["magic-stone", "monster", "up-staircase", "monster", "down-staircase"],
              ["down-staircase", "", "sword", "", "boss-monster"]]
    player = [0, 0]
    items = []
    status = "in progress"
    current_command = ""

    while status != "win" and status != "loss":
        print("-- This room has: [" + floors[player[0]][player[1]] + "] --")
        commands = display_commands(floors[player[0]][player[1]], current_command)
        current_command = raw_input("From above select your command: ")
        print("\n-----------------")
        items, status, floors = update_user_items(floors[player[0]][player[1]],
                                                  current_command, commands, items, player, floors)
        player = update_user_position(current_command, commands, player, floors)

    print("Game Over! You " + status)
    print("Thanks for playing!")


if __name__ == "__main__":
    game_cli()
