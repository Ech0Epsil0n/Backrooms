## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

### IMPORTS AND INITIALIZATIONS ###
import pygame
from pygame import mixer

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
big_font = pygame.font.SysFont("Arial", 24)
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
inventory_int = None

pathfinder = classes.pathfinder()
move_list = []

debug = False

## VIDEO INITIALIZATION ##
win.blit(preload_surf("Loading Video Assets..."), (0, 0))
pygame.display.flip()

# LOAD IMAGES #

# GAMEPLAY IMAGES #
sam = pygame.image.load("Assets//Video//player_ss.png")

# MAIN MENU IMAGES #
main_menu_background = pygame.image.load("Assets//Video//Main Menu//main menu.png")

play_uc = pygame.image.load("Assets//Video//Main Menu//play_unclicked.png")
play_c = pygame.image.load("Assets//Video//Main Menu//play_clicked.png")

options_uc = pygame.image.load("Assets//Video//Main Menu//options_unclicked.png")
options_c = pygame.image.load("Assets//Video//Main Menu//options_clicked.png")

quit_uc = pygame.image.load("Assets//Video//Main Menu//quit_unclicked.png")
quit_c = pygame.image.load("Assets//Video//Main Menu//quit_clicked.png")

# SPRITESHEET ITERATORS #
sam_y = 0
sam_x = 0

it_speed = 1
float_iterator = 0.25

spritesheet_timer = float_iterator

# LIST INITIALIZATION #
entities = []
inventory = []

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
sfx_list = [ui_sfx, player_sfx, monster_scream, monster_sfx]

# LOADS AUDIO-FILES #

# MUSIC #
menu_light_sou = mixer.Sound("Assets//Audio//menu_light.mp3")
menu_harsh_sou = mixer.Sound("Assets//Audio//menu_harsh.mp3")

# SOUND EFFECTS #
buzz_sou = mixer.Sound("Assets//Audio//buzz.mp3")
select_sou = mixer.Sound("Assets//Audio//SFX//select.wav")
transition_sou = mixer.Sound("Assets//Audio//SFX//transition.wav")
small_step_sou = mixer.Sound("Assets//Audio//SFX//small_step.wav")
big_step_sou = mixer.Sound("Assets//Audio//SFX//big_step.wav")
high_scream_sou = mixer.Sound("Assets//Audio//SFX//mon_scream_high.mp3")

# SETS MASTER AUDIO LEVEL #
mas_audio = 1

win.blit(preload_surf("Initializing UI..."), (0, 0))
pygame.display.flip()

# CREATES AUDIO-RELATED VARIABLES #
player_step = 1

## UI INITIALIZATION ##
ui_index = 0

win.blit(preload_surf("Loading Classes..."), (0, 0))
pygame.display.flip()

