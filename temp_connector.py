import neural_network
import MCTS
import state_manager_hex


verbose = False
M = 1000
S = 5
start_player = 1

replay_buffer = []
s_m = state_manager_hex.state_manager_hex(S, start_player)
MC = MCTS.MonteCarlo(start_player, s_m)
while True:
    # TODO: use anet to do rollout (selection, extension and simulation) in MCTS
    MC.search(M)
    # TODO: add state and move distribution to RBUF
    best_state, move = MC.best_move()
    winner = s_m.winner(best_state)
    if winner != 0:
        print("winner is:", winner)
        break
    # TODO: chose what to purge based on ANN
    MC.purge_tree(best_state)
# TODO: train ANN on random mb from RBUF
# TODO: save ANN weights