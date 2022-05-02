## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

### IMPORTS AND INITIALIZATIONS ###
import pygame
from pygame import mixer
import time
import random
from random import randint

import classes
import map_reader

# PYGAME STANDARD INITIALIZATION #
pygame.init()
win_x, win_y = 800, 600
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Into the Backrooms")
clock = pygame.time.Clock()
running = True

## FONTS AND TEXT ##
big_text = pygame.font.SysFont("Arial", 32, True)
item_font = pygame.font.SysFont("Times New Roman", 18)
small_text = pygame.font.SysFont("Times New Roman", 12)

# LOADS PRELOADING IMAGE #
preload_image = pygame.image.load("Assets//Video//loading.png")

# Basic preloading function.
def preload_surf (load_string) :
    # CREATES EMPTY SURFACE #
    work_surf = pygame.Surface((win_x, win_y))

    # PRINTS PRE-LOAD TO SCREEN #
    preload_text_img = small_text.render(load_string, True, (255, 255, 255))
    work_surf.blit(preload_image, (0, 0))
    work_surf.blit(preload_text_img, ((win_x / 2) - (win_x / 20), win_y - (win_y / 10)))

    return work_surf

win.blit(preload_surf("Loading Variables..."), (0, 0))
pygame.display.flip()

## BASELINE VARIABLES ##
move_speed = 100
stunned = 0
camera_x, camera_y = 0, 0
sprinting_bool = False
stamina = 100
stamina_recharge = 0
stamina_color = (0, 255, 0)

brown = (101, 67, 33)
grey = (120, 120, 120)
green = (1, 50, 32)

targ_x, targ_y = 0, 0

inv_color1 = brown
inv_color2 = brown
inv_color3 = brown
inventory_int = None
inventory_ext = False

pathfinder = classes.pathfinder()
move_list = []

debug = False
menu = True
jam_sound = False

## VIDEO INITIALIZATION ##
win.blit(preload_surf("Loading Video Assets..."), (0, 0))
pygame.display.flip()

# LOAD IMAGES #

# GAMEPLAY IMAGES #
sam = pygame.image.load("Assets//Video//player_ss.png")

# ITEMS #
small_key = pygame.image.load("Assets//Video//Static Entities//small_key.png")
big_key = pygame.image.load("Assets//Video//Static Entities//big_key.png")
backpack = pygame.image.load("Assets//Video//Static Entities//backpack.png")
hammer = pygame.image.load("Assets//Video//Static Entities//hammer.png")
stun = pygame.image.load("Assets//Video//Static Entities//stun.png")
trap_escape = pygame.image.load("Assets//Video//Static Entities//trap_escape.png")

# TRAPS #
lost_item = pygame.image.load("Assets//Video//Static Entities//lost_item.png")
bear_trap = pygame.image.load("Assets//Video//Static Entities//trap.png")
teleport = pygame.image.load("Assets//Video//Static Entities//teleport.png")

# MAP #
carpet_img = pygame.image.load("Assets//Tilesets-Tileset Images//carpet.png")
door_img = pygame.image.load("Assets//Video//Static Entities//door.png")
top_door = pygame.image.load("Assets//Tilesets-Tileset Images//top_door.png")
right_door = pygame.image.load("Assets//Tilesets-Tileset Images//right_door.png")
left_door = pygame.image.load("Assets//Tilesets-Tileset Images//left_door.png")

# MASTER LIST OF STATIC ENTITIES #
static_list = [small_key, big_key, backpack, hammer, stun, trap_escape, lost_item, bear_trap, teleport, top_door,
               right_door, left_door, door_img]

# MAIN MENU IMAGES #
main_menu_background = pygame.image.load("Assets//Video//Main Menu//main_menu_sprites.png")

play_uc = pygame.image.load("Assets//Video//Main Menu//play_unclicked.png")
play_c = pygame.image.load("Assets//Video//Main Menu//play_clicked.png")

options_uc = pygame.image.load("Assets//Video//Main Menu//options_unclicked.png")
options_c = pygame.image.load("Assets//Video//Main Menu//options_clicked.png")

quit_uc = pygame.image.load("Assets//Video//Main Menu//quit_unclicked.png")
quit_c = pygame.image.load("Assets//Video//Main Menu//quit_clicked.png")

back_uc = pygame.image.load("Assets//Video//Main Menu//back_unclicked.png")
back_c = pygame.image.load("Assets//Video//Main Menu//back_clicked.png")

# GAME OVER IMAGES #
win_img = pygame.image.load("Assets//Video//win_screen.png")
game_over_img = pygame.image.load("Assets//Video//game_over.png")

# SPRITESHEET ITERATORS #
sam_y = 0
old_y = 0
sam_x = 0

it_speed = 1
float_iterator = 0.25

spritesheet_timer = float_iterator

# LIST INITIALIZATION #
entities = []
inventory = []
stun_balls = []
removed_mask = []
sound_radius_list = []

win.blit(preload_surf("Loading Music..."), (0, 0))
pygame.display.flip()

## MUSIC INITIALIZATION ##
mixer.init()

# CREATES AUDIO CHANNELS #
main_menu_cha = mixer.Channel(0)
amb_cha = mixer.Channel(1)

# WE WILL REQUIRE SEVERAL SFX CHANNELS #
ui_sfx = mixer.Channel(2)
player_sfx = mixer.Channel(3)
monster_scream = mixer.Channel(4)
monster_sfx = mixer.Channel(5)
static_ent_sfx = mixer.Channel(6)
item_use_sfx = mixer.Channel(7)

