import itertools
import actors
import state_manager_hex


verbose = False
games_in_series = 1000
size = 5
start_player = 1
s_m = state_manager_hex.state_manager_hex(size, start_player)


def play_game(actor1, actor2):
    state = s_m.get_start()
    player_turn = 1
    while True:
        if player_turn == 1:
            state = actor1.get_state(state)[0]
        else:
            state = actor2.get_state(state)[0]
        if verbose:
            s_m.print_board(state)
        winner = s_m.winner(state)
        if winner != 0:
            if verbose:
                print("winner is:", winner)
            break
        # important: player_turn is switched after winner is checked
        player_turn = 1 if player_turn == 2 else 2
    return winner


def round_robin(actors):
    matches = itertools.combinations(actors, 2)
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
        print(winner_1, games_in_series - winner_1)


ann = actors.NeuralNet(s_m)
ann.model.load_weights("/home/kasparov/Documents/IT3105-MCTS/weights/first_test")
random1 = actors.Random(s_m)
random2 = actors.Random(s_m)
round_robin([ann, random1, random2])
