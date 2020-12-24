import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *

pygame.init()  # initiates pygame

pygame.display.set_caption('Peri the pigeon')

WINDOW_SIZE = (600, 400)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface((WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2))  # used as the surface for rendering, which is scaled
background = pygame.Surface((WINDOW_SIZE[0]/2.6, WINDOW_SIZE[1]/2.6))

moving_right = False
moving_left = False
vertical_momentum = 0
air_timer = 0
v_Jump  = False
v_Jump_multi = 0
floaty = False

game_map = [['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '1'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['1', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['1', '2', '2', '2', '2', '2', '2', '0', '0', '0', '0', '0', '2', '2', '2', '2', '2', '2', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '2', '2', '2', '2', '2', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
            ['1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1', '1']]

grass_img = pygame.image.load('Migration/grass.png')
dirt_img = pygame.image.load('Migration/Soil.png')
Paraback1 = pygame.image.load('Migration/PrallaxBackground_1.png')
Paraback2 = pygame.image.load('Migration/PrallaxBackground_2.png')

player_img = pygame.image.load('Migration/Bird_Righty.png')

player_rect = pygame.Rect(100, 100, player_img.get_width(), player_img.get_height())


def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list


def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


while True:  # game loop
    background.fill((146, 244, 255))  # clear screen by filling it with blue
    background.blit(Paraback1, (0,0))
    background.blit(Paraback2, (0, 0))

    tile_rects = []
    y = 0
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * 16, y * 16))
            if tile == '2':
                display.blit(grass_img, (x * 16, y * 16))
            if tile != '0':
                tile_rects.append(pygame.Rect(x * 16, y * 16, 16, 16))
            x += 1
        y += 1

    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 8:
        vertical_momentum = 8

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1



    display.blit(player_img, (player_rect.x, player_rect.y))

    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_d:
                moving_right = True
            if event.key == K_a:
                moving_left = True
            if event.key == K_w:
                if air_timer < 15:
                    v_Jump = True
            if event.key == K_SPACE:
                floaty = True


        if event.type == KEYUP:
            if event.key == K_d:
                moving_right = False
            if event.key == K_a:
                moving_left = False
            if event.key == K_w:
                v_Jump  = False
            if event.key == K_SPACE:
                floaty = False

    if v_Jump == True:
        if v_Jump_multi < 1.6:
            v_Jump_multi += 0.1
            vertical_momentum = -2 * v_Jump_multi
    else:
        v_Jump_multi = 0.2
    if floaty == True:
        vertical_momentum = 1.5

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    display.blit(pygame.transform.scale(background, WINDOW_SIZE), (0, 0))
    pygame.display.update()
    clock.tick(60)