channels = [main_menu_cha, amb_cha, ui_sfx, player_sfx, monster_scream, monster_sfx, static_ent_sfx, item_use_sfx]

# LOADS AUDIO-FILES #

# MUSIC #
menu_light_sou = mixer.Sound("Assets//Audio//menu_light.mp3")
menu_harsh_sou = mixer.Sound("Assets//Audio//menu_harsh.mp3")
victory_music_sou = mixer.Sound("Assets//Audio//victory_music.wav")

# SOUND EFFECTS #
buzz_sou = mixer.Sound("Assets//Audio//buzz.mp3")
death_buzz_sou = mixer.Sound("Assets//Audio//SFX//death_buzz.wav")
select_sou = mixer.Sound("Assets//Audio//SFX//select.wav")
transition_sou = mixer.Sound("Assets//Audio//SFX//transition.wav")
small_step_sou = mixer.Sound("Assets//Audio//SFX//small_step.wav")
big_step_sou = mixer.Sound("Assets//Audio//SFX//big_step.wav")
high_scream_sou = mixer.Sound("Assets//Audio//SFX//mon_scream_high.mp3")
hammer_sou = mixer.Sound("Assets//Audio//SFX//hammer.wav")
pickup_sou = mixer.Sound("Assets//Audio//SFX//pickup.wav")
taser_sou = mixer.Sound("Assets//Audio//SFX//taser.wav")
trapped_sou = mixer.Sound("Assets//Audio//SFX//trapped.wav")
denied_sou = mixer.Sound("Assets//Audio//SFX//denied.wav")

# SETS MASTER AUDIO LEVEL #
mas_audio = 1
player_step = 1

# CHANGES AUDIO LEVELS TO MATCH MAS_AUDIO #
def update_audio() :
    for cha in channels :
        if cha == monster_sfx :
            cha.set_volume(mas_audio * .75)

        elif cha == player_sfx :
            cha.set_volume(mas_audio * 1.25)

        elif cha == amb_cha :
            cha.set_volume(mas_audio * .2)

        else :
            cha.set_volume(mas_audio)

update_audio()


win.blit(preload_surf("Initializing UI..."), (0, 0))
pygame.display.flip()

## UI INITIALIZATION ##
ui_index = 0

# OPTIONS MENU VARIABLES #
options_enabled = False

win.blit(preload_surf("Loading Classes..."), (0, 0))
pygame.display.flip()

## CLASS DEFINITION ##
class Monster :
    """The main monster entity. Has pathfinding, player detection, sound detection, and controls Monster
    animation and movement."""

    def __init__(self, start_pos, patrol_list=None) :
        # BASIC STATIC VARIABLES #
        self.pos = list(start_pos)
        self.monster_ss = pygame.image.load("Assets//Video//monster_ss.png").convert_alpha()
        self.rect = pygame.Rect

        # ANIMATION VARIABLES #
        self.anim_tick = .10
        self.ss_x = 0

        # PATHFINDING VARIABLES #
        self.move_speed = 225
        self.ss = 1
        self.target_list = []

        # STUN VARIABLE #
        self.stun_var = 0

        # TILE-RELATED VARIABLES #
        self.tile = None
        self.adj_list = []

    def find_target(self, call_tile) :
        """Finds the target list to the tile that called this function."""

        # PLAYS SCREAM #
        if monster_scream.get_busy() == False :
            monster_scream.play(high_scream_sou)

        # FINDS MONSTER TILE #
        for row in tiles :
            for tile in row :
                tile_rect = pygame.Rect(tile.x, tile.y, 64, 64)

                if tile_rect.collidepoint(monster.pos[0] + 32, monster.pos[1] + 32) :
                    monster.tile = tile

        self.target_list = pathfinder.pather(monster.tile, call_tile, tiles)
        return

    def update(self, delta_time) :
        """Moves Monster towards a target position if one is available. Changes face to more accurately represent
        movement."""

        ## SEARCHES FOR PLAYER ##
        for tile in self.adj_list :
            if tile == player_tile :
                self.find_target(player_tile)

        ## MOVEMENT TO TARGET ##

        # UPDATES MONSTER RECT #
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 64, 64)

        # RUNS IF NOT STUNNED #
        if self.stun_var <= 0 :
            # MONSTER PATHFINDING #
            if len(self.target_list) > 0 :
                # ESTABLISHES NECESSARY VARIABLES #
                target_tile = self.target_list[0]
                diff_x, diff_y = target_tile.x - self.pos[0], target_tile.y - self.pos[1]
                rev_x, rev_y = False, False

                # UPDATES ANIMATION VARIABLES #
                self.anim_tick -= 1 * delta_time

                # SETS DIFFERENCE TO ABSOLUTE VALUE #
                if diff_x < 0 :
                    diff_x *= -1
                    rev_x = True

                if diff_y < 0 :
                    diff_y *= -1
                    rev_y = True

                if len(self.target_list) != 0 :
                    # FINDS WHICH WAY TO MOVE #

                    # MOVES HORIZONTALLY #
                    if diff_x > diff_y :
                        # MOVES RIGHT #
                        if rev_x == False :
                            self.pos[0] += self.move_speed * delta_time
                            self.ss = 2

                        # MOVES LEFT #
                        else :
                            self.pos[0] -= self.move_speed * delta_time
                            self.ss = 3

                    # MOVES VERTICALLY #
                    if diff_y > diff_x :
                        # MOVES UP #
                        if rev_y == False :
                            self.pos[1] += self.move_speed * delta_time
                            self.ss = 1

                        else :
                            self.pos[1] -= self.move_speed * delta_time
                            self.ss = 0

                    # CHECKS FOR ANIMATION UPDATE #
                    if self.anim_tick <= 0 :
                        self.ss_x += 1
                        self.anim_tick = .1

                        # RESET SS_X IF LOOPED #
                        if self.ss_x > 7 :
                            self.ss_x = 0

                    # IF ENCOUNTERED TARGET, ITERATES TO NEXT POSITION #
                    if diff_x < 3 and diff_y < 3 :
                        self.tile = self.target_list[0]
                        self.set_adj()
                        monster_sfx.play(big_step_sou)
                        self.target_list.pop(0)

            # RESETS ANIMATION VARIABLES #
            else :
                self.anim_tick = .1
                self.ss_x = 0

        else :
            self.stun_var -= 1 * delta_time
            self.ss_x = 0

        # RETURNS WORK SURFACE WITH MONSTER #
        work_surf = pygame.Surface((64, 64)).convert_alpha()
        work_surf.fill((0, 0, 0, 0))
        work_surf.blit(self.monster_ss, (0, 0), (self.ss_x * 64, self.ss * 64, 64, 64))

        return work_surf.convert_alpha()

    def set_adj (self) :
        """Creates Monster's new list of adjacent tiles."""

        if self.ss == 0 :
            x_min, x_max, y_min, y_max = -1, 1, -3, 0

        if self.ss == 1 :
            x_min, x_max, y_min, y_max = -1, 1, 1, 4

        elif self.ss == 2 :
            x_min, x_max, y_min, y_max = 1, 4, -1, 2

        elif self.ss == 3 :
            x_min, x_max, y_min, y_max = -4, -1, -1, 2

        add_x, add_y = x_min, y_min
        temp_list = []

        # ADDS TILES TO TEMP LIST #
        while add_y < y_max :
            try :
                new_tile = tiles[monster.tile.grid_y + add_y][monster.tile.grid_x + add_x]
                add = True

            except IndexError :
                add = False
                pass

            # ITERATES THROUGH TILES #
            add_x += 1

            if add_x > x_max :
                add_x = x_min
                add_y += 1


            # ADDS TILES TO TEMP_LIST #
            if add == True :
                # CHECKS VALIDITY OF TILE #
                if new_tile.valid == False:
                    add = False

                temp_list.append(new_tile)

        # SETS ADJ_LIST #
        self.adj_list = temp_list

