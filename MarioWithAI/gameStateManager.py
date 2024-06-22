import pygame
from constants import *


class GameStateManager:
    def __init__(self, game, gameState):
        self.game = game
        self.gameState = gameState
        self.previousGameState = None

    def returnToPreviousGameState(self):
        self.gameState = self.previousGameState

    def switchGameState(self, gameState, menuType=None):
        self.previousGameState = self.gameState
        self.gameState = gameState

        if gameState == "Menu":
            self.game.menu.changeType(menuType)

        # I don't need a loading screen when accessing the Menu
        if gameState != "Menu":
            self.game.renderLoadingScreen()

        if "Level" in gameState:
            self.game.advanceToNextLevel()

        if "Level 1" == gameState:
            self.game.setCurrentLevel(1)

        if "Level 2" == gameState:
            self.game.setCurrentLevel(2)
