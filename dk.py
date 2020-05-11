import pygame as pg
import pygame.gfxdraw
import math
import random
import util
from util import tile_width, tile_height


pg.display.init()
pg.display.set_caption("Dungeon King - v0.1.0")
pg.display.set_mode([0, 0])


class Colors(object):
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    key = (255, 0, 128)
    background = (20, 30, 70)

    def __init__(self):
        pass


colors = Colors()
trees = pg.image.load("art/trees.png").convert_alpha()
trees.set_colorkey(colors.key)
trees = trees.convert_alpha()


class GameState(object):
    def __init__(self, screen_dimensions):
        self.screen = pg.display.set_mode(
            screen_dimensions,
            pg.RESIZABLE)
        self.screen_width = screen_dimensions[0]
        self.screen_height = screen_dimensions[1]
        self.scroll_x = 0
        self.scroll_y = 0
        self.dragging_map = False
        self.drag_offset = None
        self.clock = pg.time.Clock()
        self.game_map = None
        self.render_size = 2.0

    def drag_map(self, pos):
        if not self.drag_offset:
            x = self.scroll_x - pos[0]
            y = self.scroll_y - pos[1]
            self.drag_offset = (x, y)
        self.scroll_x = pos[0] + self.drag_offset[0]
        self.scroll_y = pos[1] + self.drag_offset[1]


class DisplayLayer(pg.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        layer_width = tile_width * width
        layer_height = tile_height * height
        self.image = pg.Surface([layer_width, layer_height])
        self.image.fill(colors.key)


class GameMap(object):
    def __init__(self, map_size):
        self.width = map_size
        self.height = map_size
        self.tile_rows, self.tiles = self.setup_new_map(map_size)
        self.terrain_display_layer = self.paint_terrain_layer(self.tile_rows)

    def setup_new_map(self, map_size):
        tile_rows = []
        tiles = []
        self.map_size = map_size
        for y in range(map_size):
            new_row = []
            for x in range(map_size):
                new_tile = GameTile(x, y)
                new_row.append(new_tile)
                tiles.append(new_tile)
            tile_rows.append(new_row)
        return tile_rows, tiles

    def paint_terrain_layer(self, tile_rows):
        terrain_display_layer = DisplayLayer(self.map_size, self.map_size)
        background_x_middle = terrain_display_layer.image.get_width() / 2
        for y_row in tile_rows:
            for tile in y_row:
                # ---- Pixel Stuff ---- #
                x, y = util.get_pixel_coords(tile.x, tile.y)
                terrain_display_layer.image.blit(
                    tile.image,
                    [x + background_x_middle, y])
                if random.randint(1, 100) > 66:
                    terrain_display_layer.image.blit(
                        trees,
                        [x + background_x_middle, y - 81])

        terrain_display_layer.image.set_colorkey(colors.key)
        terrain_display_layer.image = (
            terrain_display_layer.image.convert_alpha())
        return terrain_display_layer


class GameTile(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.terrain = "Grass"
        self.image = pg.image.load("art/grass_border.png").convert_alpha()
        self.image.set_colorkey(colors.key)
        self.image = self.image.convert_alpha()

    def draw_polygon_tile(self):
        # ---- Setup Tile Image ---- #
        image = pg.Surface([36, 19])
        image.fill(colors.key)
        pygame.gfxdraw.filled_polygon(
            image,
            [(int(tile_width / 2) - 1, 0),
             (tile_width - 1, int(tile_height / 2) - 1),
             ((tile_width / 2) - 1, tile_height - 1),
             (0, int(tile_height / 2) - 1)],
            colors.green)
        image.set_colorkey(colors.key)
        image = image.convert_alpha()
        self.image = image


def start_new_game(screen_dimensions, map_size):
    state = GameState(screen_dimensions)
    state.game_map = GameMap(map_size)

    return state


def display_update(screen, map_image, scroll_x, scroll_y, clock, render_size):
    screen.fill(colors.background)
    if render_size == 0.5:
        scaled_map_image = pg.transform.scale2x(map_image)
    else:
        scaled_map_image = pg.transform.smoothscale(
            map_image,
            (int(map_image.get_width() / render_size),
             int(map_image.get_height() / render_size)))
    screen.blit(
        scaled_map_image,
        [scroll_x / render_size,
         scroll_y / render_size])
    pg.display.flip()
    clock.tick(60)


def left_click(state, pos):
    print(util.get_map_coords(
        pos,
        state.scroll_x,
        state.scroll_y,
        int(state.game_map.terrain_display_layer.image.get_width() / 2),
        state.render_size))


def scroll_click(state, pos):
    state.dragging_map = True
    state.drag_offset = (-pos[0] + state.scroll_x, -pos[1] + state.scroll_y)


def right_click():
    pass


def scroll_release(state):
    state.dragging_map = False
    state.drag_offset = None


def scroll_up_click(state):
    state.render_size = min(10, state.render_size + 0.1)


def scroll_down_click(state):
    state.render_size = max(state.render_size - 0.1, 1)


def mousedown_handler(state, event, pos):
    if event.button == 1:
        left_click(state, pos)
    elif event.button == 2:
        scroll_click(state, pos)
    elif event.button == 3:
        right_click()
    elif event.button == 4:
        scroll_down_click(state)
    elif event.button == 5:
        scroll_up_click(state)


def mouseup_handler(state, event):
    if event.button == 2:
        scroll_release(state)


def event_handler(pos):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.display.quit()
            pg.quit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                return True
        elif event.type == pg.MOUSEBUTTONDOWN:
            mousedown_handler(state, event, pos)
        elif event.type == pg.MOUSEBUTTONUP:
            mouseup_handler(state, event)
    return False


state = start_new_game([900, 800], 100)


while True:
    pos = pg.mouse.get_pos()
    event_handler(pos)
    if state.dragging_map is True:
        state.drag_map(pos)
    display_update(
        state.screen,
        state.game_map.terrain_display_layer.image,
        state.scroll_x,
        state.scroll_y,
        state.clock,
        state.render_size)
