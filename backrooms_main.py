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
player_x, player_y = 800, 1150
player_size = 20
camera_x, camera_y = 0, 0
sprinting_bool = False
stamina = 100
stamina_recharge = 0
stamina_color = (0, 255, 0)
inv_color1 = (101, 67, 33)
inv_color2 = (101, 67, 33)

# Creates fonts and renders static text.
item_font = pygame.font.SysFont("Times New Roman", 18)

# Loads assets.
map_test = pygame.image.load("Assets//Map_layout.png")
sam = pygame.image.load("Assets//sliding_sam.png")

# Image integers for iterating through spritesheets.
sam_y = 0

# Creates map surface to blit/transform.
map_surf = pygame.Surface((int(map_test.get_width()), int(map_test.get_height())))
map_surf.blit(map_test, (0, 0))
map_surf = pygame.transform.scale(map_surf, (win_x * 2, win_y * 2))

# Generates items (temporary: will be relocated to map_generator script)
items = []
inventory = []

# Test code for items.
items.append(Item(0, (1526, 645), "Hammer", (0, 255, 0)))
items.append(Item(0, (300, 300), "Bozo", (255, 255, 0)))
items.append(Item(0, (600, 600), "Taser", (0, 0, 255)))

## MAIN GAMEPLAY LOOP ##
while running :
    # Time control.
    delta_time = clock.tick() / 1000

    ## UPDATE ##
    player_rect = pygame.Rect((player_x - camera_x) + 20, (player_y - camera_y) + 15, 23, 44)
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

            # Item pickup command.
            if event.key == pygame.K_e :
                for item in items :
                    if player_rect.colliderect(item.collide_rect) :
                        items.remove(item)
                        inventory.append((item, item_font.render(item.name, True, (255, 255, 255))))

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

    # Updates camera positional values.
    camera_x, camera_y = player_x - (win_x / 2), player_y - (win_y / 2)

    # Player bounding.
    if player_x > (map_surf.get_width()) - (player_size / 2) :
        player_x = (map_surf.get_width()) - (player_size / 2)

    if player_x < 0 + (player_size / 2):
        player_x = 0 + (player_size / 2)

    if player_y > (map_surf.get_height()) - (player_size / 2) :
        player_y = (map_surf.get_height()) - (player_size / 2)

    if player_y < 0 + (player_size / 2):
        player_y = 0 + (player_size / 2)

    # Camera bounding.
    if camera_x > map_surf.get_width() - ((win_x / 2) * 2) :
        camera_x = map_surf.get_width() - ((win_x / 2) * 2)

    if camera_x < 0 :
        camera_x = 0

    if camera_y > map_surf.get_height() - ((win_y / 2) * 2) :
        camera_y = map_surf.get_height() - ((win_y / 2) * 2)

    if camera_y < 0 :
        camera_y = 0

    ## RENDERING ##
    win.fill((0, 0, 0))

    # Blits map.
    win.blit(map_surf, (0, 0), (camera_x, camera_y, win_x, win_y))

    # Draws player.
    win.blit(sam, (player_x - camera_x, player_y - camera_y, 64, 64), (0, sam_y, 64, 64))

    # Draws player hitbox.
    pygame.draw.rect(win, (255, 0, 0), player_rect, 1)

    # Draws items.
    for item in items :
        item_surf, item_x, item_y = item.update(camera_x, camera_y, player_rect)
        win.blit(item_surf, (item_x, item_y))

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

    pygame.display.flip()

# If running is set to False, runs this code.
pygame.quit()
