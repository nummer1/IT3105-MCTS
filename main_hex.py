import state_manager_hex
import actors
import trainer
import topp
from collections import deque


# TRAINING PARAMETERS
TRAIN_NETS = True
net_size = [50]
activation_function = ['sigmoid', 'tanh', 'relu'][2]
optimizer = ['adagrad', 'sgd', 'rmsprop', 'adam'][3]
batch_size = 128  # batch size during training
epsilon = 0.2  # probability of doing random move
episodes = 10  # number episodes to generate
# Imprtant: keras will delete older snapshots if snap_number is higher than 5
snap_number = 2  # number of snapshots, must be 2 or larger
buffer_size = 1000  # size of replay buffer
snapshots = [i for i in range(0, episodes+1, episodes//(snap_number-1))]

# MCTS PARAMETERS
rollouts_per_move = 200  # number of rollouts
sim_time = 0.1  # time to do rollout per move. if not 0, use instead of rollouts_per_move

# GAME PARAMETERS
verbose = False
board_size = 5
start_player = 1  # this should be 1 to work properly

# TOPP PARAMETERS
games_in_series = 10

s_m = state_manager_hex.state_manager_hex(board_size, start_player)
# TRAINING
if TRAIN_NETS:
    random_actor = actors.Random(s_m)
    ann = actors.NeuralNet(s_m, epsilon=epsilon)
    ann.create_dense_network(net_size, activation_function, optimizer)
    replay_buffer = deque(maxlen=buffer_size)
    generator = trainer.Trainer(start_player, s_m, ann, replay_buffer, sim_time, rollouts_per_move, episodes, snapshots, verbose)
    generator.generate_games(batch_size)

# TOPP
actors_list = []
actors_name = []
for i in snapshots:
    ann = actors.NeuralNet(s_m)
    ann.load(str(i))
    actors_list.append(ann)
    actors_name.append(str(i))
actors_list.append(actors.Random(s_m))
actors_name.append("random")
tournament = topp.Topp(s_m, games_in_series, verbose)
tournament.round_robin(actors_list, actors_name)
