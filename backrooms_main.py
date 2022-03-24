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
player_size = 20
sprinting_bool = False
stamina = 100
stamina_recharge = 0

# Loads assets.
map_test = pygame.image.load("Backrooms assets//Map_layout.png")

# Creates map surface to blit/transform.
map_surf = pygame.Surface((int(map_test.get_width()), int(map_test.get_height())))
map_surf.blit(map_test, (0, 0))
map_surf = pygame.transform.scale(map_surf, (win_x * 2, win_y * 2))

# Generates items (temporary: will be relocated to map_generator script)
items = []
inventory = []

# Test code.
test_hammer = Item(0, (1526 - player_x, 645 - player_y), "Hammer", (0, 255, 0))
test_bozo = Item(0, (300 - player_x, 300 - player_y), "Bozo", (255, 255, 0))
items.append(test_hammer)
items.append(test_bozo)

## MAIN GAMEPLAY LOOP ##
while running :
    # Time control.
    delta_time = clock.tick() / 1000

    ## UPDATE ##
    player_rect = pygame.Rect((win_x / 2) - 20, (win_y / 2) - 20, 40, 40)
    stamina_recharge -= 1 * delta_time

    # Handles stamina generation, depletion, and elimination.
    if sprinting_bool == False :
        stamina += 10 * delta_time

    else :
        stamina -= 25 * delta_time

    if stamina <= 0 :
        sprinting_bool = False
        stamina_recharge = 3
        move_speed = 100

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

            # Item pickup command.
            if event.key == pygame.K_e :
                for item in items :
                    if player_rect.colliderect(item.collide_rect) :
                        items.remove(item)
                        inventory.append(item)
                        print(inventory)

        ## KEYBOARD ONE-UP INPUT ##
        if event.type == pygame.KEYUP :
            # Resets move speed.
            if event.key == pygame.K_LSHIFT or pygame.key == pygame.K_LCTRL :
                move_speed = 100
                sprinting_bool = False

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
    pygame.draw.circle(win, (0, 0, 0), (win_x / 2, win_y / 2), player_size)

    # Draws items.
    for item in items :
        item_surf, item_x, item_y = item.update(player_x, player_y, player_rect)
        win.blit(item_surf, (item_x, item_y))

    # Temp Code
    pygame.draw.rect(win, (255, 0, 0), player_rect, 1)

    pygame.display.flip()

# If running is set to False, runs this code.
pygame.quit()
