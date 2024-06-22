
from Levels.level2 import Level2
from constants import *
# from player import Player
from tiles import *
from gameStateManager import GameStateManager
from utils import load_image, load_images, Animation
from player import Player
from Levels.level1 import Level1
from hud import HUD
from menu import Menu
from sound import Sound

class GameController:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Mario with AI")

        self.virtual_screen = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.maxLevel = 1
        #self.gameStateManager = GameStateManager(self, "Level 1")
        self.gameStateManager = GameStateManager(self, "Menu")
        #self.menu = Menu(self, "Pause Menu")
        self.menu = Menu(self, "Start Menu")

        self.camera = [0, -60]
        self.render_camera = [0, 0]
        self.eventList = None

        self.background = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.background.fill((92, 148, 252))
        self.background_image = load_image('background.png')

        self.movement = [False, False]
        self.loadingImage = pygame.image.load("data/images/menus/LoadingScreenImage.png").convert_alpha()

        self.darken_surface = pygame.Surface((VIRTUALSCREEN_WIDTH, VIRTUALSCREEN_HEIGHT))
        self.darken_surface.set_alpha(128)  # Adjust alpha for transparency; 0 is fully transparent, 255 is fully opaque
        self.darken_surface.fill((0, 0, 0))  # Fill with black color to darken the screen

        self.end_level_rewards = [0, 400, 700, 1100, 1500, 2000, 2600, 3200, 4000, 5000]

        self.assets = {
            'floor': load_image('tiles/floor.png'),
            'wall': load_image('tiles/wall.png'),
            'brick_wall': load_image('tiles/brick_wall.png'),
            'mystery': load_image('tiles/mysteryBlocks/mystery1.png'),
            'mystery/used': load_image('tiles/mysteryBlocks/mystery4.png'),
            'pipe_up': load_image('tiles/pipes/pipe_up.png'),
            'pipe_extension': load_image('tiles/pipes/pipe_extension.png'),
            'invisible_block': load_image('tiles/invisible_block.png'),
            'end_flag': load_image('tiles/end_flag.png'),
            'castle': load_image('tiles/castle.png'),
            # 'platform': load_image('tiles/platform.png'),
            # 'mistery': load_image('tiles/mistery.png'),
            'player': load_image('entities/mario/mario.png'),
            'enemy': load_image('entities/enemy/goombas/red/run/0.png'),
            'enemy/run': Animation(load_images('entities/enemy/goombas/blue/run/'), img_dur=25),
            'enemy/goombas/red/run': Animation(load_images('entities/enemy/goombas/red/run/'), img_dur=25),
            'enemy/koopas/green/run': Animation(load_images('entities/enemy/koopas/green/run/'), img_dur=25),
            'enemy/bloopa/white/run': Animation(load_images('entities/enemy/bloopa/white/run/'), img_dur=50),
            'clouds': 'clouds/',
            'player/idle': Animation(load_images('entities/mario/idle'), img_dur=6),
            'player/run': Animation(load_images('entities/mario/run'), img_dur=4),
            'player/jump': Animation(load_images('entities/mario/jump'), img_dur=4),
            'player/die': Animation(load_images('entities/mario/die'), img_dur=4),
            'player/flag': Animation(load_images('entities/mario/flag'), img_dur=4),
            'player/pipeHorizontal': Animation(load_images('entities/mario/pipeHorizontal'), img_dur=4),
            'player/pipeVertical': Animation(load_images('entities/mario/pipeVertical'), img_dur=6),
            # 'powerUps/mushroom': load_image('entities/powerUps/Mushrooms/2.png')
            'mushroom': load_image('entities/powerUps/Mushrooms/mushroom.png'),
            'mushroom/run': Animation(load_images('entities/powerups/Mushrooms/move/'), img_dur=6),
            'mushroom/idle': Animation(load_images('entities/powerups/Mushrooms/move/'), img_dur=6),
        }

        self.tilemap = None
        self.player = Player(self)

        # Game information:
        self.current_world = 1
        self.current_level = 1

        # Scenes

        self.Level1 = Level1(self)
        self.Level2 = None
        self.Level3 = None

        self.currentLevel = self.Level1



        # Game HUD:
        self.hud = HUD(self)

        # Initialize the Sound class
        self.sound = Sound()
        self.sound.play_music('soundtrack')  # Play background music

    def restartGame(self):
        self.currentLevel.init_Level()

    def setCurrentLevel(self, number=1):
        pass

    def startGame(self):
        self.loadNewGame()

    def loadNewGame(self):
        self.player.loadNewPlayer()
        self.player.savePlayer()
        self.current_world = 1
        self.current_level = 0

    '''
    def loadLevel1(self):
        self.Level1 = Level1(self)
        self.Level1.init_Level_1()
    '''

    def saveGame(self):
        self.player.savePlayer()

        directory = "saves/"
        file = open(directory + 'gameSave1.json', 'w')

        data = {}
        data['CURRENT_WORLD'] = self.current_world
        data['CURRENT_LEVEL'] = self.current_level

        json_data = json.dumps(data, indent=4)
        file.write(json_data)

    def loadGame(self):
        directory = "saves/"
        file = open(directory + 'gameSave1.json', 'r')
        data = json.load(file)

        self.current_world = data['CURRENT_WORLD']
        self.current_level = data['CURRENT_LEVEL']

        self.player.loadPlayer()

    def advanceToNextLevel(self):

        self.current_level += 1

        if self.current_level > 4:
            self.current_level = 1
            self.current_world += 1

        self.saveGame()

    def renderLoadingScreen(self):

        loadingScreenImg = self.loadingImage
        loadingScreenImg = pygame.transform.scale(loadingScreenImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(loadingScreenImg, (0, 0))
        pygame.display.flip()

    def updatePlayer(self):
        # update the player
        self.player.update()

    def updateCamera(self):

        # camera follows the player with a smooth effect , MIGHT CHANGE VALUES LATER
        last_camera = self.camera[0]

        self.camera[0] += (self.player.pos[0] - self.camera[0] - VIRTUALSCREEN_WIDTH / 2 + self.player.size[
            0] / 2) / CAMERA_FOLLOW_RATE

        if self.camera[0] < last_camera:
            self.camera[0] = last_camera
        #self.camera[1] += (self.player.pos[1] - self.camera[1] - VIRTUALSCREEN_HEIGHT / 2 + self.player.size[
           # 1] / 2) / CAMERA_FOLLOW_RATE
        self.render_camera = [(self.camera[0]), (self.camera[1])]

    def update(self):
        # print(self.currentLevel.enemiesList[0].pos)
        #print(self.player.lives)

        if self.running == False:
            pygame.quit()
            quit()

        if self.gameStateManager.gameState == "Menu":
            self.menu.update()

        if self.gameStateManager.gameState == "Level 1":
            self.Level1.updateLevel()

        self.hud.updateHUD()

        # I don't want the clock to be ticking when in the menu
        # As I could exploit the time
        if self.gameStateManager.gameState != "Menu":
            self.clock.tick(FPS)

        self.checkGameEvents()
        self.render()

    def resetPlayerMovement(self):
        self.player.movement = [0, 0]
        self.player.acceleration = [0, 0]
        self.player.velocity = [0, 0]

    def checkGameEvents(self):

        self.eventList = pygame.event.get()

        if self.gameStateManager.gameState == "Menu":
            self.menu.handleEvents(self.eventList)

        if self.gameStateManager.gameState == "Level 1":
            self.Level1.checkEvents(self.eventList)

        for event in self.eventList:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.gameStateManager.gameState != "Menu":
                        self.gameStateManager.switchGameState("Menu","Pause Menu")
                    else:
                        self.gameStateManager.returnToPreviousGameState()


    def render(self):

        # render background on the virtual screen
        self.virtual_screen.blit(self.background, (0, 0))
        self.background.fill((92, 148, 252))
        self.virtual_screen.blit(self.background_image, (-self.camera[0], 45))

        self.hud.renderHUD(self.virtual_screen)

        # --- Rendering the correct Scene based on the gameState ---

        if self.gameStateManager.gameState == "Level 1":
            self.Level1.renderLevel(self.virtual_screen, self.render_camera)

        # --- Rendering the correct Scene based on the gameState ---


        if self.gameStateManager.gameState == "Menu":
            self.currentLevel.renderLevel(self.virtual_screen, self.render_camera)

            # If paused I darken the screen
            if self.menu.type == "Pause Menu":
                self.virtual_screen.blit(self.darken_surface, (0, 0))

            self.menu.render(self.virtual_screen)

        # scale the virutal screen onto the actual screen
        scaledScreen = pygame.transform.scale(self.virtual_screen, (SCREEN_WIDTH, SCREEN_HEIGHT), self.screen)
        self.screen.blit(scaledScreen, (0, 0))

        pygame.display.flip()
        pygame.display.update()