# MAIN MENU INITIALIZATION #

# ESTABLISHES NECESSARY VARIABLES #
button_width, button_height = play_c.get_width(), play_c.get_height()
select_sound_played = False
slider_back = pygame.Rect(win_x / 10, win_y - (win_y / 3), win_x / 1.5, win_y / 20)
slider_width = slider_back[3]

# CREATES RECTS OF ALL BUTTONS #
play_rect = pygame.Rect(200, 350, play_uc.get_width(), play_uc.get_height())

options_rect = pygame.Rect(400, 325, options_uc.get_width(), options_uc.get_height())

quit_rect = pygame.Rect(300, 450, quit_uc.get_width(), quit_uc.get_height())

back_rect = pygame.Rect(300, 450, back_uc.get_width(), back_uc.get_height())

exit_rect = pygame.Rect(400, 400, quit_uc.get_width(), quit_uc.get_height())

# CREATES STATIC LISTS FOR DATA REFERENCE #
button_rect_list = [play_rect, options_rect, quit_rect]
pressed_button_list = [play_c, options_c, quit_c]

win.blit(preload_surf("Generating Map..."), (0, 0))
pygame.display.flip()

## MAP GENERATION ##
map_loader = 0
map_surf, objects, tiles, walls = map_reader.load_map(map_loader)
doors = [map_reader.Tile(64, 64, 1, 1)]

## MONSTER GENERATION ##
mons_start_pos = [(512, 128), (128, 64)]
monster = Monster(mons_start_pos[map_loader])

## PLAYER GENERATION ##
player_start_pos = [(928, 1895), (704, 800)]
player_x, player_y = player_start_pos[map_loader][0], player_start_pos[map_loader][1]

## STATIC ENTITY GENERATION ##
for object in objects :
    entities.append(classes.StaticEntity((object[0], object[1]), object[2], object[3], static_list[int(object[2])],
                    tiles))

## FUNCTION DEFINITION ##
def game_over(victory=False) :
    """Brings player to game over screen. When this function exits, the program should terminate."""

    # ESTABLISHES BASELINE VARIABLES #
    new_quit_rect = pygame.Rect(win_x / 2.5, win_y - (win_y / 4), quit_c.get_width(), quit_c.get_height())
    running = True
    play_sound = False

    if victory == False :
        # CONFIGURES AUDIO FOR SCENE #
        main_menu_cha.play(menu_harsh_sou, -1)

        amb_cha.play(death_buzz_sou, -1)
        amb_cha.set_volume(mas_audio * .25)

        monster_scream.play(high_scream_sou)

        over_img = game_over_img

    else :
        # CONFIGURES AUDIO FOR SCENE #
        main_menu_cha.play(victory_music_sou, -1)

        over_img = win_img

    while running :
        ## COLLISION ##
        mos_pos = pygame.mouse.get_pos()

        # QUIT_RECT COLLISION #
        if new_quit_rect.collidepoint(mos_pos) :
            quit_image = quit_c
            hover_int = 0

            if play_sound == False :
                ui_sfx.play(select_sou)
                play_sound = True

        else :
            play_sound = False
            quit_image = quit_uc
            hover_int = -1

        ## EVENT HANDLER ##
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # KEYDOWN INPUT #
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            # MOUSEDOWN INPIUT #
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and hover_int == 0 :
                running = False

        ## RENDERING ##
        win.fill((0, 0, 0))

        # DRAWS BACKGROUND #
        win.blit(over_img, (0, 0))

        # DRAWS QUIT BUTTON #
        win.blit(quit_image, (new_quit_rect[0], new_quit_rect[1]))

        pygame.display.flip()
        running = False

