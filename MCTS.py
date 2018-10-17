import math
import random
import state_manager_nim


debug = True
M = 1000  # Number of simulation per move in actual game
C = math.sqrt(2)  # exploration term
start_player = 1  # starting player

state_manager = state_manager_nim.state_manager_nim(10, 3, start_player)


class Node:
    def __init__(self, parent, state_key, player_turn):
        self.parent = parent
        # map of state_keys to child_nodes
        self.children = {}
        self.state_key = state_key
        self.player_turn = player_turn
        self.tot_sims = 0
        self.win_sims = 0

    def uct(self):
        # return UCT of node
        return (self.win_sims / self.tot_sims) + (C * math.sqrt(math.log(self.parent.tot_sims) / self.tot_sims))

    def select_and_expand(self):
        # returns the expanded node
        legal_states = state_manager.get_child_state_keys(self.state_key)
        if len(legal_states) == 0:
            if debug:
                print("reached leaf node in selection fase in Node.select_and_expand()")
            return self
        opt_keys = [s for s in legal_states if s not in self.children.keys()]
        if opt_keys != []:
            # expand node with new kid
            random_kid_state = random.choice(opt_keys)
            next_player = 1 if self.player_turn == 2 else 2
            node = Node(self, random_kid_state, next_player)
            self.children[random_kid_state] = node
            if debug:
                print("node expanded:", node.state_key)
            return node
        else:
            # select kid with highest UCT
            best_kid = None
            best_kid_uct = float("-inf")
            for kid in self.children.values():
                kid_uct = kid.uct()
                if kid_uct > best_kid_uct:
                    best_kid = kid
                    best_kid_uct = kid_uct
            if best_kid is None:
                print("Error in Node.select_and_expand(); best_kid is None")
            if debug:
                print("node selected:", best_kid.state_key)
            return best_kid.select_and_expand()

    def simulate(self):
        # simulates a game played from self
        current_state_key = self.state_key
        while True:
            winner = state_manager.winner(current_state_key)
            if winner != 0:
                if debug:
                    print("found winner in simulation:", current_state_key, winner)
                return winner
            current_state_key = random.choice(state_manager.get_child_state_keys(current_state_key))
            if debug:
                print("random simulation:", current_state_key)

    def backpropagate(self, winner):
        # update all stats and parent stats based on winner
        # winner whould be 1 or 2
        self.tot_sims += 1
        if winner != self.player_turn:
            # increment wins if current player is losing, because stats is used by parents
            self.win_sims += 1
        if self.parent is not None:
            self.parent.backpropagate(winner)


class MonteCarlo:
    def __init__(self):
        self.root = Node(None, state_manager.get_start(), start_player)

    def play(self):
        for i in range(M):
            expanded_node = self.root.select_and_expand()
            winner = expanded_node.simulate()
            expanded_node.backpropagate(winner)

    def best_move(self):
        best_kid = None
        visited = 0
        for key in self.root.children:
            if self.root.children[key].tot_sims > visited:
                visited = self.root.children[key].tot_sims
                best_kid = self.root.children[key]
        return best_kid.state_key
