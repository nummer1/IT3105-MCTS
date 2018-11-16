import state_manager_hex
import actors
import trainer
import topp
from collections import deque
import threading


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
# TODO: integrate rollouts again
rollouts_per_move = 200  # number of rollouts
sim_time = 5  # time to do rollout per move. if not 0, use instead of rollouts_per_move

# GAME PARAMETERS
verbose = False
board_size = 5
start_player = 1  # this should be 1 to work properly

# TOPP PARAMETERS
games_in_series = 2


s_m = state_manager_hex.state_manager_hex(board_size, start_player)
lock = threading.Lock()
end_event = threading.Event()


print("Net will be cahced after the following episodes:", snapshots)
s_m = state_manager_hex.state_manager_hex(board_size, start_player)
if replay_buffer is None:
    replay_buffer = deque(maxlen=buffer_size)
actor.save("0")


random_actor = actors.Random(s_m)
ann = actors.NeuralNet(s_m, epsilon=epsilon)
ann.create_dense_network(net_size, activation_function, optimizer)
replay_buffer = deque(maxlen=buffer_size)
generator = trainer.GameGenerator(start_player, s_m, ann, replay_buffer, lock, end_event, sim_time)
generator.run()


# TOPP
ann_1 = actors.NeuralNet(s_m)
ann_1.load("first_test")
ann_0 = actors.NeuralNet(s_m)
ann_0.load("10")
ann_new = actors.NeuralNet(s_m)
ann_new.load("200")
ann_new_epsilon = actors.NeuralNet(s_m, 0.1)
ann_new_epsilon.load("200")
random_1 = actors.Random(s_m)
# actors_name = ["old_ann", "ann_0", "ann_new", "ann_eps", "random"]
# actors_list = [ann_1, ann_0, ann_new, ann_new_epsilon, random_1]
actors_name = ["old", "new"]
actors_list = [ann_1, ann_new]
tournament = topp.Topp(s_m, games_in_series, verbose)
tournament.round_robin(actors_list, actors_name)
