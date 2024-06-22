import os
import pickle
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.buffers import ReplayBuffer
from stable_baselines3.common.env_checker import check_env
from MarioEnv import MarioEnv
import numpy as np

# Path to the model file and replay buffer
model_path = "dqn_mario.zip"
replay_buffer_path = "dqn_mario_replay_buffer.pkl"


# Custom DQN class with save/load replay buffer methods
class CustomDQN(DQN):
    def save_replay_buffer(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.replay_buffer, f)

    def load_replay_buffer(self, path):
        with open(path, 'rb') as f:
            self.replay_buffer = pickle.load(f)
        print(f"Replay buffer loaded. Current size: {self.replay_buffer.size()}")
        # Verify a few samples
        if self.replay_buffer.size() > 0:
            sample_idx = np.random.randint(0, self.replay_buffer.size())
            sample_transition = self.replay_buffer.observations[sample_idx]
            print(f"Sample transition at index {sample_idx}: {sample_transition}")

    def keep_rewards_above_threshold(self, threshold):
        # Create a new buffer to store the filtered transitions
        new_replay_buffer = ReplayBuffer(self.replay_buffer.buffer_size, self.replay_buffer.observation_space,
                                         self.replay_buffer.action_space, self.replay_buffer.device)

        # Iterate over the existing buffer and add transitions with rewards above the threshold to the new buffer
        for idx in range(self.replay_buffer.size()):
            if self.replay_buffer.rewards[idx] >= threshold:
                new_replay_buffer.add(
                    self.replay_buffer.observations[idx],
                    self.replay_buffer.next_observations[idx],
                    self.replay_buffer.actions[idx],
                    self.replay_buffer.rewards[idx],
                    self.replay_buffer.dones[idx],
                    infos=[{}]
                )

        # Replace the old buffer with the new one
        self.replay_buffer = new_replay_buffer
        print(f"Replay buffer filtered. Current size: {self.replay_buffer.size()}")

        self.save_replay_buffer(replay_buffer_path)

    '''
    def keep_rewards_above_threshold(self, threshold):
        for idx in range(self.replay_buffer.size()):
            reward = self.replay_buffer.rewards[idx]
            if reward < threshold:
               self.replay_buffer.remove(idx)
    '''


# Initialize the custom Mario environment
env = MarioEnv()

# Check if the environment is valid
check_env(env)

# Check if the model file exists
if os.path.exists(model_path):
    # Load the model
    model = CustomDQN.load(model_path, env=env)
    print("Model loaded successfully.")

    # Check if the replay buffer file exists
    if os.path.exists(replay_buffer_path):
        model.load_replay_buffer(replay_buffer_path)
        print("Replay buffer loaded successfully.")
else:
    # Create the DQN model
    model = CustomDQN('MlpPolicy', env, verbose=1)
    print("New model created.")

# model.keep_rewards_above_threshold(2500)

# Train the model
model.learn(total_timesteps=10000)

# Save the model and replay buffer
model.save(model_path)
model.save_replay_buffer(replay_buffer_path)
print("Model and replay buffer saved successfully.")

print("ok")
# Enjoy trained agent
obs, info = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    env.render()

    if done:
        obs, info = env.reset()

env.close()
