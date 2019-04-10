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
world.printRooms()

player = Player("Name", world.startingRoom)

# FILL THIS IN
traversalPath = []
rooms = {}
unexplored = deque()
unexplored.append(player.currentRoom.id)
opposite_dirs = {"n": "s", "s": "n", "e": "w", "w": "e"}


def get_random_move(room):
    exits = room.getExits()
    possible_moves = []
    for exit in exits:
        if rooms[room.id][exit] == "?":
            possible_moves.append(exit)
    if len(possible_moves) == 0:
        return None
    random_idx = random.randrange(len(possible_moves))
    print(f"possible: {possible_moves}")
    return possible_moves[random_idx]


def add_room_exits(room):
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
    # print(f"updated: {rooms}")


def update_exits(prev_room, currentRoom, direction):
    print(f"update exits\n--------\nprevious room: {prev_room}")
    print(f"current room: {currentRoom}")
    print(f"direction: {direction}")
    # direction is how we got to the current room from the prev room
    rooms[prev_room][direction] = currentRoom
    if "?" not in rooms[prev_room].values() and prev_room in unexplored:
        unexplored.remove(prev_room)
    rooms[currentRoom][opposite_dirs[direction]] = prev_room
    # print("here:", rooms[currentRoom][opposite_dirs[next_move]])
    print(rooms[currentRoom])
    if "?" not in rooms[currentRoom].values() and currentRoom in unexplored:
        unexplored.remove(currentRoom)


def reverse(path):
    print("unexplored:", unexplored)
    while len(path):
        backtrack = path.pop(0)
        print("reversing", backtrack)
        traversalPath.append(backtrack)
        player.travel(backtrack)


def get_shortest_path(start, target):
    q = deque()
    q.append([start])
    visited = {}
    # print(q)
    while len(q) > 0:
        path = q.popleft()
        room = path[-1]
        # print(f"path is {path}")
        if room not in visited:
            visited[room] = path
            # print(f"visited: {visited}")
            if room == target:
                # print(f"found target. shortest path: {path}")
                shortest_path = []
                for room in path:
                    current = path.pop(0)  # this should be a queue?
                    for exit in rooms[current]:
                        if rooms[current][exit] == path[0]:
                            shortest_path.append(exit)

                # print(f"shortest: {shortest_path}")
                return shortest_path
            # print("rooms:", rooms[room].values())
            for neighbor in rooms[room].values():
                if neighbor is not "?":
                    q.append(path + [neighbor])


prev_room = None
next_move = None
while len(unexplored) > 0:
    currentRoom = player.currentRoom
    print("current room:", currentRoom.id)
    if currentRoom not in rooms:
        add_room_exits(currentRoom)
    if prev_room and next_move:
        update_exits(prev_room.id, currentRoom.id, next_move)
    next_move = get_random_move(currentRoom)
    # print(f"move: {next_move}")  # print the possible exits
    if next_move is None:
        # print("bumped into a wall. now what?")
        # print(f"unexplored is {unexplored}")
        # print(f" path is {path}")
        if len(unexplored) == 0:
            break
        shortest = get_shortest_path(
            currentRoom.id, unexplored[-1]
        )  # this should pop off the unexplored list instead of 0
        # print(f"path back: {shortest}")
        if shortest:
            reverse(shortest)
        next_move = get_random_move(player.currentRoom)
        if next_move is None:
            if currentRoom.id in unexplored:
                unexplored.remove(currentRoom.id)
        else:
            prev_room = player.currentRoom
            traversalPath.append(next_move)
            player.travel(next_move)

    else:
        traversalPath.append(next_move)
        # path.append(next_move)
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
