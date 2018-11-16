import MCTS


class Trainer:
    # generate games
    def __init__(self, start_player, state_manager, actor, replay_buffer, sim_time, rollouts_per_move, episodes, snapshots, verbose):
        self.start_player = start_player
        self.state_manager = state_manager
        self.actor = actor
        self.replay_buffer = replay_buffer
        self.sim_time = sim_time
        self.rollouts_per_move = rollouts_per_move
        self.episodes = episodes
        self.snapshots = snapshots
        self.verbose = verbose

    def generate_games(self, batch_size):
        # geenrate a game and add to replay_buffer
        print("Net will be cahced after the following episodes:", self.snapshots)
        self.actor.save("0")
        for i in range(1, self.episodes + 1):
            board = self.state_manager.get_start()
            MC = MCTS.MonteCarlo(self.start_player, self.state_manager, self.actor)
            while True:
                # Do M rollouts
                MC.search(sim_time=self.sim_time, simulations=self.rollouts_per_move)
                distribution = MC.get_move_distribution()
                self.replay_buffer.append((board, distribution))
                # Get next state based on rollouts
                board, move = MC.best_move()
                winner = self.state_manager.winner(board)
                if self.verbose:
                    self.state_manager.print_move(move)
                    self.state_manager.print_board(board)
                # set new root
                MC.purge_tree(board)

                if winner != 0:
                    break
            # lock before accessing shared actor
            self.actor.train_network(self.replay_buffer, batch_size=batch_size)

            if i in self.snapshots:
                self.actor.save(str(i))
