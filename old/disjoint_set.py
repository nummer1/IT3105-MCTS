import copy


class SetNode:
    def __init__(self):
        self.parent = self
        self.rank = 0


class DisjointSet:
    def __init__(self):
        self.set = []

    def make_set(self, x):
        x = SetNode()
        self.set.append(x)

    def find(self, x):
        if x.parent != x:
            x.parent = self.find(x.parent)
        return x.parent

    def union(self, x, y):
        x_root = self.find(x)
        y_root = self.find(y)
        if x_root == y_root:
            return
        if x_root.rank < y_root.rank:
            x_root, y_root = y_root, x_root
        y_root.parent = x_root
        if x_root.rank == y_root.rank:
            x_root.rank += 1




class state_manager_hex:
    # the state_keys are numbers
    def __init__(self, size, start_player):
        self.size = size
        self.start_player = start_player

    def get_start(self):
        # return start state
        return (self.start_player, DisjointSet())

    def get_child_state_keys(self, state_key):
        # must return a list of unique keys for all legal child states
        # returns state and moves made to get to the state
        legal_states = []
        legal_moves = []
        player = state_key[0]
        board = state_key[1]
        return legal_states, legal_moves

    def winner(self, state_key):
        # return winner (0 (no winner), 1 or 2)
        prev_player = 1 if state_key[0] == 2 else 2
        board = state_key[1]

        return prev_player # or 0
