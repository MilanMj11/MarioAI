import time
from game import GameController

class GameAI(GameController):
    def __init__(self):
        super().__init__()
        self.action_space_size = 4  # Assuming 4 actions: left, right, jump, no-op

        # Track the last X position and time
        self.last_x_pos = self.player.pos[0]
        self.last_x_change_time = time.time()

        # Track the maximum X position reached by the player and it's time
        self.max_x_pos = self.player.pos[0]
        self.max_x_pos_time = time.time()

    def restartNewGame(self):
        self.loadNewGame()
        self.Level1.init_Level()

        # Track the last X position and time
        self.last_x_pos = self.player.pos[0]
        self.last_x_change_time = time.time()

        # Track the maximum X position reached by the player and it's time
        self.max_x_pos = self.player.pos[0]
        self.max_x_pos_time = time.time()

        self.player.lives = 3

    def get_state(self):
        player = self.player
        state = {
            'player_pos': player.pos,
            'player_velocity': player.velocity,
            'player_acceleration': player.acceleration,
            'player_air_time': player.air_time,
            'player_score': player.score,
            'player_coins': player.coins,
            'player_touched_finish': player.touched_finish,
            'nearest_enemy_pos': player.getNearestEnemyPosition(),
            'distance_to_nearest_enemy': player.distanceToNearestEnemy()
        }
        return state

    def get_reward(self):
        player = self.player
        reward = 0

        # Reward for progress in the level
        reward += player.pos[0] * (self.currentLevel.current_time / 100 + 1)

        # Reward for collecting coins
        reward += player.coins * 10

        # Reward for killing enemies
        reward += player.score

        # Reward for finishing the level
        if player.touched_finish:
            reward += 100000

        # Penalty for falling off the screen
        if player.pos[1] > 250:
            reward = -5000

        # Penalty for not making progress
        if self.checkProgress(3):
            reward -= 100

        # Penalty for dying:
        if player.lives < 3:
            print("OK")
            reward = -5000

        return reward

    def checkProgress(self, time_limit=10):

        player = self.player
        current_time = time.time()

        # Check if player's X position has changed
        if player.pos[0] != self.last_x_pos:
            self.last_x_pos = player.pos[0]
            self.last_x_change_time = current_time

        # Update the maximum X position reached by the player
        if player.pos[0] > self.max_x_pos:
            self.max_x_pos = player.pos[0]
            self.max_x_pos_time = current_time

        # Check if the maximum X position hasn't changed for 5 seconds
        if current_time - self.max_x_pos_time > time_limit:
            return True

        # Terminate if X position hasn't changed for 5 seconds
        if current_time - self.last_x_change_time > time_limit:
            return True

        return False

    def take_action(self, action):
        self.player.perform_action(action)

    def is_done(self):
        player = self.player

        if self.currentLevel.current_time <= 1 or player.lives <= 2 or player.touched_finish or player.pos[1] > 350:
            return True
        return False
