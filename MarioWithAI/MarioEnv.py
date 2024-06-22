import gymnasium as gym
import numpy as np
import time
from GameAI import GameAI


class MarioEnv(gym.Env):
    def __init__(self):
        super(MarioEnv, self).__init__()

        # Define action and observation space
        self.action_space = gym.spaces.Discrete(4)  # Assuming 4 actions: left, right, jump, no-op
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(7,), dtype=np.float32)

        self.game = GameAI()
        self.state = self.game.get_state()

    def reset(self, seed=None, options=None):
        # super().reset()
        # self.np_random, _ = gym.utils.seeding.np_random(seed)

        observation = self._get_obs()
        self.game.restartNewGame()
        print("Game reset")
        return observation, {}

    def step(self, action):
        self.game.take_action(action)
        self.game.update()  # Update game state
        reward = self.game.get_reward()
        done = self.game.is_done() or self.game.checkProgress(10)
        info = {}
        truncated = False
        return self._get_obs(), reward, done, truncated, info

    def render(self, mode='human'):
        self.game.render()

    def _get_obs(self):
        self.state = self.game.get_state()
        obs = np.array([
            self.state['player_pos'][0],
            self.state['player_pos'][1],
            self.state['player_velocity'][0],
            self.state['player_velocity'][1],
            self.state['distance_to_nearest_enemy'],
            #self.state['nearest_enemy_pos'][0],
            #self.state['nearest_enemy_pos'][1],
            self.state['player_score'],
            self.state['player_coins']
        ], dtype=np.float32)

        return obs
