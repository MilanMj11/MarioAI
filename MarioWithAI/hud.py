import pygame
from constants import *


class HUD:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font('data/fonts/Pixeltype.ttf', 32)

        self.scoreText = self.font.render("SCORE", True, (255, 255, 255))
        self.scoreNumbers = self.font.render(f"{self.game.player.score}", True, (255, 255, 255))

        self.coinsText = self.font.render("COINS", True, (255, 255, 255))
        self.coinsNumbers = self.font.render(f"{self.game.player.coins}", True, (255, 255, 255))

        self.worldText = self.font.render("WORLD", True, (255, 255, 255))
        self.worldNumbers = self.font.render(f"{self.game.current_world} - {self.game.current_level}", True,
                                             (255, 255, 255))

        self.timeText = self.font.render("  TIME", True, (255, 255, 255))
        self.timeNumbers = self.font.render(f"{self.game.currentLevel.current_time}", True, (255, 255, 255))

        self.livesText = self.font.render("LIVES", True, (255, 255, 255))
        self.livesNumbers = self.font.render(f"{self.game.player.lives}", True, (255, 255, 255))

    def updateHUD(self):
        self.scoreNumbers = self.font.render(f"{self.game.player.score}", True, (255, 255, 255))
        self.coinsNumbers = self.font.render(f"{self.game.player.coins}", True, (255, 255, 255))
        self.worldNumbers = self.font.render(f"{self.game.current_world} - {self.game.current_level}", True,
                                             (255, 255, 255))
        self.timeNumbers = self.font.render(f"{self.game.currentLevel.current_time}", True, (255, 255, 255))
        self.livesNumbers = self.font.render(f"{self.game.player.lives}", True, (255, 255, 255))

    def renderHUD(self, surf):
        ''' RENDER SCORE '''
        surf.blit(self.scoreText, (0 * (VIRTUALSCREEN_WIDTH / 5) + 10, 1))
        # render score numbers in the middle under the score text
        scoreNumbersRect = self.scoreNumbers.get_rect()
        scoreNumbersRect.center = ((0 * (VIRTUALSCREEN_WIDTH / 5) + 1 * (VIRTUALSCREEN_WIDTH / 5)) / 2, 26)
        surf.blit(self.scoreNumbers, scoreNumbersRect)
        ''' RENDER SCORE '''

        ''' RENDER COINS '''
        surf.blit(self.coinsText, (1 * (VIRTUALSCREEN_WIDTH / 5) + 10, 1))
        # render coins numbers in the middle under the coins text
        coinsNumbersRect = self.coinsNumbers.get_rect()
        coinsNumbersRect.center = ((1 * (VIRTUALSCREEN_WIDTH / 5) + 2 * (VIRTUALSCREEN_WIDTH / 5)) / 2, 26)
        surf.blit(self.coinsNumbers, coinsNumbersRect)
        ''' RENDER COINS '''

        ''' RENDER WORLD '''
        surf.blit(self.worldText, (2 * (VIRTUALSCREEN_WIDTH / 5) + 10, 1))
        # render world numbers in the middle under the world text
        worldNumbersRect = self.worldNumbers.get_rect()
        worldNumbersRect.center = ((2 * (VIRTUALSCREEN_WIDTH / 5) + 3 * (VIRTUALSCREEN_WIDTH / 5)) / 2, 26)
        surf.blit(self.worldNumbers, worldNumbersRect)
        ''' RENDER WORLD '''

        ''' RENDER TIME '''
        surf.blit(self.timeText, (3 * (VIRTUALSCREEN_WIDTH / 5) + 10, 1))
        # render time numbers in the middle under the time text
        timeNumbersRect = self.timeNumbers.get_rect()
        timeNumbersRect.center = ((3 * (VIRTUALSCREEN_WIDTH / 5) + 4 * (VIRTUALSCREEN_WIDTH / 5)) / 2, 26)
        surf.blit(self.timeNumbers, timeNumbersRect)
        ''' RENDER TIME '''

        ''' RENDER LIVES '''
        surf.blit(self.livesText, (4 * (VIRTUALSCREEN_WIDTH / 5) + 10, 1))
        # render lives numbers in the middle under the lives text
        livesNumbersRect = self.livesNumbers.get_rect()
        livesNumbersRect.center = ((4 * (VIRTUALSCREEN_WIDTH / 5) + 5 * (VIRTUALSCREEN_WIDTH / 5)) / 2, 26)
        surf.blit(self.livesNumbers, livesNumbersRect)
        ''' RENDER LIVES '''