## CLASS DEFINITION ##
class Monster :
    """The main monster entity. Has pathfinding, player detection, sound detection, and controls Monster
    animation and movement."""

    def __init__(self, start_pos, patrol_list=None) :
        self.pos = list(start_pos)
        self.move_speed = 300
        self.monster_ss = pygame.image.load("Assets//Video//monster_ss.png").convert_alpha()
        self.target_list = []
        self.walked_list = []
        self.target_pos = None
        self.mas_target = None

    def find_target(self, call_tile) :
        """Finds the target list to the tile that called this function."""

        if self.mas_target is None :
            self.mas_target = call_tile
            self.walked_list = []

        # FINDS PLAYER TILE #
        for row in tiles :
            for tile in row :
                tile_rect = pygame.Rect(tile.x, tile.y, 64, 64)

                if tile_rect.collidepoint(monster.pos[0] + 32, monster.pos[1] + 32) :
                    start_tile = tile
                    self.walked_list.append(start_tile)


        self.target_list = pathfinder.pather(start_tile, self.mas_target, tiles, self)

        return

    def update(self, delta_time) :
        """Moves Monster towards a target position if one is available. Changes face to more accurately represent
        movement."""

        ss = 1

        if len(self.target_list) != 0 :
            self.target_pos = (self.target_list[0].x, self.target_list[0].y)

            if self.target_pos is not None:
                target_x, target_y = self.target_pos[0], self.target_pos[1]
                move_x, move_y = 0, 0

                # MOVE RIGHT #
                if self.pos[0] <= target_x :
                    move_x += move_speed
                    ss_x = 2

                # MOVE LEFT #
                elif self.pos[0] > target_x :
                    move_x -= move_speed
                    ss_x = 3

                # MOVE UP #
                if self.pos[1] >= target_y :
                    move_y -= move_speed
                    ss_y = 0

                # MOVE DOWN #
                elif self.pos[1] < target_y :
                    move_y += move_speed
                    ss_y = 1

                # CALCULATES DISTANCE TO TARGET #
                diff_x, diff_y = target_x - self.pos[0], target_y - self.pos[1]

                # SETS DISTANCE TO ABSOLUTE VALUE #
                if diff_x < 0 :
                    diff_x *= -1

                if diff_y < 0 :
                    diff_y *= -1

                # APPLIES MOVEMENT #
                if diff_x > diff_y :
                    self.pos[0] += move_x * delta_time
                    ss = ss_x

                if diff_y > diff_x :
                    self.pos[1] += move_y * delta_time
                    ss = ss_y

                # IF CLOSE ENOUGH TO TARGET, REMOVES TARGET #
                if diff_x < 3 and diff_y < 3 :
                    self.target_list.pop(0)
                    monster_sfx.play(big_step_sou)

                    if len(self.target_list) != 0 :
                        self.find_target(self.mas_target)

                    else :
                        self.mas_target = None

        # RETURNS WORK SURFACE WITH MONSTER #
        work_surf = pygame.Surface((64, 64)).convert_alpha()
        work_surf.fill((0, 0, 0, 0))
        work_surf.blit(self.monster_ss, (0, 0), (0, ss * 64, 64, 64))

        return work_surf.convert_alpha()

# MAIN MENU INITIALIZATION #

# ESTABLISHES NECESSARY VARIABLES #
button_width, button_height = play_c.get_width(), play_c.get_height()
print(play_c.get_width())
select_sound_played = False

# CREATES RECTS OF ALL BUTTONS #
#play_rect = pygame.Rect(button_width * .055, win_y - (button_height + (button_height / )), button_width, button_height)
play_rect = pygame.Rect(352, 393, 102, 78)
#options_rect = pygame.Rect(button_width * 1.5, win_y - (button_height + (button_height / 2)), button_width, button_height)
options_rect = pygame.Rect(281, 480, 234, 99)
quit_rect = pygame.Rect(button_width * 2.75, win_y - (button_height + (button_height / 2)), button_width, button_height)

# CREATES STATIC LISTS FOR DATA REFERENCE #
button_rect_list = [play_rect, options_rect, quit_rect]
pressed_button_list = [play_c, options_c, quit_c]

win.blit(preload_surf("Generating Map..."), (0, 0))
pygame.display.flip()

## MAP GENERATION ##
map_loader = 2
map_surf, objects, tiles, walls = map_reader.load_map(map_loader)

## MONSTER GENERATION ##
mons_start_pos = [(64, 64), (148, 64), (192, 64)]
monster = Monster(mons_start_pos[map_loader])

## PLAYER GENERATION ##
player_start_pos = [(576, 900), (128, 64), (704, 800)]
player_x, player_y = player_start_pos[map_loader][0], player_start_pos[map_loader][1]

## STATIC ENTITY GENERATION ##
for object in objects :
    entities.append(classes.StaticEntity((object[0], object[1]), object[2], object[3]))

### POST-INITIALIZATION ###

# PLAYS INITIAL AUDIO CONFIGURATION #
main_menu_cha.play(menu_light_sou, -1)

amb_cha.set_volume((mas_audio + 0.001) * .15)
amb_cha.play(buzz_sou, -1)

