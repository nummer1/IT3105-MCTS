import itertools


class Topp():
    def __init__(self, state_manager, games_in_series, verbose):
        self.state_manager = state_manager
        self.games_in_series = games_in_series
        self.verbose = verbose

    def play_game(self, actor1, actor2):
        state = self.state_manager.get_start()
        player_turn = 1
        while True:
            if player_turn == 1:
                state, move = actor1.get_state(state, True)
            else:
                state, move = actor2.get_state(state, True)
            if self.verbose:
                self.state_manager.print_move(move)
                self.state_manager.print_board(state)
                print()
            winner = self.state_manager.winner(state)
            if winner != 0:
                if self.verbose:
                    print("winner is:", winner)
                break
            # important: player_turn is switched after winner is checked
            player_turn = 1 if player_turn == 2 else 2
        return winner

    def round_robin(self, actors_list, actors_name):
        print("name_1, name_2: win_1, win_2")
        matches = itertools.combinations(actors_list, 2)
        for match in matches:
            winner_1 = 0
            first_player = 1
            for i in range(self.games_in_series):
                if first_player == 1:
                    w = self.play_game(match[0], match[1])
                    if w == 1:
                        winner_1 += 1
                    first_player = 2
                else:
                    w = self.play_game(match[1], match[0])
                    if w == 2:
                        winner_1 += 1
                    first_player = 1
                if w == 0:
                    print("ERROR: round_robin: winner is 0")
            print(actors_name[actors_list.index(match[0])], ",", actors_name[actors_list.index(match[1])],
                        ":", winner_1, self.games_in_series - winner_1)
