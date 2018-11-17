import state_manager_hex
import actors
import trainer
import topp
from collections import deque
import pickle


# SAVE PARAMETERS
network_name = "delete_"  # will match nest with 'name' + number against each other

# TRAINING PARAMETERS
TRAIN_NETS = True
net_size = [50]
activation_function = ['sigmoid', 'tanh', 'relu'][2]
optimizer = ['adagrad', 'sgd', 'rmsprop', 'adam'][1]
batch_size = 128  # batch size during training
epsilon = 0.0  # probability of doing random move
episodes = 200  # number episodes to generate
# Imprtant: keras will delete older snapshots if snap_number is higher than 5
snap_number = 5  # number of snapshots, must be 2 or larger
buffer_size = 2000  # size of replay buffer
snapshots = [i for i in range(0, episodes+1, episodes//(snap_number-1))]

train_on_random = False
sim_time_in_random = 1
random_episodes = 200

# MCTS PARAMETERS
rollouts_per_move = 200  # number of rollouts
sim_time = 5  # time to do rollout per move. if not 0, use instead of rollouts_per_move

# GAME PARAMETERS
verbose = False
board_size = 5
start_player = 1  # this should be 1 to work properly

# TOPP PARAMETERS
games_in_series = 100

s_m = state_manager_hex.state_manager_hex(board_size, start_player)
# TRAINING
if TRAIN_NETS:
    random_actor = actors.Random(s_m)
    ann = actors.NeuralNet(s_m, epsilon=epsilon)
    ann.create_dense_network(net_size, activation_function, optimizer)
    replay_buffer = deque(maxlen=buffer_size)
    generator = trainer.Trainer(start_player, s_m, ann, replay_buffer, verbose, network_name)
    if train_on_random:
        generator.generate_games(random_episodes, [], batch_size, sim_time=sim_time_in_random,
                generate_random=True)
    generator.generate_games(episodes, snapshots, batch_size, sim_time=sim_time,
                rollouts_per_move=rollouts_per_move)
    with open("replay_buffer.dat", "wb") as output:
        pickle.dump(generator.replay_buffer, output)

# TOPP
actors_list = []
actors_name = []
for i in snapshots:
    ann = actors.NeuralNet(s_m)
    ann.load(network_name + str(i))
    actors_list.append(ann)
    actors_name.append(network_name + str(i))
actors_list.append(actors.Random(s_m))
actors_name.append("random")
tournament = topp.Topp(s_m, games_in_series, verbose)
tournament.round_robin(actors_list, actors_name)
