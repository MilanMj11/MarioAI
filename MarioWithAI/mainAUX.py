import os

import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_checker import check_env
from MarioEnv import MarioEnv

# Path to the model file
model_path = "dqn_mario.zip"

# Initialize the custom Mario environment
env = MarioEnv()

# Check if the environment is valid
check_env(env)


# Check if the model file exists
if os.path.exists(model_path):
    # Load the model
    model = DQN.load(model_path, env=env)
    print("Model loaded successfully.")
else:
    # Create the DQN model
    model = DQN('MlpPolicy', env, verbose=1)
    print("New model created.")


# Train the model
model.learn(total_timesteps=100000)

# Save the model
model.save(model_path)
print("Model saved successfully.")

print("ok")
# Enjoy trained agent
obs, info = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, truncated, info = env.step(action)
    env.render()

    if done:
        obs, info = env.reset()
