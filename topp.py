import itertools
import actors
import state_manager_hex


verbose = True
games_in_series = 2
size = 5
start_player = 1
s_m = state_manager_hex.state_manager_hex(size, start_player)


def play_game(actor1, actor2):
    state = s_m.get_start()
    player_turn = 1
    while True:
        if player_turn == 1:
            state = actor1.get_state(state, True)[0]
        else:
            state = actor2.get_state(state, True)[0]
        if verbose:
            s_m.print_board(state)
            print()
        winner = s_m.winner(state)
        if winner != 0:
            if verbose:
                print("winner is:", winner)
            break
        # important: player_turn is switched after winner is checked
        player_turn = 1 if player_turn == 2 else 2
    return winner


def round_robin(actors_list, actors_name):
    matches = itertools.combinations(actors_list, 2)
    for match in matches:
        winner_1 = 0
        first_player = 1
        for i in range(games_in_series):
            if first_player == 1:
                w = play_game(match[0], match[1])
                if w == 1:
                    winner_1 += 1
                first_player = 2
            else:
                w = play_game(match[1], match[0])
                if w == 2:
                    winner_1 += 1
                first_player = 1
            if w == 0:
                print("ERROR: round_robin: winner is 0")
        print(actors_name[actors_list.index(match[0])], ",", actors_name[actors_list.index(match[1])],
                    ":", winner_1, games_in_series - winner_1)


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
round_robin(actors_list, actors_name)
