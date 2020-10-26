from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk

retraceSteps = {'n': 's','s': 'n','w': 'e','e': 'w'}


def mapTransversal(current_room, visited=None):
    # list for directions
    directions = []
    # If visited is none create a visited set(empty for now)
    if visited is None:
        visited = set()

    # Find all exits of current room
    for move in player.current_room.get_exits():
        # Move in the selected direction
        player.travel(move)

        # If room was visited, the player retraces steps to find an unvisted path
        if player.current_room in visited:
            player.travel(retraceSteps[move])
        # If the player has not visited this room:
        else:
            # Add room to visited
            visited.add(player.current_room)
            # Append the move to the direction's list
            directions.append(move)
            # recursively call the above loop
            directions += mapTransversal(player.current_room, visited)
            # Move to the previous room
            player.travel(retraceSteps[move])
            # Add retraceSteps to the directions list
            directions.append(retraceSteps[move])

    return directions


# traversal_path = ['n', 'n']
traversal_path = mapTransversal(player.current_room)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
