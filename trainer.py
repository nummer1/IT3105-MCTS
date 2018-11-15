import actors
import MCTS
import state_manager_hex
from collections import deque


# TODO: show graphic games during training and TOPP

# ANET TRAINING PARAMETERS
net_size = [50]
activation_function = ['sigmoid', 'tanh', 'relu'][2]
optimizer = ['adagrad', 'sgd', 'rmsprop', 'adam'][3]
batch_size = 128  # batch size during training
epsilon = 0.05  # probability of doing random move
episodes = 200  # number episodes to generate
# Imprtant: keras will delete older snapshots if snap_number is higher than 5
snap_number = 20  # number of snapshots, must be 2 or larger
buffer_size = 1000  # size of replay buffer
snapshots = [i for i in range(0, episodes+1, episodes//(snap_number-1))]

# MCTS PARAMETERS
rollouts_per_move = 200  # number of rollouts
sim_time = 5  # time to do rollout per move. if not 0, use instead of rollouts_per_move

# GAME PARAMETERS
board_size = 5
start_player = 1  # this should be 1 to work properly


def fill_replay_buffer(actor, replay_buffer):
    # fill replay_buffer with games from random rollouts
    while len(replay_buffer) < buffer_size:
        board = s_m.get_start()
        MC = MCTS.MonteCarlo(start_player, s_m, actor)
        while True:
            # Do M rollouts
            MC.search(sim_time=0.5)
            distribution = MC.get_move_distribution()
            replay_buffer.append((board, distribution))
            # Get next state based on rollouts
            board, move = MC.best_move()
            winner = s_m.winner(board)
            # set new root
            MC.purge_tree(board)

            if winner != 0:
                break
        print("progress:", len(replay_buffer))


def train_neural_networks(actor, replay_buffer=None):
    print("Net will be cahced after the following episodes:", snapshots)
    s_m = state_manager_hex.state_manager_hex(board_size, start_player)
    if replay_buffer is None:
        replay_buffer = deque(maxlen=buffer_size)
    actor.save("0")

    for i in range(1, episodes+1):
        board = s_m.get_start()
        MC = MCTS.MonteCarlo(start_player, s_m, actor)
        while True:
            # Do M rollouts
            MC.search(sim_time=sim_time)
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

        if i in snapshots:
            actor.save(str(i))


s_m = state_manager_hex.state_manager_hex(board_size, start_player)
random_actor = actors.Random(s_m)
ann = actors.NeuralNet(s_m, epsilon=epsilon)
ann.create_dense_network(net_size, activation_function, optimizer)
replay_buffer = deque(maxlen=buffer_size)
fill_replay_buffer(random_actor, replay_buffer)
ann.train_network(replay_buffer, epochs=50)
train_neural_networks(ann, replay_buffer=replay_buffer)
