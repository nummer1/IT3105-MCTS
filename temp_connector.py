import neural_network
import MCTS
import state_manager_hex
from collections import deque


verbose = False
M = 200  # number of rollouts
S = 5  # size of board
games = 10
buffer_size = 1000
start_player = 1  # this should be 1 to work properly
save_interval = 1


s_m = state_manager_hex.state_manager_hex(S, start_player)
actor = neural_network.HexPlayer(S)
replay_buffer = deque(maxlen=buffer_size)

for i in range(games):
    board = s_m.get_start()
    MC = MCTS.MonteCarlo(start_player, s_m)
    while True:
        # TODO: use anet to do rollout (simulation) in MCTS
        # Do M rollouts
        MC.search(M)
        distribution = MC.get_move_distribution()
        replay_buffer.append((board, distribution))
        # Get next state based on rollouts
        board, move = MC.best_move()
        winner = s_m.winner(board)
        # set new root
        MC.purge_tree(board)

        if winner != 0 and verbose:
            print("winner is:", winner)
            break

    # train network
    input = []
    target = []
    for c in replay_buffer:
        case = []
        for c_i in c[0][1]:
            case.extend(c_i)
        input.append(case)
        target.append(c[1])
    actor.train_network(input, target)

    if i % save_interval == 0:
        actor.save_weights(str(i//save_interval))
