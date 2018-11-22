import state_manager_hex
import actors
import trainer
import topp
from collections import deque
# import pickle
import os
import re


# SAVE PARAMETERS
network_name = "test_"  # will match nest with 'name' + number against each other

# TRAINING PARAMETERS
TRAIN_NETS = True
net_size = [50]
activation_function = ['sigmoid', 'tanh', 'relu'][2]
optimizer = ['sgd', 'rmsprop', 'adagrad', 'adam'][3]
batch_size = 128  # batch size during training
epsilon = 0.05  # probability of doing random move
use_default_lr = True  # use keras default learning rate for optimizer
learning_rate = 0.01  # use this learning rate if use_default_leraning_rate is False
episodes = 2  # number episodes to generate
# Imprtant: if snap_number must divide episodes in equal sequences
snap_number = 2  # number of snapshots, must be 2 or larger
buffer_size = 100  # size of replay buffer
snapshots = [i for i in range(0, episodes+1, episodes//(snap_number-1))]

# Don't use
train_on_random = False
sim_time_in_random = 1
random_episodes = 200

# MCTS PARAMETERS
rollouts_per_move = 200  # number of rollouts
sim_time = 0.1  # time to do rollout per move. if not 0, use instead of rollouts_per_move

# GAME PARAMETERS
verbose = False
board_size = 5
start_player = 1  # this should be 1 to work properly

# TOPP PARAMETERS
topp_names = []  # extra networks to compete in topp
games_in_series = 100

s_m = state_manager_hex.state_manager_hex(board_size, start_player)
# TRAINING
if TRAIN_NETS:
    random_actor = actors.Random(s_m)
    ann = actors.NeuralNet(s_m, epsilon=epsilon)
    ann.create_dense_network(net_size, activation_function, optimizer, learning_rate, use_default_lr)
    replay_buffer = deque(maxlen=buffer_size)
    generator = trainer.Trainer(start_player, s_m, ann, replay_buffer, verbose, network_name)
    if train_on_random:
        generator.generate_games(random_episodes, [], batch_size, sim_time=sim_time_in_random,
                generate_random=True)
    generator.generate_games(episodes, snapshots, batch_size, sim_time=sim_time,
                rollouts_per_move=rollouts_per_move)
    # with open("replay_buffer.dat", "wb") as output:
    #     pickle.dump(generator.replay_buffer, output)

# TOPP
actors_list = []
actors_name = []
# for i in snapshots:
for file_name in os.listdir('weights'):
    file_name = file_name[:-3]
    if re.match(network_name, file_name) or file_name in topp_names:
        ann = actors.NeuralNet(s_m)
        ann.load(file_name)
        actors_list.append(ann)
        actors_name.append(file_name)
actors_list.append(actors.Random(s_m))
actors_name.append("random")
tournament = topp.Topp(s_m, games_in_series, verbose)
tournament.round_robin(actors_list, actors_name)
