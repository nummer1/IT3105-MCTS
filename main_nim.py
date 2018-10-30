import state_manager_nim
import MCTS
import random


verbose = False
G = 50  # Number of episodes to batch run
P = 1  # Starting player, if 0: random
M = 1000  # Number of simulations per move in actual game
N = 10  # Number of starting stones
K = 3  # Max number of stones a player can pick


win_game_count_p1 = 0
game_count = 0

for g in range(G):
    if P == 0:
        start_player = random.randint(1, 2)
    else:
        start_player = P

    s_m = state_manager_nim.state_manager_nim(N, K, start_player)
    MC = MCTS.MonteCarlo(start_player, s_m)
    while True:
        MC.search(M)
        best_state, move = MC.best_move()
        if verbose:
            # player that made move, is the player whose turn it's not
            print("Player ", 1 if best_state[0] == 2 else 2, " made move: ", move,
                            " :: Current state: ", best_state[1], sep='')
        winner = s_m.winner(best_state)
        if winner != 0:
            game_count += 1
            print(game_count, "of", G, "games done")
            if winner == 1:
                win_game_count_p1 += 1
            if verbose:
                print("Player", winner, "wins!")
            break
        MC.purge_tree(best_state)

p1_win_perc = round(win_game_count_p1/G*100, 1)
print("player 1 won ", p1_win_perc, "% of games", sep='')
print("player 2 won ", 100-p1_win_perc, "% of games", sep='')
