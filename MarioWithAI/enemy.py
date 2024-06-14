import pygame
import random

from utils import load_image
from constants import *
from entities import PhysicsEntity
from PIL import Image

class Enemy(PhysicsEntity):
    def __init__(self, game, name, color=None, pos=(0, 0), size=(16, 16)):
        self.name = name
        self.walking = 0
        self.index = 0
        self.walking_animation_frame = 0
        self.walking_animation_duration = 250
        self.walking_animation_timer = 0
        self.color = color
        #self.animation = self.game.assets[self.type + '/' + self.name + '/' + self.action].copy()
        #self.image = self.game.assets['enemy']
        # self.animation = self.game.assets['enemy/run'].copy()
        super().__init__(game, 'enemy', pos, size)
        self.set_action('run')
        size = self.get_enemy_image_size()[1]
        self.setAnimationOffset((0, min(16 - size + 1, 0)))

    '''
    def update_animation(self):
        self.walking_animation_timer += self.game.clock.get_time()
        if self.walking_animation_timer >= self.walking_animation_duration:
            self.walking_animation_timer = 0
            self.walking_animation_frame = 1 - self.walking_animation_frame
            self.image = load_image(self.game.assets['enemy/run'] + str(self.walking_animation_frame) + '.png')

    '''

    def setAnimationOffset(self, offset):
        self.anim_offset = offset

    def die(self):
        self.game.Level1.enemiesList.remove(self)

    def check_collision_with_player(self):
        player_rect = self.game.player.rect()
        enemy_rect = self.rect()

        if enemy_rect.colliderect(player_rect):
            #print(player_rect.x, player_rect.y, enemy_rect.x, enemy_rect.y)
            if enemy_rect.x - self.size[0]//8*7 <= player_rect.x <= enemy_rect.x + self.size[0] and enemy_rect.y - self.size[1] <= player_rect.y <= enemy_rect.y - 1 :
                self.die()
                self.game.player.score += 100
                self.game.player.killingJump()
            else:
                self.game.player.die()
                # self.game.loadGame()
                # self.game.running = False

    def check_collision_with_other_enemy(self):
        frame_movement = (self.movement[0] + self.velocity[0], self.movement[1] + self.velocity[1])
        enemy_rect = self.rect()
        for enemy in self.game.Level1.enemiesList:
            if enemy != self:
                enemy2_rect = enemy.rect()
                if enemy_rect.colliderect(enemy2_rect):
                    self.flip = not self.flip
                    self.movement = (- 0.5 if self.flip else  0.5, self.movement[1])
                    enemy.flip = not enemy.flip
                    enemy.movement = (- 0.5 if enemy.flip else  0.5, enemy.movement[1])

    def showIfIsOnScreen(self):
        if self.game.camera[0] + VIRTUALSCREEN_WIDTH < self.pos[0]:
            return False
        self.walking = 1
        return True

    def set_action(self, action):
        #if action != self.action:
        self.action = action
        self.animation = self.game.assets[self.type + '/' + self.name + '/' + self.color + '/' + self.action].copy()

    def get_enemy_image_size(self):
        if self.color == None:
            image_path = 'data/images/entities/enemy/' + self.name + '/' + self.action + '/0.png'
        else: image_path = 'data/images/entities/enemy/' + self.name + '/' + self.color + '/' + self.action + '/0.png'

        image = Image.open(image_path)
        return image.size
        #self.setAnimationOffset(0, 16 - + 1)

    def update(self):

        if self.walking:
            if (self.collisions['right'] or self.collisions['left']):
                self.flip = not self.flip
                #self.movement = (0, self.movement[1])
                self.movement = (- 0.5 if self.flip else 0.5, self.movement[1])
            else:
                self.movement = (- 0.5 if self.flip else  0.5, self.movement[1])
            #self.walking = max(0, self.walking - 1)
        #elif random.random() < 0.01:
            #self.walking = random.randint(160, 1600)

        self.check_collision_with_player()
        self.check_collision_with_other_enemy()

        super().update()


        if self.pos[1] <= self.game.virtual_screen.get_height():
            self.action = 'run'
        else:
            self.action = 'stay'
            self.die()

        self.updateAnimation()
       #  self.update_animation()

    '''
    def render(self, surf):
        surf.blit(self.image, self.pos)
    '''