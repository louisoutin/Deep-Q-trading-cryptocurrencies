from keras.models import Sequential  # One layer after the other
from keras.layers import Dense, Dropout, Flatten  # Dense layers are fully connected layers,
# Flatten layers flatten out multidimensional inputs
from collections import deque  # For storing moves
from Action import *

import numpy as np
import random  # For sampling batches from the observations

from keras.optimizers import Adam


# Code inspired from https://keon.io/deep-q-learning/


class DQNetwork:
    """
        Deep Q network, represent the model of our DQN
    """

    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.85  # discount rate
        self.epsilon = 0.7  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.002
        self.model = self._build_model()
        self.targetModel = self._build_model()
        self.batch_size = 300

    def _build_model(self):
        """
            Build the different layers of the neural network for Deep Q Learning
        """
        model = Sequential()
        model.add(Dense(units=100, input_shape=(self.state_size,), activation="relu"))
        model.add(Dropout(0.25))
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.0001))
        return model

    def build_online_model(self):
        """
            Build the different layers of the neural network for Deep Q Learning
        """
        model = Sequential()
        model.add(Dense(units=100, input_shape=(self.state_size,), activation="relu"))
        model.add(Dropout(0.25)) # ou ligne suivante?
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss="mse", optimizer=Adam(lr=0.0005))
        return model

    def remember(self, state, rewards, next_state, done):
        self.memory.append((state, rewards, next_state, done))

    def act(self, state):
        act_values = self.targetModel.predict(np.asarray([state]))
        # if np.argmax(act_values[0]) == 2:
        #     print("SELL")
        #     return Action.SELL
        # else:
        return act_values[0]
        # returns action (-1 so as to be between -1 and 1)

    def updateTargetModel(self):
        self.targetModel.set_weights(self.model.get_weights())

    def replayInitial(self):
        batch_size = self.batch_size
        minibatch = random.sample(self.memory, batch_size)

        for state, rewards, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                         np.amax(self.model.predict(np.asarray([next_state]))[0])
            target_f = self.model.predict(np.asarray([state]))
            target_f[0][action.value] = target
            #print(np.asarray([state]), target_f)
            self.model.fit(np.asarray([state]), target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def replay(self):
        batch_size = self.batch_size
        minibatch = random.sample(self.memory, batch_size)

        for state, rewards, next_state, isDone in minibatch:
            target = self.model.predict(np.asarray([state]))
            if isDone:
                target[0] = rewards
            else:
                a = self.model.predict(np.asarray([next_state]))[0]
                t = self.targetModel.predict(np.asarray([next_state]))[0]

                # Bellman Equation
                target[0] = rewards + self.gamma * t[np.argmax(a)]

                self.model.fit(np.asarray([state]), target, epochs=1, verbose=0)

        # update the epsilon to gradually reduce the random exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def onlineLearning(self):
        minibatch = self.memory

        for state, rewards, next_state, done in minibatch:
            target = rewards
            if not done:
                target = rewards + self.gamma * \
                                  np.amax(self.targetModel.predict(np.asarray([next_state]))[0])

            self.targetModel.fit(np.asarray([state]), np.asarray([target]), epochs=1, verbose=0)





    def save(self, path):
        self.targetModel.save_weights(path)

    def load(self, path):
        self.targetModel.load_weights(path)
