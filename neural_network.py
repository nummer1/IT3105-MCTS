from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np


PATH = "/home/kasparov/Documents/IT3105-MCTS/"


class HexPlayer:
    def __init__(self, state_manager):
        self.state_manager = state_manager
        self.node_number = state_manager.size**2
        self.model = None
        self.bs = 32
        self.create_network()

    def create_network(self):
        self.model = Sequential()
        self.model.add(Dense(50, activation='relu', input_shape=([self.node_number * 2])))
        # self.model.add(Dense(25, activation='relu'))
        # TODO: softmax over only empty legal moves/nodes
        # TODO: softmax can be problematic if two good moves
        self.model.add(Dense(self.node_number, activation='softmax'))
        # try rmsprop
        self.model.compile(optimizer='adam', loss='mean_squared_error')
        self.model.summary()

    def train_network(self, replay_buffer):
        # TODO: take more parameters
        # TODO: Defaults to one epoch, should not train on all samples
        # epochs: how many times to run through all the input
        # batchs_size: how many cases to run through
        input, target = self.replay_to_ann(replay_buffer)
        self.model.fit([input], [target], batch_size=self.bs, validation_split=0.1, shuffle=True)

    def save_weights(self, number):
        filepath = PATH + "weights/" + number
        self.model.save_weights(filepath)

    def load_weights(self, number):
        filepath = PATH + "weights/" + number
        self.model.load_weights(filepath)

    def state_to_ann(self, state):
        # converts a state from state_manager to input for ANN
        case = []
        for cell in state[1]:
            case.extend(cell)
        return case

    def replay_to_ann(self, replay_buffer):
        # converts replay to input and target
        input = []
        target = []
        for replay in replay_buffer:
            input.append(self.state_to_ann(replay[0]))
            target.append(replay[1])
        return input, target

    def prediction(self, state_key):
        # return predicted state and predicted move
        # TODO: change batchsize?
        input = [[self.state_to_ann(state_key)]]
        prediction = self.model.predict(input, batch_size=1)[0]
        legal_state, legal_moves = self.state_manager.get_child_state_keys(state_key)
        for i, cell in enumerate(prediction):
            if i not in legal_moves:
                prediction[i] = 0
        # p_sum = sum(prediction)
        # if p_sum == 0:
        #     print("WARNING: HexPlayer.prediction, p_sum us 0")
        # prediction = [p/p_sum for p in prediction]
        # TODO: fix prediction
        print(prediction)
        move = prediction.index(max(prediction))
        self.state_manager.add_move_to_state(state_key, move)
        return state_key, move
