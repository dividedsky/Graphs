from room import Room
from player import Player
from world import World
from collections import deque
from room_graphs import (
    roomGraph_sm,
    roomGraph_md,
    roomGraph_lg,
    roomGraph_xl,
    roomGraph_xxl,
)

import random

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.

roomGraph = roomGraph_xxl
world.loadGraph(roomGraph)

# UNCOMMENT TO VIEW MAP
# world.printRooms()

player = Player("Name", world.startingRoom)

# FILL THIS IN
traversalPath = []
rooms = {}  # graph to store room info
unexplored = deque()  # queue storing unexplored rooms
unexplored.append(player.currentRoom.id)
opposite_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}


def get_random_move(room):
    # returns a random direction from the unexplored room exits
    exits = room.getExits()
    possible_moves = []
    for exit in exits:
        if rooms[room.id][exit] == "?":
            possible_moves.append(exit)
    if len(possible_moves) == 0:
        return None
    random_idx = random.randrange(len(possible_moves))
    return possible_moves[random_idx]


def add_room_exits(room):
    # adds exits for new room
    exits = room.getExits()
    if room.id not in rooms.keys():
        rooms[room.id] = {}
    for exit in exits:
        if exit not in rooms[room.id]:
            rooms[currentRoom.id][
                exit
            ] = "?"  # add all unexplored rooms to rooms dictionary
            if room.id not in unexplored:
                unexplored.append(room.id)


def update_exits(prev_room, currentRoom, direction):
    # add this room to previous room's exit list
    rooms[prev_room][direction] = currentRoom
    if "?" not in rooms[prev_room].values() and prev_room in unexplored:
        # if we marked the last exit, remove the previous room from the unexplored list
        unexplored.remove(prev_room)

    # add the previous room to this room's exit list
    rooms[currentRoom][opposite_dirs[direction]] = prev_room
    if "?" not in rooms[currentRoom].values() and currentRoom in unexplored:
        # if we've filled in the last exit, remove this room from the unexplored list
        unexplored.remove(currentRoom)


def reverse(path):
    # takes a path and reverses the player
    while len(path):
        backtrack = path.pop(0)
        traversalPath.append(backtrack)
        player.travel(backtrack)


def get_shortest_path(start, target):
    # breadth-first search to find the closest unexplored room
    q = deque()
    q.append([start])
    visited = {}
    while len(q) > 0:
        path = q.popleft()
        room = path[-1]
        if room not in visited:
            visited[room] = path
            if room == target:
                shortest_path = []
                for room in path:
                    current = path.pop(0)  # this should be a queue?
                    for exit in rooms[current]:
                        if rooms[current][exit] == path[0]:
                            shortest_path.append(exit)

                return shortest_path
            for neighbor in rooms[room].values():
                if neighbor is not "?":
                    q.append(path + [neighbor])


prev_room = None
next_move = None
while len(unexplored) > 0:
    currentRoom = player.currentRoom
    if currentRoom not in rooms:
        # if this room has not been mapped, map it
        add_room_exits(currentRoom)
    if prev_room and next_move:
        # if we moved here from a previous room, update that room's map
        update_exits(prev_room.id, currentRoom.id, next_move)
    # get a random move
    next_move = get_random_move(currentRoom)
    if next_move is None:
        # if we have nowhere to move, and the unexplored list is empty, we're done
        if len(unexplored) == 0:
            break
        # otherwise, get the path to the closest unexplored room
        shortest = get_shortest_path(currentRoom.id, unexplored[-1])
        if shortest:
            # if we've found a path, backtrack to that room
            reverse(shortest)
        next_move = get_random_move(player.currentRoom)
        # if we're at a dead end, mark this room as exlored
        if next_move is None:
            if currentRoom.id in unexplored:
                unexplored.remove(currentRoom.id)
        else:
            prev_room = player.currentRoom
            traversalPath.append(next_move)
            player.travel(next_move)

    # if next_move is not None, go to the next room
    else:
        traversalPath.append(next_move)
        prev_room = currentRoom
        player.travel(next_move)


# TRAVERSAL TEST
visited_rooms = set()
player.currentRoom = world.startingRoom
visited_rooms.add(player.currentRoom)
for move in traversalPath:
    player.travel(move)
    visited_rooms.add(player.currentRoom)

if len(visited_rooms) == len(roomGraph):
    print(
        f"TESTS PASSED: {len(traversalPath)} moves, {len(visited_rooms)} rooms visited"
    )
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(roomGraph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.currentRoom.printRoomDescription(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     else:
#         print("I did not understand that command.")
