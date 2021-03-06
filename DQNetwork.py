import random  # For sampling batches from the observations
from collections import deque  # For storing moves

import numpy as np
import tensorflow as tf
from keras.layers import Dense, Dropout  # Dense layers are fully connected layers, Dropout for prevent overfitting
from keras.models import Sequential  # One layer after the other
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
        self.gamma = 0.9  # discount rate
        self.learning_rate = 0.0001
        self.online_lr = 0.0001
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
        model.compile(loss=self.huber_loss, optimizer=Adam(lr=self.learning_rate))
        return model

    def build_online_model(self):
        """
            Build the different layers of the neural network for Deep Q Learning
        """
        model = Sequential()
        model.add(Dense(units=100, input_shape=(self.state_size,), activation="relu"))
        model.add(Dropout(0.25))
        model.add(Dense(units=50, activation="relu"))
        model.add(Dense(self.action_size, activation="linear"))
        model.compile(loss=self.huber_loss, optimizer=Adam(lr=self.online_lr))
        return model

    @staticmethod
    def huber_loss(y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond = tf.keras.backend.abs(error) < clip_delta

        squared_loss = 0.5 * tf.keras.backend.square(error)
        linear_loss = clip_delta * (tf.keras.backend.abs(error) - 0.5 * clip_delta)

        return tf.where(cond, squared_loss, linear_loss)

    def remember(self, state, rewards, next_state, done):
        self.memory.append((state, rewards, next_state, done))

    def act(self, state):
        act_values = self.targetModel.predict(np.asarray([state]))
        return act_values[0]

    def updateTargetModel(self):
        self.targetModel.set_weights(self.model.get_weights())

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
