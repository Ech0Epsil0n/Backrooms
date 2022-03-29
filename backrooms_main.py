## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

## IMPORTS AND INITIALIZATIONS ##
import pygame
import classes
import time

# Pygame standard initialization.
import map_reader

pygame.init()
win_x, win_y = 800, 600
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Into the Backrooms")
clock = pygame.time.Clock()
running = True

# Establishes baseline variables.
move_speed = 100
stunned = 0
camera_x, camera_y = 0, 0
sprinting_bool = False
end_game = False
stamina = 100
stamina_recharge = 0
stamina_color = (0, 255, 0)
inv_color1 = (101, 67, 33)
inv_color2 = (101, 67, 33)

# Creates fonts and renders static text.
item_font = pygame.font.SysFont("Times New Roman", 18)
big_font = pygame.font.SysFont("Times New Roman", 48)

# Loads assets.
map_test = pygame.image.load("Assets//Map_layout.png")
sam = pygame.image.load("Assets//sliding_sam.png")

# Image integers for iterating through spritesheets.
sam_y = 0

# Loads items and inventory lists.
entities = []
inventory = []

# Renders current map and creates static entity list.
map_surf, objects, tiles = map_reader.load_map(0)
start_pos = [(576, 1000), (128, 128)]

player_x, player_y = start_pos[0][0], start_pos[0][1]

for object in objects :
    entities.append(classes.StaticEntity((object[0], object[1]), object[2], object[3]))

# Prepares game end screen.
end_game_surf = pygame.Surface((win_x, win_y))
victory_text = big_font.render("VICTORY!", True, (255, 255, 255))
quit_text = big_font.render("QUIT?", True, (0, 255, 0))

