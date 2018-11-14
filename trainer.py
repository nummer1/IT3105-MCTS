import neural_network
import MCTS
import state_manager_hex
from collections import deque


verbose = False
M = 200  # number of rollouts
S = 5  # size of board
games = 1
buffer_size = 1000
start_player = 1  # this should be 1 to work properly
save_interval = 1


s_m = state_manager_hex.state_manager_hex(S, start_player)
actor = neural_network.HexPlayer(s_m)
replay_buffer = deque(maxlen=buffer_size)

for i in range(games):
    board = s_m.get_start()
    MC = MCTS.MonteCarlo(start_player, s_m, actor)
    while True:
        # TODO: use ANN to do rollout (simulation) in MCTS
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
            print("winner is:", winner)
            break

    # train network
    print(len(replay_buffer))
    for line in replay_buffer:
        print(line)
    actor.train_network(replay_buffer)

    if i % save_interval == 0:
        actor.save_weights(str(i/save_interval))

p = actor.get_best_state((1, [(0, 0) for i in range(25)]))
print(p)
