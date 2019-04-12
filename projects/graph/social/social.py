import random
from collections import deque


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif (
            friendID in self.friendships[userID] or userID in self.friendships[friendID]
        ):
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # check to be sure that numUsers is greater than avgFriendships
        if avgFriendships > numUsers:
            raise ValueError("The number of users must be greater than avg friendships")

        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(numUsers):
            self.addUser(f"user {i}")

        # Create friendships
        possible_friendships = []
        for user in self.users:
            for friend_id in range(user + 1, len(self.users)):
                possible_friendships.append([user, friend_id])

        random.shuffle(possible_friendships)

        for i in range(numUsers * avgFriendships // 2):
            friendship = possible_friendships[i]
            self.addFriendship(friendship[0], friendship[1])

    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME
        q = deque()
        q.append([userID])
        while len(q) > 0:
            path = q.popleft()
            friend = path[-1]
            if friend not in visited:
                visited[friend] = path
                # add friend's friends to q
                for f in self.friendships[friend]:
                    # if f not in visited?
                    q.append(path + [f]) # unclear if this is okay or if I need to copy the path

        return visited


if __name__ == "__main__":
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print(connections)
