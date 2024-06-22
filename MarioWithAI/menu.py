import pygame
from constants import *
from gameStateManager import GameStateManager

SCALING_FACTOR = SCREEN_WIDTH / VIRTUALSCREEN_WIDTH

pygame.init()
pygame.font.init()

pixel_font = pygame.font.Font('data/fonts/Pixeltype.ttf', 32)
pixel_font_bigger = pygame.font.Font('data/fonts/Pixeltype.ttf', 64)
class Menu:
    def __init__(self, game, type):
        self.type = type
        self.game = game
        self.image = None
        '''
        self.text_rect_play = None
        self.text_surface_play = None
        self.text_rect_ai = None
        self.text_surface_ai = None
        '''
        self.play_rect = None
        self.ai_rect = None
        self.level1_rect = None
        self.level2_rect = None
        self.loadMenu()

    def changeType(self, type):
        self.type = type
        self.play_rect = None
        self.ai_rect = None
        self.level1_rect = None
        self.level2_rect = None
        self.loadMenu()

    def loadMenu(self):
        if self.type == "Start Menu":
            self.image = pygame.image.load("data/images/menus/StartMenu4.jpg")
            self.image = pygame.transform.scale(self.image, (VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
            self.play_rect = pygame.Rect(50, 150, 100, 100)
            self.ai_rect = pygame.Rect(250, 150, 100, 100)

        if self.type == "Level Menu":
            self.image = pygame.image.load("data/images/menus/level_menu.jpg")
            self.image = pygame.transform.scale(self.image, (VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
            self.level1_rect = pygame.Rect(50, 100, 100, 50)
            self.level2_rect = pygame.Rect(250, 100, 100, 50)

        if self.type == "Pause Menu":
            self.image = pygame.image.load("data/images/menus/PauseMenu.png")

    def handleEvents(self, eventList):
        for event in eventList:
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = x / SCALING_FACTOR
                y = y / SCALING_FACTOR
                if self.type == "Start Menu" and self.play_rect.collidepoint(x, y):
                    #self.game.gameStateManager.switchGameState("Level 1")
                    self.changeType("Level Menu")
                elif self.type == "Level Menu" and self.level1_rect.collidepoint(x, y):
                    self.game.gameStateManager.switchGameState("Level 1")
                    #self.game.setCurrentLevel(1)
                elif self.type == "Level Menu" and self.level2_rect.collidepoint(x, y):
                    self.game.gameStateManager.switchGameState("Level 2")
                    #self.game.setCurrentLevel(2)

    def update(self):
        pass

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect(center=(x,y))
        surface.blit(text_obj, text_rect)

    def renderStartMenu(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), self.play_rect)
        pygame.draw.rect(surf, (255, 255, 255), self.ai_rect)
        self.draw_text("PLAY", pixel_font, (0, 0, 0), surf, self.play_rect.x + self.play_rect.width // 2 , self.play_rect.y + self.play_rect.height // 2)
        self.draw_text("AI", pixel_font,  (0, 0, 0), surf, self.ai_rect.x + self.ai_rect.width // 2, self.ai_rect.y + self.ai_rect.width // 2)
        self.draw_text("WELCOME TO", pixel_font_bigger,  (255, 255, 255), surf, 200, 50)
        self.draw_text("MARIO", pixel_font_bigger, (255, 255, 255), surf, 200, 100)

    def renderLevelMenu(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), self.level1_rect)
        pygame.draw.rect(surf, (255, 255, 255), self.level2_rect)
        self.draw_text("LVL 1", pixel_font, (200, 150, 50), surf, self.level1_rect.x + self.level1_rect.width // 2,
                       self.level1_rect.y + self.level1_rect.height // 2)
        self.draw_text("LVL 2", pixel_font, (200, 150, 50), surf, self.level2_rect.x + self.level2_rect.width // 2,
                       self.level2_rect.y + self.level2_rect.height // 2)

    def render(self, surf):
        surf.blit(self.image, (0, 0))
        if self.type == "Start Menu":
            self.renderStartMenu(surf)
        if self.type == "Level Menu":
            self.renderLevelMenu(surf)

