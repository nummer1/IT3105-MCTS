# NOTE: MCTS is explained in materials on course page

# NOTE: Separate, modular units:
# 1. Tree Search
# 2. Node Expansion
# 3. Leaf Evaluation
# 4. Backpropagation

# NOTE:
# player1: argmax(Q(s, a) + u(s, a))
# player2: argmin(Q(s, a) - u(s, a))

# NOTE:
# rollout -> update Q(s, a)
# leaf expansion
# more rollouts
# choose best action from root
# prune tree of parent (and parent and kids of parent except self) of new root node

import math


M = 0  # Number of simulation per move in actual game
C = math.sqrt(2)  # exploration term


class Node:
    def __init__(self, parent):
        self.parent = parent
        # TODO: maybe map to legal states?
        self.children = []
        self.tot_sims = 0
        self.win_sims = 0

    def selection(self):
        # TODO: if one or more legal kids: stop selection and expand
        if self.children == []:
            # TODO: use state_manager expand random kid
            pass
        else:
            # select kid with highest UCT
            best_kid = None
            best_kid_uct = float("-inf")
            for i, kid in enumerate(children):
                kid_uct = kid.uct()
                if kid_uct > best_kid_uct:
                    best_kid = kid
                    best_kid_uct = kid_uct
            return best_kid.selection()

    def uct(self):
        # return UCT of node
        return (self.win_sims / self.tot_sims) + (C * math.sqrt(math.log(parent.tot_sims) / self.tot_sims))


def MCTS(root):
    pass
