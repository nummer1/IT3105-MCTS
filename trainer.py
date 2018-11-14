import actors
import MCTS
import state_manager_hex
from collections import deque


verbose = False
# TODO: use time instead of absolute value
M = 200  # number of rollouts
S = 5  # size of board
games = 200
buffer_size = 1000
start_player = 1  # this should be 1 to work properly
save_interval = 10


s_m = state_manager_hex.state_manager_hex(S, start_player)
actor = actors.NeuralNet(s_m)
replay_buffer = deque(maxlen=buffer_size)

for i in range(games):
    board = s_m.get_start()
    MC = MCTS.MonteCarlo(start_player, s_m, actor)
    while True:
        # Do M rollouts
        MC.search(M)
        distribution = MC.get_move_distribution()
        replay_buffer.append((board, distribution))
        # Get next state based on rollouts
        board, move = MC.best_move()
        winner = s_m.winner(board)
        # set new root
        MC.purge_tree(board)

        if winner != 0:
            break

    # train network
    actor.train_network(replay_buffer)

    if i % save_interval == 0:
        actor.save_weights(str(i//save_interval))