## MAIN GAMEPLAY LOOP ##
while running :
    # Time control.
    delta_time = clock.tick() / 1000

    ## UPDATE ##
    player_rect = pygame.Rect((player_x - camera_x) + 20, (player_y - camera_y) + 15, 23, 44)

    stamina_recharge -= 1 * delta_time
    stunned -= 1 * delta_time

    # Handles stamina generation, depletion, and elimination.
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

    # Sprint bounding.
    if stamina > 100 :
        stamina = 100

    elif stamina <= 0 :
        stamina = 0

    ## EVENT HANDLER ##
    for event in pygame.event.get() :
        ## KEYBOARD ONE-PRESS INPUT ##
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                running = False

            # Speed control using shift/control.
            if event.key == pygame.K_LSHIFT and stamina_recharge <= 0 :
                move_speed = 300
                sprinting_bool = True

            elif event.key == pygame.K_LCTRL :
                move_speed = 25

            elif event.key == pygame.K_F1 :
                end_game = True

        ## KEYBOARD ONE-UP INPUT ##
        if event.type == pygame.KEYUP :
            # Resets move speed.
            if event.key == pygame.K_LSHIFT or pygame.key == pygame.K_LCTRL :
                move_speed = 100
                sprinting_bool = False

        ## MOUSE ONE-PRESS INPUT ##
        if event.type == pygame.MOUSEBUTTONDOWN :
            if end_game == True :
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.collidepoint(mouse_pos[0], mouse_pos[1]) :
                    running = False

    ## CONTINUOUS KEYBOARD INPUT ##
    keys = pygame.key.get_pressed()

    # Basic WASD movement.
    pre_player_x = player_x
    pre_player_y = player_y

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

    # Updates camera positional values.
    camera_x, camera_y = player_x - (win_x / 2), player_y - (win_y / 2)

    # Player bounding.
    if player_x > (map_surf.get_width()) - 43 :
        player_x = (map_surf.get_width()) - 43

    if player_x < -23 :
        player_x = -23

    if player_y > (map_surf.get_height()) - 59 :
        player_y = (map_surf.get_height()) - 59

    if player_y < -14 :
        player_y = -14

    # Camera bounding.
    if camera_x > map_surf.get_width() - ((win_x / 2) * 2) :
        camera_x = map_surf.get_width() - ((win_x / 2) * 2)

    if camera_x < 0 :
        camera_x = 0

    if camera_y > map_surf.get_height() - ((win_y / 2) * 2) :
        camera_y = map_surf.get_height() - ((win_y / 2) * 2)

    if camera_y < 0 :
        camera_y = 0

    ## COLLISION ##

    # Checks for static entity collision and acts accordingly.
    for entity in entities:
        entity.entity_surf, entity.entity_x, entity.entity_y = entity.update(camera_x, camera_y, player_rect)

        if player_rect.colliderect(entity.collide_rect) :
            if len(inventory) < 2 and entity.class_type < 10 :
                entities.remove(entity)
                inventory.append((entity, item_font.render(entity.name, True, (255, 255, 255))))

            if entity.class_type >= 10 and entity.class_type < 20 :
                print(f"YOU'VE BEEN HIT BY A {entity.name.upper()}!")
                entities.remove(entity)
                stunned = 3

            if entity.class_type == 20 :
                end_game = True
                print("Hit DOOR")
                entities.remove(entity)

    ## RENDERING ##
    win.fill((255, 255, 255))

    # Blits map.
    win.blit(map_surf, (0, 0), (camera_x, camera_y, win_x, win_y))

    # Draws player.
    win.blit(sam, (player_x - camera_x, player_y - camera_y, 64, 64), (0, sam_y, 64, 64))

    # Draws player hitbox.
    pygame.draw.rect(win, (255, 0, 0), player_rect, 1)

    # Checks for wall collisions to all walls within a reasonable range.
    for tile in tiles :
        dist_x = tile.pos[0] - (player_x + 20)
        dist_y = tile.pos[1] - (player_y + 20)
        pygame.draw.circle(win, (0, 255, 0), ((player_x + 20) - camera_x, (player_y + 20) - camera_y), 10, 1)

        # Sets distance to absolute value.
        if dist_x < 0 :
            dist_x = -dist_x

        if dist_y < 0 :
            dist_y = -dist_y

        if dist_x < 30 and dist_y < 30 :
            pygame.draw.line(win, (0, 255, 0), ((player_x + 20) - camera_x, (player_y + 20) - camera_y),
                             (tile.col_pos[0] - camera_x, tile.col_pos[1] - camera_y))

            collision_bool, new_player_pos = tile.check((player_x, player_y), (camera_x, camera_y), win)

            if collision_bool == True :
                player_x = new_player_pos[0]
                player_y = new_player_pos[1]

    # Draws items.
    for entity in entities :
        win.blit(entity.entity_surf, (entity.entity_x, entity.entity_y))

    ## UI RENDERING ##

    # Draws inventory item containers.
    # Outlines.
    pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 5.5), win_y - (win_y / 7), win_x / 13, win_y / 10), 5)
    pygame.draw.rect(win, (0, 0, 0), (win_x - (win_x / 10), win_y - (win_y / 7), win_x / 13, win_y / 10), 5)

    # Containers proper.
    pygame.draw.rect(win, inv_color1, (win_x - (win_x / 5.5), win_y - (win_y / 7), win_x / 13, win_y / 10))
    pygame.draw.rect(win, inv_color2, (win_x - (win_x / 10), win_y - (win_y / 7), win_x / 13, win_y / 10))


    if len(inventory) == 1 :
        win.blit(inventory[0][1], ((win_x - (win_x / 5.6)) + ((win_x / 13) / 10),
                                   win_y - ((win_y / 10) + ((win_y / 10) / 8))))

    elif len(inventory) == 2:
        win.blit(inventory[0][1], ((win_x - (win_x / 5.6)) + ((win_x / 13) / 10),
                                   win_y - ((win_y / 10) + ((win_y / 10) / 8))))
        win.blit(inventory[1][1], ((win_x - (win_x / 10)) + ((win_x / 13) / 10),
                                   win_y - ((win_y / 10) + ((win_y / 10) / 8))))
    # Draws stamina bar.
    pygame.draw.rect(win, (0, 0, 0), (win_x / 30, win_y / 40, win_x / 3, win_y / 15))
    pygame.draw.rect(win, stamina_color, (win_x / 25, win_y / 35, (win_x / 3.14) * (stamina / 100), win_y / 16.5))

    # Draws end game screen.
    if end_game == True :
        end_game_surf.blit(victory_text, (win_x / 3, win_y / 20))
        end_game_surf.blit(quit_text, (win_x / 3 + (win_x / 12), win_y / 3 + (win_x / 12)))
        quit_button = pygame.draw.rect(end_game_surf, (255, 0, 0), (win_x / 3, win_y / 3, win_x / 3, win_y / 3), 10)
        win.blit(end_game_surf, (0, 0))

    pygame.display.flip()

# If running is set to False, runs this code.
pygame.quit()
