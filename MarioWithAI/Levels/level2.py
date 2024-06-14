from enemy import Enemy
from powerUps import PowerUp

from tiles import *

from Levels.level import Level


class Level2(Level):
    def __init__(self, game):
        super().__init__(game)

        self.init_Level()

    def init_Level(self):
        self.game.player.loadNewPlayer()
        # super().init_Level()

        self.game.background.fill((108, 190, 237))
        self.game.tilemap = Tilemap(self.game)

        self.enemiesPositions = []
        self.nrOfEnemies = 0

        self.powerUpsPositions = [(6, 6)]
        self.nrOfPowerUps = 1

        self.game.tilemap.load(r"Maps\map2.json")

        for i in range(self.nrOfEnemies):
            self.enemiesList.append(Enemy(self.game, self.enemiesPositions[i]))

        for i in range(self.nrOfPowerUps):
            self.powerUpsList.append(PowerUp(self.game, self.powerUpsPositions[i]))

        ''' Setam pozitia initiala a playerului '''
        self.game.player.pos = [50, 10]

    def checkEvents(self, eventList):
        super().checkEvents(eventList)
        ''' Here we check for the event of ending the Level and going through to the next one '''
        # if Something ->
        # then self.game.gameStateManager.switchGameState("Level 2")
