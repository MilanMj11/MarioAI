import numpy as np
import random

def discretize(value, bins):
    return np.digitize(value, bins) - 1


# Define bins for each state variable
pos_bins = np.linspace(-1, 1, 10)  # Adjust the range and number of bins as needed
velocity_bins = np.linspace(-1, 1, 10)
acceleration_bins = np.linspace(-1, 1, 10)
air_time_bins = np.linspace(0, 100, 10)
score_bins = np.linspace(0, 1000, 10)
coins_bins = np.linspace(0, 100, 10)
lives_bins = np.array([0, 1, 2, 3])


def get_discrete_state(state):
    discrete_state = (
        discretize(state['player_pos'][0], pos_bins),
        discretize(state['player_pos'][1], pos_bins),
        discretize(state['player_velocity'][0], velocity_bins),
        discretize(state['player_velocity'][1], velocity_bins),
        discretize(state['player_acceleration'][0], acceleration_bins),
        discretize(state['player_acceleration'][1], acceleration_bins),
        discretize(state['player_air_time'], air_time_bins),
        discretize(state['player_lives'], lives_bins),
        discretize(state['player_score'], score_bins),
        discretize(state['player_coins'], coins_bins)
    )
    return discrete_state
class Agent:
    def __init__(self, action_space_size, state_space_size, learning_rate=0.1, discount_factor=0.99, exploration_rate=1.0, exploration_decay=0.995):
        self.action_space_size = action_space_size
        self.state_space_size = state_space_size
        self.q_table = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = exploration_decay
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.min_epsilon = 0.01

    def choose_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.randint(0, self.action_space_size)
        else:
            discrete_state = get_discrete_state(state)
            return np.argmax([self.q_table.get(discrete_state + (a,), 0) for a in range(self.action_space_size)])

    def update_q_table(self, state, action, reward, next_state, done):
        discrete_state = get_discrete_state(state)
        discrete_next_state = get_discrete_state(next_state)
        max_future_q = max([self.q_table.get(discrete_next_state + (a,), 0) for a in range(self.action_space_size)])
        current_q = self.q_table.get(discrete_state + (action,), 0)

        if done:
            new_q = reward
        else:
            new_q = (1 - self.learning_rate) * current_q + self.learning_rate * (
                    reward + self.discount_factor * max_future_q)

        self.q_table[discrete_state + (action,)] = new_q

        if done:
            self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
