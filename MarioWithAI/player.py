import json
from random import random, randint

import pygame
# import game
from constants import *
from entities import PhysicsEntity
from powerUps import PowerUp

NEIGHBOURS_OFFSET = [[0, 0], [-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]
NEIGHBOURS_OFFSET_4 = [[-1, 0], [1, 0], [0, -1], [0, 1]]


class Player(PhysicsEntity):  # Inherit from PhysicsEntity
    def __init__(self, game, pos=(0, 0), size=(16, 16)):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.acceleration = [0, 0]
        self.touched_finish = False

        self.lives = 3
        self.score = 0
        self.coins = 0

    def perform_action(self, action):
        # Define how actions map to player movements
        if action == 0:  # Move left
            self.move_left()
        elif action == 1:  # Move right
            self.move_right()
        elif action == 2:  # Jump
            self.jump()
        elif action == 3:  # No-op
            self.no_op()

    def move_left(self):
        # Implement movement logic
        self.acceleration[0] = -PLAYER_SPEED

    def move_right(self):
        # Implement movement logic
        self.acceleration[0] = PLAYER_SPEED

    def jump(self):
        # Implement jump logic
        if self.collisions['down']:
            self.velocity[1] = -PLAYER_SPEED * 4
            # self.game.sound.play_sfx('jump')

    def no_op(self):
        # Implement no operation
        self.acceleration[0] = 0

    def getNearestEnemyPosition(self):
        min_distance = 1000000
        nearest_enemy = None
        for enemy in self.game.currentLevel.enemiesList:
            distance = abs(self.pos[0] - enemy.pos[0])
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy
        return nearest_enemy.pos


    def getTilesAroundPlayer(self):
        # return 4 booleans, if there is a tile around the player in each direction
        # up, down, left, right
        tile_loc = (int((self.pos[0] + self.size[0] // 2) // self.size[0]), int(self.pos[1] // self.size[1]))
        tiles = [False, False, False, False]

        for offset in NEIGHBOURS_OFFSET_4:
            check_loc = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if check_loc in self.game.tilemap.tilemap:
                tiles[NEIGHBOURS_OFFSET_4.index(offset)] = True

        return tiles




    def savePlayer(self):
        directory = "saves/"
        file = open(directory + 'playerSave.json', 'w')

        data = {}
        data['LIVES'] = self.lives
        data['SCORE'] = self.score
        data['COINS'] = self.coins

        json_data = json.dumps(data, indent=4)
        file.write(json_data)

    def loadPlayer(self):
        directory = "saves/"
        file = open(directory + 'playerSave.json', 'r')
        data = json.load(file)

        self.lives = data['LIVES']
        self.score = data['SCORE']
        self.coins = data['COINS']

    def loadNewPlayer(self):
        self.lives = 3
        self.score = 0
        self.coins = 0

    def hitHead(self):
        if self.collisions['up']:
            return True
        return False

    def killingJump(self):
        self.velocity[1] = -PLAYER_SPEED

    def updateFacingDirection(self):
        if self.velocity[0] < 0:
            self.facingRight = True
        else:
            self.facingRight = False

    def die(self):
        self.lives -= 1
        self.game.sound.play_sfx('death')  # Play death sound

        if self.lives <= 0:
            self.game.running = False
            return

        # self.savePlayer()
        # Wait a second before restarting the Game.
        pygame.time.wait(500)
        self.game.saveGame()
        self.game.restartGame()

    def updateFinishScore(self):
        jump_height = 11 - self.pos[1] // self.size[1]

        if 2992 < self.pos[0] and 0 < jump_height < 10 and self.touched_finish == False:
            self.touched_finish = True
            self.score += self.game.end_level_rewards[int(jump_height)]

    def update(self, movement=(0, 0)):
        super().update()
        #print(self.pos)
        if self.pos[1] > 250:
            self.die()

        self.air_time += 1

        if self.collisions['down']:
            self.air_time = 0

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        # self.score += 10
        # self.coins += 1

        if self.hitHead() == True:
            tile = self.getTileAbovePlayer()
            # print(tile)
            if tile != None and tile['type'] == 'mystery':
                # self.game.tilemap.hitTileAnimation(tile['pos'])
                self.game.tilemap.setTile(tile['pos'], 'mystery/used')
                if (randint(0, 10) == 0):
                    self.game.sound.play_sfx('powerup_appear')  # Play power-up collect sound effect
                    position = (tile['pos'][0] * 16, tile['pos'][1] * 16 - 16)
                    self.game.currentLevel.powerUpsList.append(
                        PowerUp(self.game, pos=position, size=(16, 16)))
                else:
                    self.coins += 1
                    self.game.sound.play_sfx('coin')  # Play coin sound

        self.updateFinishScore()

    def getTileAbovePlayer(self):
        tile_loc = (int((self.pos[0] + self.size[0] // 2) // self.size[0]), int(self.pos[1] // self.size[1]))
        check_loc = str(tile_loc[0]) + ';' + str(tile_loc[1] - 1)
        if check_loc in self.game.tilemap.tilemap:
            return self.game.tilemap.tilemap[check_loc]
        return None

    def updateVelocity(self):
        # Apply acceleration to velocity
        self.velocity[0] += self.acceleration[0] * 1 / 10

        # self.velocity[1] = max(-5, self.velocity[1])
        if self.velocity[0] > 5:
            self.velocity[0] = 5
        if self.velocity[0] < -5:
            self.velocity[0] = -5

        # Apply friction to velocity for smooth stopping
        self.velocity[0] *= (1 - FRICTION)

    def move(self):
        self.updateVelocity()
        super().move()

        # Boundary checks to prevent the player from moving out of the screen
        if self.pos[0] < self.game.render_camera[0]:
            self.pos[0] = self.game.render_camera[0]

    def checkEvents(self, eventList):
        for event in eventList:
            # Movement with W A S D and arrows
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    # jump only if player is on the ground
                    # if self.velocity[1] == 0:
                    self.velocity[1] = -PLAYER_SPEED * 4
                    self.game.sound.play_sfx('jump')  # Play jump sound
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.velocity[1] = PLAYER_SPEED
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.acceleration[0] > 0:
                        self.acceleration[0] = 0
                    else:
                        self.acceleration[0] = -PLAYER_SPEED
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.acceleration[0] < 0:
                        self.acceleration[0] = 0
                    else:
                        self.acceleration[0] = PLAYER_SPEED

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    if self.velocity[1] < 0:
                        self.velocity[1] = 0
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.velocity[1] = 0
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    if self.acceleration[0] == 0:
                        self.acceleration[0] = PLAYER_SPEED
                    else:
                        self.acceleration[0] = 0
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    if self.acceleration[0] == 0:
                        self.acceleration[0] = -PLAYER_SPEED
                    else:
                        self.acceleration[0] = 0

    '''
    def render(self, surf):
        surf.blit(self.image, self.pos)
    '''
