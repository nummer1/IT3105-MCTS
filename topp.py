import actors
import state_manager_hex


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
        # s_m.print_board(state)
        winner = s_m.winner(state)
        if winner != 0:
            print("winner is:", winner)
            break
        # important: player_turn is switched after winner is checked
        player_turn = 1 if player_turn == 2 else 2
    return winner


ann = actors.NeuralNet(s_m)
ann.load_weights("16")
random = actors.Random(s_m)
winner_1 = 0
winner_2 = 0
for i in range(100):
    w = play_game(random, ann)
    if w == 1:
        winner_1 += 1
    elif w == 2:
        winner_2 += 1
    else:
        print("What?")
print(winner_1, winner_2)
