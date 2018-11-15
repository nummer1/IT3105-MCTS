import random
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model


PATH = "/home/kasparov/Documents/IT3105-MCTS/"


class Random:
    def __init__(self, state_manager):
        self.state_manager = state_manager

    def get_state(self, state_key, best_move):
        move = random.choice(self.state_manager.get_legal_moves(state_key))
        state = self.state_manager.apply_move_to_state(state_key, move)
        return state, move


class NeuralNet:
    def __init__(self, state_manager, epsilon=0):
        self.state_manager = state_manager
        # chose random action with epsilon probability
        self.epsilon = epsilon
        self.model = None

    def create_dense_network(self, size, afunc, optimizer):
        node_number = self.state_manager.size**2
        self.model = Sequential()
        for i, s in enumerate(size):
            if i == 0:
                self.model.add(Dense(s, activation=afunc, input_shape=([node_number * 2])))
            else:
                self.model.add(Dense(s, activation=afunc))
        # TODO: softmax can be problematic if two good moves
        self.model.add(Dense(node_number, activation='softmax'))
        self.model.compile(optimizer=optimizer, loss='mean_squared_error')
        self.model.summary()

    def train_network(self, replay_buffer, batch_size=128, epochs=1):
        # TODO: take more parameters
        # TODO: Defaults to one epoch, should not train on all samples
        # epochs: how many times to run through all the input
        # batchs_size: how many cases to run through
        input, target = self.replay_to_ann(replay_buffer)
        self.model.fit([input], [target], batch_size=batch_size, epochs=epochs, validation_split=0.0, shuffle=True)

    def save(self, name):
        filepath = PATH + "weights/" + name + ".h5"
        self.model.save(filepath)

    def load(self, name):
        filepath = PATH + "weights/" + name + ".h5"
        self.model = load_model(filepath)

    def state_to_ann(self, state):
        # TODO: move to state_manager_hex
        # converts a state from state_manager to input for ANN
        case = []
        for cell in state[1]:
            case.extend(cell)
        return case

    def replay_to_ann(self, replay_buffer):
        # TODO: move to state_manager_hex
        # converts replay to input and target
        input = []
        target = []
        for replay in replay_buffer:
            input.append(self.state_to_ann(replay[0]))
            target.append(replay[1])
        return input, target

    def get_state(self, state_key, best_move):
        # TODO: assignment says take best move, or random move with epsilon probabiltity
        # returns state and move
        # if best_move is True, return move with highest probability, else return based on probability
        input = [[self.state_to_ann(state_key)]]
        # prediction is a numpy array
        prediction = self.model.predict(input, batch_size=1)[0]
        legal_moves = self.state_manager.get_legal_moves(state_key)
        for i, cell in enumerate(prediction):
            if i not in legal_moves:
                prediction[i] = 0

        p_sum = sum(prediction)
        if p_sum == 0:
            print("Zero in neural_network")

        # TODO: Random in beginning
        # state_key[1].count((0, 0)) > self.state_manager.size - 2
        if self.epsilon > random.uniform(0, 1):
            move = random.choice(self.state_manager.get_legal_moves(state_key))
        else:
            if best_move:
                # argmax returns index of max argument
                move = prediction.argmax()
            else:
                # chose move and state based on probabilities
                prediction = [p/p_sum for p in prediction]
                move = random.choices([i for i in range(self.state_manager.get_move_size())],
                            weights=prediction, k=1)[0]
        state = self.state_manager.apply_move_to_state(state_key, move)
        return state, move
