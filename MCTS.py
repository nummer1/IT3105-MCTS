import math
import random


debug = False


C = math.sqrt(2)  # exploration term


class MonteCarlo:
    def __init__(self, start_player, state_manager):
        self.state_manager = state_manager
        self.root = Node(None, state_manager.get_start(), None, start_player, state_manager)

    def search(self, simulations):
        # simulations is number of games to simulate
        for i in range(simulations):
            expanded_node = self.root.select_and_expand()
            winner = expanded_node.simulate()
            expanded_node.backpropagate(winner)

    def best_move(self):
        best_kid = None
        visited = 0
        if not self.root.child_nodes:
            print("Error in best_move, root node is end state")
        for kid in self.root.child_nodes:
            if kid.tot_sims > visited:
                visited = kid.tot_sims
                best_kid = kid
        return best_kid.state_key, best_kid.move_to_state

    def purge_tree(self, state_key):
        # set kid with state_key to new root, and purge all nodes not it's children
        old_root = self.root
        self.root = self.root.child_nodes[self.root.child_states.index(state_key)]
        for kid in old_root.child_nodes:
            if kid.state_key != self.root.state_key:
                kid.purge()
        if debug:
            print("old_root:", old_root.state_key)
            print("new root:", self.root.state_key)
        del old_root


class Node:
    def __init__(self, parent, state_key, move_to_state, player_turn, state_manager):
        self.state_manager = state_manager
        self.parent = parent
        # list of child nodes
        self.child_nodes = []
        # list of child node states
        self.child_states = []
        self.state_key = state_key
        self.move_to_state = move_to_state
        self.player_turn = player_turn
        self.tot_sims = 0
        self.win_sims = 0
        self.is_winning = state_manager.winner(state_key)  # 1 if win for 1, 2 if win for 2

    def uct(self):
        # return UCT of node
        return (self.win_sims / self.tot_sims) + (C * math.sqrt(math.log(self.parent.tot_sims) / self.tot_sims))

    def select_and_expand(self):
        # if this node is a win for either player, don't simulate
        if self.is_winning != 0:
            return self
        # returns the expanded node
        legal_states, legal_moves = self.state_manager.get_child_state_keys(self.state_key)
        if len(legal_states) == 0:
            if debug:
                print("Reached leaf node in selection fase in Node.select_and_expand()")
            return self
        opt_keys = [s for s in legal_states if s not in self.child_states]
        if opt_keys:
            # expand node with new kid
            random_kid_state = random.choice(opt_keys)
            move = legal_moves[legal_states.index(random_kid_state)]
            next_player = 1 if self.player_turn == 2 else 2
            node = Node(self, random_kid_state, move, next_player, self.state_manager)
            self.child_nodes.append(node)
            self.child_states.append(random_kid_state)
            if debug:
                print("node expanded:", node.state_key)
            return node
        else:
            # select kid with highest UCT
            best_kid = None
            best_kid_uct = float("-inf")
            for kid in self.child_nodes:
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
            winner = self.state_manager.winner(current_state_key)
            if winner != 0:
                if debug:
                    print("found winner in simulation:", current_state_key, winner)
                return winner
            current_state_key = random.choice(self.state_manager.get_child_state_keys(current_state_key)[0])
            if debug:
                print("random simulation:", current_state_key)

    def backpropagate(self, winner):
        # update all stats and parent stats based on winner
        # winner would be 1 or 2
        self.tot_sims += 1
        if winner != self.player_turn:
            # increment wins if current player is losing, because stats is used by parents
            self.win_sims += 1
        if self.parent is not None:
            self.parent.backpropagate(winner)

    def purge(self):
        # purge self and all children
        if self.child_nodes:
            for kid in self.child_nodes:
                kid.purge()
        del self
