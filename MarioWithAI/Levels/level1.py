import pygame

from enemy import Enemy
from constants import *
from tiles import *
from gameStateManager import GameStateManager
from Levels.level import Level

from tiles import Tilemap


class Level1(Level):
    def __init__(self, game):
        super().__init__(game)
        self.init_Level()

    def init_Level(self):

        self.current_time = 300
        self.aux_time = 100

        self.game.player.loadPlayer()
        self.enemiesList = []
        # super().init_Level()

        self.game.background.fill((108, 190, 237))
        self.game.tilemap = Tilemap(self.game)

        self.enemiesPositions = [(400, 200), (650, 200), (850, 200), (1108, 10), (1140, 10), (1368, 200), (1388, 200),
                                 (1528, 200), (1638, 200), (1658, 200), (1942, 200), (1962, 200), (2002, 200),
                                 (2027, 200), (2646, 200), (2666, 200)]

        self.enemiesType = [("goombas", "red"), ("goombas", "red"), ("goombas", "red"), ("goombas", "red"),
                            ("goombas", "red"), ("goombas", "red"), ("goombas", "red"), ("koopas", "green"),
                            ("goombas", "red"), ("goombas", "red"), ("goombas", "red"), ("goombas", "red"),
                            ("goombas", "red"), ("goombas", "red"), ("goombas", "red"), ("goombas", "red")]

        self.enemiesOffsets = []
        self.nrOfEnemies = 16

        self.powerUpsPositions = [(10, 20)]

        ''' Incarcam pe tilemap harta levelului 1 '''
        # levels/level1.json
        self.game.tilemap.load("Maps/map1.json")

        ''' Spawning the enemies '''

        for i in range(self.nrOfEnemies):
            enemy = Enemy(self.game, name=self.enemiesType[i][0], color=self.enemiesType[i][1], pos=self.enemiesPositions[i])
            #enemy.setAnimationOffset((0, 16-24+1))
            self.enemiesList.append(enemy)

        ''' Setam pozitia initiala a playerului '''
        self.game.player.pos = [50, 175]

        self.game.camera = [0, -60]
        self.game.render_camera = [0, 0]

    def checkEvents(self, eventList):
        super().checkEvents(eventList)
        ''' Here we check for the event of ending the Level and going through to the next one '''
        # if Something ->
        # then self.game.gameStateManager.switchGameState("Level 2")
