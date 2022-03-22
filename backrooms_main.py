## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

## IMPORTS AND INITIALIZATIONS ##
import pygame
from items_file import Item

# Pygame standard initialization.
pygame.init()
win_x, win_y = 800, 600
win = pygame.display.set_mode((win_x, win_y))
pygame.display.set_caption("Into the Backrooms")
clock = pygame.time.Clock
clock = pygame.time.Clock()
running = True

# Establishes baseline variables.
move_speed = 100
player_x, player_y = 0, 0

# Loads assets.
map_test = pygame.image.load("Backrooms assets\\Map_layout.png")

# Creates map surface to blit/transform.
map_surf = pygame.Surface((int(map_test.get_width()), int(map_test.get_height())))
map_surf.blit(map_test, (0, 0))
map_surf = pygame.transform.scale(map_surf, (win_x * 2, win_y * 2))

# Generates items (temporary: will be relocated to map_generator script)
test_hammer = Item(0, (1515 - player_x, 625 - player_y))

## MAIN GAMEPLAY LOOP ##
while running :
    # Time control.
    delta_time = clock.tick() / 1000

    ## EVENT HANDLER ##
    for event in pygame.event.get() :
        ## KEYBOARD ONE-PRESS INPUT ##
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                running = False

            # Speed control using shift/control.
            if event.key == pygame.K_LSHIFT :
                move_speed = 300

            elif event.key == pygame.K_LCTRL :
                move_speed = 25

        ## KEYBOARD ONE-UP INPUT ##
        if event.type == pygame.KEYUP :
            # Resets move speed.
            if event.key == pygame.K_LSHIFT or pygame.key == pygame.K_LCTRL :
                move_speed = 100

    ## CONTINUOUS KEYBOARD INPUT ##
    keys = pygame.key.get_pressed()

    # Basic WASD movement.
    if keys[pygame.K_w] :
        player_y -= move_speed * delta_time

    if keys[pygame.K_s] :
        player_y += move_speed * delta_time

    if keys[pygame.K_d] :
        player_x += move_speed * delta_time

    if keys[pygame.K_a] :
        player_x -= move_speed * delta_time

    ## RENDERING ##
    win.fill((0, 0, 0))

    # Blits map.
    win.blit(map_surf, (0 - player_x, 0 - player_y))

    # Draws player.
    pygame.draw.circle(win, (0, 0, 0), (win_x / 2, win_y / 2), 20)

    # Draws enemies.
    enemy_surf, enemy_x, enemy_y = test_hammer.update(player_x, player_y)
    win.blit(enemy_surf, (enemy_x, enemy_y))

    # Finalizes render.
    pygame.display.flip()

# If running is set to False, runs this code.
pygame.quit()