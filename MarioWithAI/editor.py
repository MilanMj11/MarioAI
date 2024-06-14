import sys

from utils import load_image
from tiles import *
from constants import *

#Teritoriu de lucru: Sumi
class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('editor')
        self.screen = pygame.display.set_mode((640, 480))
        self.display = pygame.Surface((320, 240))

        self.clock = pygame.time.Clock()

        self.assets = {
            'floor': load_image('tiles/floor.png'),
            'wall': load_image('tiles/wall.png'),
            'brick_wall': load_image('tiles/brick_wall.png'),
            'mystery': load_image('tiles/mysteryBlocks/mystery1.png'),
            'pipe_up': load_image('tiles/pipes/pipe_up.png'),
            'pipe_extension': load_image('tiles/pipes/pipe_extension.png'),
            'invisible_block': load_image('tiles/invisible_block.png'),
            'end_flag': load_image('tiles/end_flag.png'),
            'castle': load_image('tiles/castle.png'),
            # 'platform': load_image('tiles/platform.png'),
            # 'mistery': load_image('tiles/mistery.png'),
        }
        self.nume = input('Numele fisierului de deschis: ')
        self.movement = [False, False, False, False]
        self.tilemap = Tilemap(self, tile_size=16)
        try:
            self.tilemap.load('Maps/' + self.nume + '.json')
        except FileNotFoundError:
            print('Nu exista fisierul cu numele ' + self.nume + '.json')
            if input('Doresti sa creezi unul nou? (y/n) ') == 'y':
                pass
            else:
                sys.exit()


        self.scroll = [0, 0]

        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0

        self.clicking = False
        self.right_clicking = False
        self.ongrid = True

        # partea pentru schimbarea intre variante
        self.shift = False




    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            current_tile_img = self.assets[self.tile_list[self.tile_group]].copy()
            current_tile_img.set_alpha(100)

            self.tilemap.render(self.display, offset=render_scroll)

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)

            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tilemap.tile_size),
                        int((mpos[1] + self.scroll[1]) // self.tilemap.tile_size))
            if self.ongrid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tilemap.tile_size - self.scroll[0],
                                                     tile_pos[1] * self.tilemap.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, (mpos[0], mpos[1]))

            if self.clicking and self.ongrid:
                self.tilemap.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {
                    'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}

            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                for tile in self.tilemap.offgrid_tiles.copy():
                    #pentru variante
                    #tile_aux = self.assets[tile['type'][tile['variant']]]
                    tile_aux = self.assets[tile['type']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1]- self.scroll[0], tile_aux.get_width(), tile_aux.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            # cand o sa avem mai multe variante la  tileuri, o sa trebuiasca sa facem un sistem de scroll al variantei dar acum nu avem
            # current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()

            self.display.blit(current_tile_img, (5, 5))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:
                            self.tilemap.offgrid_tiles.append(
                                {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant,
                                 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True
                        # Pentru cand/daca o sa avem mai multe variante la tileuri
                        #   ''''if self.shift:
                        #       if event.button == 4:
                        #           self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                        #      if event.button == 5:
                        #          self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])

                    if event.button == 4:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        # self.tile_variant = 0
                    if event.button == 5:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        # self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_w:
                        self.movement[2] = True
                    if event.key == pygame.K_s:
                        self.movement[3] = True
                    if event.key == pygame.K_t:
                        self.tilemap.autotile()
                    if event.key == pygame.K_o:
                        self.tilemap.save('Maps/' + self.nume + '.json')
                        print('Harta salvata cu succes')
                    if event.key == pygame.K_g:
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_LSHIFT:
                        self.shift = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()