def set_wall_tiles(item, valid_state=False) :
    if item.class_type > 8 :
        if valid_state == True :
            walls.remove(item.tile)

            # ADDS SECOND TILE AS WELL #
            if item.class_type == 9 :
                walls.remove(tiles[item.tile.grid_y][item.tile.grid_x - 1])

            if item.class_type > 9 and item.class_type != 12 :
                walls.remove(tiles[item.tile.grid_y - 1][item.tile.grid_x])

        else :
            walls.append(item.tile)

            # ADDS SECOND TILE AS WELL #
            if item.class_type == 9:
                walls.append(tiles[item.tile.grid_y][item.tile.grid_x - 1])

            if item.class_type > 9 and item.class_type != 12:
                walls.append(tiles[item.tile.grid_y - 1][item.tile.grid_x])

# ADDS DOORS TO WALLS LIST #
walls.append(map_reader.Tile(64, 64, 1, 1, False))

for entity in entities :
    set_wall_tiles(entity)

### POST-INITIALIZATION ###

# PLAYS INITIAL AUDIO CONFIGURATION #
main_menu_cha.play(menu_light_sou, -1)
amb_cha.play(buzz_sou, -1)

## MAIN GAMEPLAY LOOP ##
while running :
    # TIME CONTROL #
    delta_time = clock.tick() / 1000

    ## GAMEPLAY ##
    if ui_index is None :
        ## UPDATE ##
        pcol_x, pcol_y = player_x + 32, player_y + 32
        player_rect = pygame.Rect(pcol_x - 10, pcol_y - 18, 20, 45)

        stamina_recharge -= 1 * delta_time
        stunned -= 1 * delta_time

        # FINDS PLAYER TILE #
        for row in tiles :
            for tile in row :
                tile_rect = pygame.Rect(tile.x, tile.y, 64, 64)

                if tile_rect.collidepoint(pcol_x, pcol_y) :
                    player_tile = tile

        # FINDS TARGET TILE (DEBUG) #
        targ_tile = tiles[targ_y][targ_x]

        # STAMINA HANDLER #
        if sprinting_bool == False :
            stamina += 10 * delta_time

        else :
            stamina -= 40 * delta_time

        if stamina <= 0 :
            sprinting_bool = False
            stamina_recharge = 3
            it_speed = 1
            move_speed = 100
            stamina_color = (255, 0, 0)

        if stamina_recharge <= 0 and stamina_color != (0, 255, 0) :
            stamina_color = (0, 255, 0)

        if stamina > 100 :
            stamina = 100

        elif stamina <= 0 :
            stamina = 0

        # UPDATES MOVING STUN BALLS #
        ball_rect_list = []
        for ball in stun_balls :
            # UPDATES AND CHECKS STATE OF BALL #
            destroy = ball.update(delta_time)

            if destroy == True :
                stun_balls.remove(ball)

            # CREATES BALL_RECT #
            ball_rect_list.append(pygame.Rect(ball.pos_x - ball.radius, ball.pos_y - ball.radius,
                                  ball.radius * 2, ball.radius * 2))

        ## AI ##
        monster_img = monster.update(delta_time).convert_alpha()

        # SOUND RADIUS #
        for sound_radius in sound_radius_list :
            remove_bool, collide_rect = sound_radius.update(delta_time)

            # REMOVES SOUND RADIUS FROM LIST #
            if remove_bool == True :
                sound_radius_list.remove(sound_radius)
                continue

            # COLLISION WITH MONSTER #
            if collide_rect.colliderect(monster.rect) and monster.stun_var <= 0 :
                monster.find_target(sound_radius.tile)

        ## EVENT HANDLER ##
        for event in pygame.event.get() :
            # QUIT EVENT #
            if event.type == pygame.QUIT :
                running = False

            ## KEYBOARD ONE-PRESS INPUT ##
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    running = False

                # SPEED CONTROL #
                if event.key == pygame.K_LSHIFT and stamina_recharge <= 0 :
                    move_speed = 300
                    it_speed = 3
                    sprinting_bool = True

                # INVENTORY SELECTION #
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3 :
                    inv_color1 = brown
                    inv_color2 = brown
                    inv_color3 = brown

                    if event.key == pygame.K_1 :
                        inv_color1 = grey

                    elif event.key == pygame.K_2 :
                        inv_color2 = grey

                    elif event.key == pygame.K_3 :
                        inv_color3 = grey

                # INVENTORY USE #
                if event.key == pygame.K_e and inventory_int is not None :
                    try :
                        inventory[inventory_int]
                        temp_bool = True

                    except IndexError :
                        temp_bool = False

                    if temp_bool == True :
                        item = inventory[inventory_int][0]

                        if item.class_type > 2 :
                            inventory.pop(inventory_int)

                            # HAMMER ITEM #
                            if item.class_type == 3 :
                                # GENERATES SOUND #
                                item_use_sfx.play(hammer_sou)
                                sound_radius_list.append(classes.sound_generation((pcol_x, pcol_y),
                                                                                  300, player_tile))

                                # SETS TILES ADJACENT TO PLAYER #
                                add_x = -1
                                add_y = -1
                                adj_list = []

                                while add_y < 2 :
                                    adj_list.append(tiles[player_tile.grid_y + add_y][player_tile.grid_x + add_x])

                                    add_x += 1
                                    if add_x > 1 :
                                        add_x = -1
                                        add_y += 1

                                # IF ANY ADJACENT TILES ARE CRACKED, REMOVES THEM #
                                for tile in adj_list :
                                    if tile.crack == True :
                                        walls.remove(tile)
                                        tiles[tile.grid_y][tile.grid_x].valid = True
                                        tile.crack = False
                                        removed_mask.append((tile.x, tile.y))

                            if item.class_type == 4 :
                                # GENERATES SOUND #
                                item_use_sfx.play(taser_sou)

                                # CREATES STUN BALL #
                                stun_balls.append(item.use(sam_y / 64, player_rect))

                            if item.class_type == 5 :
                                stunned = 0

                    inventory_int = None
                    inv_color1 = brown
                    inv_color2 = brown
                    inv_color3 = brown

                # INVENTORY DROP #
                if event.key == pygame.K_g :
                    try :
                        inventory[inventory_int]
                        temp_bool = True

                    except IndexError :
                        temp_bool = False

                    if temp_bool == True :
                        # DICTATES FACING #
                        if sam_y == 0 :
                            mul = (0, -2)

                        elif sam_y == 64 :
                            mul = (0, 1)

                        elif sam_y == 128 :
                            mul = (1, 0)

                        elif sam_y == 192 :
                            mul = (-1.5, 0)

                        # ACTUALLY DROPS ITEM #
                        entities.append(classes.StaticEntity((pcol_x + (entity.image.get_width() * mul[0]), pcol_y +
                                                              entity.image.get_height() * mul[1]),
                                                             inventory[inventory_int][0].class_type,
                                                             inventory[inventory_int][0].name,
                                                             inventory[inventory_int][0].image, tiles))

                        # REMOVES ITEM FROM LIST #
                        inventory.pop(inventory_int)

                    inventory_int = None
                    inv_color1 = brown
                    inv_color2 = brown

                ## DEBUG COMMANDS ##

                # ENABLE/DISABLE DEBUG #
                if event.key == pygame.K_F1:
                    debug = not debug

                if debug == True :
                    # CHANGES TARGET TILE #
                    if event.key == pygame.K_RIGHT :
                        targ_x += 1

                    if event.key == pygame.K_LEFT :
                        targ_x -= 1

                    if event.key == pygame.K_DOWN :
                        targ_y += 1

                    if event.key == pygame.K_UP :
                        targ_y -= 1

                    # RETURNS PATH FROM PLAYER-TARGET #
                    if event.key == pygame.K_SPACE :
                        if targ_tile.valid == True :
                            move_list = pathfinder.pather(player_tile, targ_tile, tiles)

                    # SETS A TARGET PATH TO MONSTER #
                    if event.key == pygame.K_LALT :
                        monster.find_target(targ_tile)

                    # TELEPORTS PLAYER TO TARGET TILE #
                    if event.key == pygame.K_LCTRL :
                        player_x, player_y = targ_tile.x, targ_tile.y

                    # PRINTS PLAYER POSITION #
                    if event.key == pygame.K_F2 :
                        print(f"PLAYER POS: ({player_tile.grid_x}, {player_tile.grid_y})")

                    # PRINTS DISTANCE FROM PLAYER-TARGET #
                    if event.key == pygame.K_F3 :
                        print(f"PLAYER-TARGET DIST: {classes.pathfinder.calc_dest(pathfinder, player_tile, targ_tile)}")

            ## KEYBOARD ONE-UP INPUT ##
            if event.type == pygame.KEYUP :
                # RESETS MOVE SPEED #
                if event.key == pygame.K_LSHIFT :
                    move_speed = 100
                    it_speed = 1
                    sprinting_bool = False

                # CONTINUED INVENTORY SELECTION #
                if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                    inv_color1 = brown
                    inv_color2 = brown

                    if event.key == pygame.K_1 :
                        if len(inventory) >= 1 :
                            inv_color1 = green
                            inventory_int = 0

                        else :
                            inv_color1 = brown

                    elif event.key == pygame.K_2 :
                        if len(inventory) >= 2 :
                            inv_color2 = green
                            inventory_int = 1

                        else :
                            inv_color2 = brown

                    elif event.key == pygame.K_3 :
                        if len(inventory) >= 3 :
                            inv_color3 = green
                            inventory_int = 2

                        else :
                            inv_color3 = brown

        ## CONTINUOUS KEYBOARD INPUT ##
        keys = pygame.key.get_pressed()

        # BASIC WASD MOVEMENT #
        pre_player_x = player_x
        pre_player_y = player_y
        is_moving = False

        if keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_a] :
            is_moving = True

            if keys[pygame.K_w] :
                player_y -= move_speed * delta_time
                sam_y = 0

            if keys[pygame.K_s] :
                player_y += move_speed * delta_time
                sam_y = 64

            if keys[pygame.K_d] :
                player_x += move_speed * delta_time
                sam_y = 128

            if keys[pygame.K_a] :
                player_x -= move_speed * delta_time
                sam_y = 192

            if stunned > 0 :
                player_x = pre_player_x
                player_y = pre_player_y
                sam_x = 0

        # PLAYER HORIZONTAL ANIMATION #
        if is_moving == True :
            spritesheet_timer -= it_speed * delta_time
            player_step -= it_speed * delta_time

            if spritesheet_timer < 0 :
                sam_x += 1
                spritesheet_timer = float_iterator

                if sam_x > 7 :
                    sam_x = 0

            if player_step < 0 :
                player_sfx.play(small_step_sou)
                player_step = .8

                # SOUND GENERATION #
                if sprinting_bool == True :
                    size_int = 100

                else :
                    size_int = 50

                sound_radius_list.append(classes.sound_generation((pcol_x, pcol_y), size_int, player_tile))


        # RESETS HORIZONTAL ANIMATION #
        elif is_moving == False or sam_y != old_y:
            sam_x = 0
            player_step = .8
            spritesheet_timer = float_iterator

        old_y = sam_y

        # UPDATES CAMERA POSITION #
        camera_x, camera_y = player_x - (win_x / 2), player_y - (win_y / 2)

        # PLAYER BOUNDING #
        if player_x > (map_surf.get_width()) - 43 :
            player_x = (map_surf.get_width()) - 43

        if player_x < -23 :
            player_x = -23

        if player_y > (map_surf.get_height()) - 59 :
            player_y = (map_surf.get_height()) - 59

        if player_y < -14 :
            player_y = -14

        # CAMERA BOUNDING #
        if camera_x > map_surf.get_width() - ((win_x / 2) * 2) :
            camera_x = map_surf.get_width() - ((win_x / 2) * 2)

        if camera_x < 0 :
            camera_x = 0

        if camera_y > map_surf.get_height() - ((win_y / 2) * 2) :
            camera_y = map_surf.get_height() - ((win_y / 2) * 2)

        if camera_y < 0 :
            camera_y = 0

        ## COLLISION ##

        # STATIC ENTITY COLLISION #
        for entity in entities :
            if player_rect.colliderect(entity.collide_rect) :
                # ITEM COLLISION #
                if entity.class_type < 6 :
                    pickup = False

                    ## ON-CONTACT ITEM EFFECTS ##

                    # BACKPACK #
                    if entity.class_type == 2 :
                        # SOUND GENERATION #
                        static_ent_sfx.play(pickup_sou)
                        sound_radius_list.append(classes.sound_generation((pcol_x, pcol_y), 50, player_tile))

                        inventory_ext = True
                        entities.remove(entity)

                    ## NON-CONTACT ITEM EFFECTS ##
                    else :
                        if inventory_ext == False :
                            if len(inventory) < 2 :
                                pickup = True

                        else :
                            if len(inventory) < 3 :
                                pickup = True

                    if pickup == True :
                        # SOUND GENERATION #
                        static_ent_sfx.play(pickup_sou)

                        entities.remove(entity)
                        inventory.append((entity, entity.image))

                # TRAP COLLISION #
                elif entity.class_type < 9 :
                    # ENTITY REMOVAL/SOUND GENERATION #
                    entities.remove(entity)
                    static_ent_sfx.play(trapped_sou)
                    sound_radius_list.append(classes.sound_generation((pcol_x, pcol_y), 500, player_tile))

                    # LOST ITEM #
                    if entity.class_type == 6 :
                        if len(inventory) > 0 :
                            inventory.pop(randint(0, len(inventory) - 1))

                    # BEAR TRAP #
                    if entity.class_type == 7 :
                        stunned = 3

                    # TELEPORTATION TRAP #
                    if entity.class_type == 8 :
                        tile_list = []

                        for row in tiles :
                            for tile in row :
                                if tile.valid == True :
                                    tile_list.append(tile)

                        rand_tile = randint(0, len(tile_list) - 1)
                        player_x, player_y = tile_list[rand_tile].x, tile_list[rand_tile].y

                # DOOR COLLISION #
                if entity.class_type > 8 :
                    # LOOPS THROUGH INVENTORY LOOKING FOR SMALL_KEY #
                    unlock_bool = False
                    for key in inventory :
                        if key[0].class_type == 0 :
                            unlock_bool = True
                            fav_key = key

                    # IF KEYS ARE AVAILABLE, USES A KEY AND UNLOCKS DOOR #
                    if unlock_bool == True :
                        entities.remove(entity)
                        inventory.remove(key)

                        # SETS TILES TO VALID #
                        set_wall_tiles(entity, True)

                        classes.sound_generation((player_x, player_y), 300, player_tile)

                    # IF KEYS ARE NOT AVAILABLE, PLAYS JAMMING SOUND #
                    else :
                        if jam_sound == False :
                            jam_sound = True
                            player_sfx.stop()
                            player_sfx.play(denied_sou)

            # RESETS JAM SOUND IF VALID #
            temp_list = []
            for item in entities :
                if item.class_type > 8 :
                    temp_list.append(item)

            reset_bool = True
            for door in temp_list :
                if player_rect.colliderect(door.collide_rect) :
                    reset_bool = False

            if reset_bool == True :
                jam_sound = False

        # WALL COLLISION #
        for wall in walls :
            # LEFT #
            if pcol_x > wall.x - 6 and pcol_x < wall.x + 32 :
                if pcol_y > wall.y and pcol_y < wall.y + 64 :
                    player_x = wall.x - 38

            # RIGHT #
            if pcol_x < wall.x + 70 and pcol_x > wall.x + 64 :
                if pcol_y > wall.y and pcol_y < wall.y + 64 :
                    player_x = wall.x + 38

            # UP #
            if pcol_x > wall.x and pcol_x < wall.x + 64 :
                if pcol_y > wall.y - 26 and pcol_y < wall.y + 64 :
                    player_y = wall.y - 58

            # DOWN #
            if pcol_x > wall.x and pcol_x < wall.x + 64 :
                if pcol_y > wall.y and pcol_y < wall.y + 81 :
                    player_y = wall.y + 49

        # PLAYER-DOOR COLLISION #
        for door in doors :
            door_rect = pygame.Rect(door.x, door.y, 64, 64)

            if door_rect.colliderect(player_rect) :
                key_bool = False
                for item in inventory :
                    if item[0].class_type == 1 :
                        key_bool = True

                if key_bool == True :
                    game_over(True)

        # MONSTER-PLAYER COLLISION #
        if player_rect.colliderect(monster.rect) :
            game_over()
            running = False

        # MONSTER-BALL COLLISION #
        for ball_rect in ball_rect_list :
            if monster.rect.colliderect(ball_rect) :
                monster.stun_var = 3
                stun_balls.remove(stun_balls[ball_rect_list.index(ball_rect)])

        ## RENDERING ##
        win.fill((255, 255, 255))

        # BLITS MAP #
        win.blit(map_surf, (0, 0), (camera_x, camera_y, win_x, win_y))

        # DRAWS DOORS #
        for door in doors :
            win.blit(door_img, (door.x - camera_x, door.y - camera_y))

        # BLITS CARPET MASKS #
        for carpet in removed_mask :
            win.blit(carpet_img, (carpet[0] - camera_x, carpet[1] - camera_y))

        # BLITS SOUND RADII #
        for sound_radius in sound_radius_list :
            pygame.draw.circle(win, (200, 200, 200, 10), (sound_radius.epicenter[0] - camera_x,
                                                          sound_radius.epicenter[1] - camera_y), sound_radius.cur_size, 1)

        # BLITS PLAYER #
        win.blit(sam, (player_x - camera_x, player_y - camera_y, 64, 64), (sam_x * 64, sam_y, 64, 64))

        # BLITS MONSTER #
        win.blit(monster_img, (monster.pos[0] - camera_x, monster.pos[1] - camera_y, 64, 64))

        # BLITS STATIC ENTITIES #
        for entity in entities :
            if entity.tile.crack == False :
                win.blit(entity.image, (entity.collide_rect[0] - camera_x, entity.collide_rect[1] - camera_y))

        # BLITS STUN BALLS #
        for ball in stun_balls :
            pygame.draw.circle(win, (0, 0, 255), (ball.pos_x - camera_x, ball.pos_y - camera_y), ball.radius, 3)

        ## UI RENDERING ##

        # DRAWS INVENTORY ITEMS #
        pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 5.5), win_y - (win_y / 13), win_x / 20, win_y / 16), 5)
        inv_1 = pygame.draw.rect(win, inv_color1, (win_x - (win_x / 5.5), win_y - (win_y / 13), win_x / 20, win_y / 16))

        pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 8), win_y - (win_y / 13), win_x / 20, win_y / 16), 5)
        inv_2 = pygame.draw.rect(win, inv_color2, (win_x - (win_x / 8), win_y - (win_y / 13), win_x / 20, win_y / 16))

        inv_list = [inv_1, inv_2]

        pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 15), win_y - (win_y / 13), win_x / 20, win_y / 16), 5)
        if inventory_ext == True :
            inv_3 = pygame.draw.rect(win, inv_color3,
                                     (win_x - (win_x / 15), win_y - (win_y / 13), win_x / 20, win_y / 16))
            inv_list.append(inv_3)

        inv_x = 0
        for item in inventory :
            rect = inv_list[inv_x]
            win.blit(item[1], (rect[0], rect[1]))

            inv_x += 1

        # DRAWS STAMINA #
        pygame.draw.rect(win, (0, 0, 0), (win_x / 30, win_y / 40, win_x / 3, win_y / 15))
        pygame.draw.rect(win, stamina_color, (win_x / 25 + (win_x / 50), win_y / 35 + (win_y / 70),
                                              (win_x / 3.14) * (stamina / 100), win_y / 16.5))

        if debug == True:
            ## DEBUG PRINT ##
            pygame.draw.line(win, (0, 0, 255), (pcol_x - camera_x, pcol_y - camera_y),
                             (tiles[targ_y][targ_x].x - camera_x + 32, tiles[targ_y][targ_x].y - camera_y + 32), 5)

            pygame.draw.rect(win, (255, 0, 0), (targ_tile.x - camera_x, targ_tile.y - camera_y, 64, 64), 1)
            pygame.draw.rect(win, (0, 0, 255), (player_tile.x - camera_x, player_tile.y - camera_y, 64, 64), 1)

            for tile in walls :
                pygame.draw.rect(win, (255, 0, 0), (tile.x - camera_x, tile.y - camera_y, 64, 64), 1)

            i = 0
            for tile in move_list:
                pygame.draw.rect(win, (0, 255, 0), (tile.x - camera_x, tile.y - camera_y, 64, 64), 1)
                tile_text = small_text.render(f"N: {str(i)}, S: {str(tile.score)}", True, (0, 255, 0))
                win.blit(tile_text, (tile.x - camera_x, tile.y - camera_y))
                i += 1

            # DRAWS MONSTER VIEW TILES #
            for tile in monster.adj_list :
                pygame.draw.rect(win, (255, 255, 0), (tile.x - camera_x, tile.y - camera_y, 64, 64))

            ## DRAWS HITBOXS ##
            pygame.draw.rect(win, (0, 255, 0), (player_rect[0] - camera_x, player_rect[1] - camera_y,
                                                player_rect[2], player_rect[3]), 1)

            pygame.draw.rect(win, (0, 0, 255), (monster.rect[0] - camera_x, monster.rect[1] - camera_y, 64, 64), 1)

            for entity in entities :
                if entity.class_type < 6 :
                    entity_color = (0, 255, 0)

                else :
                    entity_color = (255, 0, 0)

                pygame.draw.rect(win, entity_color, (entity.collide_rect[0] - camera_x,
                                                    entity.collide_rect[1] - camera_y, entity.collide_rect[2],
                                                    entity.collide_rect[3]), 1)

            for ball_rect in ball_rect_list :
                pygame.draw.rect(win, (255, 255, 0), (ball_rect[0] - camera_x, ball_rect[1] - camera_y,
                                 ball_rect[2], ball_rect[3]), 1)

    ## MAIN MENU SCREEN ##
    elif ui_index == 0 :

        # RESETS NECESSARY VARIABLES #
        hover_int = -1
        button_img_list = [play_uc, options_uc, quit_uc]

        ## MASTER RENDERING ##

        # CLEARS SCREEN #
        win.fill((0, 0, 0))

        # RENDERS BACKGROUND #
        flicker_int = randint(1, 100)
        background_y = 0

        if flicker_int >= 99 :
            background_y = 600

        win.blit(main_menu_background, (0, 0, 800, 600), (0, background_y, 800, 600))

        # UPDATES MOUSE POSITION #
        mos_pos = pygame.mouse.get_pos()

        # MAIN MENU #
        if options_enabled == False :
            ## COLLISION ##
            x = -1
            for rect in button_rect_list :
                x += 1
                if rect.collidepoint(mos_pos) :
                    hover_int = x

                    if select_sound_played == False :
                        ui_sfx.play(select_sou)
                        select_sound_played = True

            if hover_int != -1 :
                button_img_list[hover_int] = pressed_button_list[hover_int]

            else :
                select_sound_played = False

            ## RENDERING ##

            # RENDERS BUTTONS #
            x = 0
            while x < 3 :
                win.blit(button_img_list[x], (button_rect_list[x][0], button_rect_list[x][1]))
                x += 1

        # OPTIONS MENU #
        else :
            ## COLLISION ##
            if back_rect.collidepoint(mos_pos) :
                back_image = back_c
                hover_int = 0

                if select_sound_played == False:
                    ui_sfx.play(select_sou)
                    select_sound_played = True

            else :
                back_image = back_uc
                select_sound_played = False

            # RENDERING #

            # RENDERS BACK SLIDER #
            pygame.draw.rect(win, (255, 255, 255), slider_back)

            # RENDERS VOLUME INFO SLIDER #
            pygame.draw.rect(win, (255, 0, 0), (slider_back[0], slider_back[1], slider_back[2] * mas_audio,
                                                slider_back[3]))

            # RENDERS VOLUME INFO TEXT #
            vol_txt = big_text.render(str(f"{int(mas_audio * 100)}%"), True, (255, 255, 0))
            win.blit(vol_txt, (slider_back[0] + slider_back[2] + (win_x / 20), slider_back[1] - (win_y / 120)))

            # RENDERS BACK BUTTON #
            win.blit(back_image, back_rect)

        ## EVENT HANDLER ##
        for event in pygame.event.get():
            ## QUIT EVENT ##
            if event.type == pygame.QUIT:
                running = False

            ## ONE-PRESS KEYBOARD INPUT ##
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

            ## ONE-PRESS MOUSE INPUT ##
            if event.type == pygame.MOUSEBUTTONDOWN:
                # MAIN MENU BUTTON PRESSES #
                if event.button == 1 and hover_int != -1  :
                    if options_enabled == False :
                        # STARTS GAME #
                        if hover_int == 0:
                            ui_index = None
                            main_menu_cha.fadeout(5000)
                            amb_cha.set_volume(mas_audio / 20)
                            ui_sfx.play(transition_sou)

                        # GOES TO OPTIONS MENU #
                        elif hover_int == 1:
                            options_enabled = True

                        # QUITS GAME #
                        elif hover_int == 2:
                            running = False

                    elif options_enabled == True :
                        # GOES BACK TO MAIN MENU #
                        if hover_int == 0 :
                            options_enabled = False

            ## CONTINUOUS INPUT ##

            # MOUSE INPUT #
            mouse_keys = pygame.mouse.get_pressed()

            # OPTIONS SLIDER INPUT #
            if mouse_keys[0] == True and options_enabled == True :
                if mos_pos[1] > slider_back[1] and mos_pos[1] < slider_back[1] + slider_back[3] :
                    mas_audio = (mos_pos[0] - slider_back[0]) / slider_back[2]
                    update_audio()

                    # BOUNDS MASTER AUDIO #
                    if mas_audio > 1 :
                        mas_audio = 1

                    elif mas_audio < 0 :
                        mas_audio = 0

    pygame.display.flip()

# QUITS GAME #
pygame.quit()