for cha in sfx_list :
    cha.set_volume((mas_audio + 0.001) * 0.4)

## MAIN GAMEPLAY LOOP ##
while running :
    # TIME CONTROL #
    delta_time = clock.tick() / 1000

    ## GAMEPLAY ##
    if ui_index is None :
        ## UPDATE ##
        player_rect = pygame.Rect((player_x - camera_x) + 20, (player_y - camera_y) + 15, 23, 44)
        pcol_x, pcol_y = player_x + 32, player_y + 32

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
            stamina -= 25 * delta_time

        if stamina <= 0 :
            sprinting_bool = False
            stamina_recharge = 3
            move_speed = 100
            stamina_color = (255, 0, 0)

        if stamina_recharge <= 0 and stamina_color != (0, 255, 0) :
            stamina_color = (0, 255, 0)

        if stamina > 100 :
            stamina = 100

        elif stamina <= 0 :
            stamina = 0

        ## AI ##
        monster_img = monster.update(delta_time).convert_alpha()

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
                if event.key == pygame.K_1 or event.key == pygame.K_2 :
                    inv_color1 = brown
                    inv_color2 = brown

                    if event.key == pygame.K_1 :
                        inv_color1 = grey

                    elif event.key == pygame.K_2 :
                        inv_color2 = grey

                # INVENTORY USE #
                if event.key == pygame.K_e and inventory_int is not None :
                    try :
                        inventory[inventory_int]
                        temp_bool = True

                    except IndexError :
                        temp_bool = False

                    if temp_bool == True :
                        inventory[inventory_int][0].use()
                        inventory.pop(inventory_int)

                    inventory_int = None
                    inv_color1 = brown
                    inv_color2 = brown

                # INVENTORY DROP #
                if event.key == pygame.K_g :
                    try :
                        inventory[inventory_int]
                        temp_bool = True

                    except IndexError :
                        temp_bool = False

                    if temp_bool == True :
                        entities.append(classes.StaticEntity((player_x - 20, player_y + 32),
                                        inventory[inventory_int][0].class_type, inventory[inventory_int][0].name))

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
                        monster_scream.play(high_scream_sou)

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
                if event.key == pygame.K_1 or event.key == pygame.K_2 :
                    inv_color1 = brown
                    inv_color2 = brown

                    if event.key == pygame.K_1 :
                        inv_color1 = green
                        inventory_int = 0

                    elif event.key == pygame.K_2 :
                        inv_color2 = green
                        inventory_int = 1

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

        # PLAYER HORIZONTAL ANIMATION #
        if is_moving == True :
            spritesheet_timer -= it_speed * delta_time
            player_step -= it_speed * delta_time

            if spritesheet_timer < 0 :
                sam_x += 1
                spritesheet_timer = float_iterator

                if sam_x > 2 :
                    sam_x = 0

            if player_step < 0 :
                player_sfx.play(small_step_sou)
                player_step = .8

        # RESETS HORIZONTAL ANIMATION #
        else :
            sam_x = 0
            player_step = .8
            spritesheet_timer = float_iterator

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
            entity.entity_surf, entity.entity_x, entity.entity_y = entity.update(camera_x, camera_y)

            if player_rect.colliderect(entity.collide_rect) :
                if len(inventory) < 2 and entity.class_type < 10 :
                    entities.remove(entity)
                    inventory.append((entity, item_font.render(entity.name, True, (255, 255, 255))))

                if entity.class_type >= 10 and entity.class_type < 20 :
                    print(f"YOU'VE BEEN HIT BY A {entity.name.upper()}!")
                    entities.remove(entity)
                    stunned = 3

                if entity.class_type == 20 :
                    print("YOU'RE A WINNER!")
                    entities.remove(entity)

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
                    player_y = wall.y + 50

        ## RENDERING ##
        win.fill((255, 255, 255))

        # BLITS MAP #
        win.blit(map_surf, (0, 0), (camera_x, camera_y, win_x, win_y))

        # BLITS PLAYER #
        win.blit(sam, (player_x - camera_x, player_y - camera_y, 64, 64), (sam_x * 64, sam_y, 64, 64))

        # BLITS MONSTER #
        win.blit(monster_img, (monster.pos[0] - camera_x, monster.pos[1] - camera_y, 64, 64))

        # BLITS ITEMS #
        for entity in entities :
            win.blit(entity.entity_surf, (entity.entity_x, entity.entity_y))

        ## UI RENDERING ##

        # DRAWS INVENTORY ITEMS #
        pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 8), win_y - (win_y / 13), win_x / 20, win_y / 16), 5)
        pygame.draw.rect(win, inv_color1, (win_x - (win_x / 8), win_y - (win_y / 13), win_x / 20, win_y / 16))

        pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 15), win_y - (win_y / 13), win_x / 20, win_y / 16), 5)
        pygame.draw.rect(win, inv_color2, (win_x - (win_x / 15), win_y - (win_y / 13), win_x / 20, win_y / 16))

        if len(inventory) >= 1 :
            win.blit(inventory[0][1], ((win_x - (win_x / 5.6)) + ((win_x / 13) / 10),
                                       win_y - ((win_y / 10) + ((win_y / 10) / 8))))

            if len(inventory) == 2:
                win.blit(inventory[1][1], ((win_x - (win_x / 10)) + ((win_x / 13) / 10),
                                           win_y - ((win_y / 10) + ((win_y / 10) / 8))))

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
                pygame.draw.rect(win, (0, 0, 0), (tile.x - camera_x, tile.y - camera_y, 64, 64), 1)

            i = 0
            for tile in move_list:
                pygame.draw.rect(win, (0, 255, 0), (tile.x - camera_x, tile.y - camera_y, 64, 64), 1)
                tile_text = small_text.render(f"N: {str(i)}, S: {str(tile.score)}", True, (0, 255, 0))
                win.blit(tile_text, (tile.x - camera_x, tile.y - camera_y))
                i += 1

            ## DRAWS MONSTER HITBOX ##
            pygame.draw.rect(win, (0, 0, 255), (monster.pos[0] - camera_x, monster.pos[1] - camera_y, 64, 64), 1)

    ## MAIN MENU SCREEN ##
    elif ui_index == 0 :
        ## UPDATE ##

        # RESETS NECESSARY VARIABLES #
        hover_int = -1
        button_img_list = [play_uc, options_uc, quit_uc]

        # UPDATES MOUSE POSITION #
        mos_pos = pygame.mouse.get_pos()

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

        ## EVENT HANDLER ##
        for event in pygame.event.get() :
            ## QUIT EVENT ##
            if event.type == pygame.QUIT :
                running = False

            ## ONE-PRESS KEYBOARD INPUT ##
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_ESCAPE :
                    running = False

            ## ONE-PRESS MOUSE INPUT ##
            if event.type == pygame.MOUSEBUTTONDOWN :
                # WILL ENACT THE OPERATION FROM A BUTTON IF ONE IS HOVERED OVER #
                if event.button == 1 and hover_int != -1 :
                    # STARTS GAME #
                    if hover_int == 0 :
                        ui_index = None
                        main_menu_cha.fadeout(5000)
                        amb_cha.fadeout(3000)
                        ui_sfx.play(transition_sou)

                    # GOES TO OPTIONS MENU #
                    elif hover_int == 1 :
                        print("OPTIONS MENU")

                    # QUITS GAME #
                    elif hover_int == 2 :
                        running = False

        ## RENDERING ##

        # RENDERS BACKGROUND #
        win.blit(main_menu_background, (0, 0))

        # RENDERS BUTTONS #
        x = 0
        while x < 3 :
            win.blit(button_img_list[x], (button_rect_list[x][0], button_rect_list[x][1]))
            x += 1

    pygame.display.flip()

# QUITS GAME #
pygame.quit()
quit()
