class state_manager_nim:
    # the state_keys are numbers
    def __init__(self, start_stones, max_stone_pick, start_player):
        self.start_stones = start_stones  # number of stones at start of game
        self.max_stone_pick = max_stone_pick  # maximum number of stones a player is allowed to pick
        self.start_player = start_player  # starting player (1 or 2)

    def get_start(self):
        # return start state
        return (self.start_player, self.start_stones)

    def get_child_state_keys(self, state_key):
        # must return a list of unique keys for all legal child states
        # returns state and moves made to get to the state
        r = range(1, min(self.max_stone_pick+1, state_key[1]+1))
        keys = [state_key[1]-i for i in r]
        moves = [i for i in r]
        player = 1 if state_key[0] == 2 else 2
        return [(player, key) for key in keys], moves

    def winner(self, state_key):
        # return winner (0 (no winner), 1 or 2)
        if state_key[1] == 0:
            return 1 if state_key[0] == 2 else 2
        return 0
