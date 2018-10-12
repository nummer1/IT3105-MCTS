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

M = 0  # Number of simulation per move in actual game


class Node:
    def __init__(self, parent):
        self.parent = parent
        self.children = []


def MCTS(root):
    pass
