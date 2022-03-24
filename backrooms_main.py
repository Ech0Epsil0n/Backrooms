## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

## IMPORTS AND INITIALIZATIONS ##
import pygame
pickup = False
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
map_test = pygame.image.load("Backrooms assets//Map_layout.png")

# Creates map surface to blit/transform.
map_surf = pygame.Surface((int(map_test.get_width()), int(map_test.get_height())))
map_surf.blit(map_test, (0, 0))
map_surf = pygame.transform.scale(map_surf, (win_x * 2, win_y * 2))

# Generates items (temporary: will be relocated to map_generator script)
items = []
inventory = []
test_hammer = Item(0, (1526 - player_x, 645 - player_y), "Hammer", (0,255,0))
items.append(test_hammer)
print(items)

## MAIN GAMEPLAY LOOP ##
while running :
    # Time control.
    delta_time = clock.tick() / 1000

    ## UPDATE ##
    player_rect = pygame.Rect((win_x / 2) - 20, (win_y / 2) - 20, 40, 40)

    ## EVENT HANDLER ##
    for event in pygame.event.get() :
        ## KEYBOARD ONE-PRESS INPUT ##
        if event.type == pygame.QUIT:
            running = False
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

    


##    while pickup == True:
##        for event in pygame.event.get():
##            if event.type == pygame.KEYDOWN:
##                if event.key == pygame.K_e:
##                    items.pop(test_hammer)
##                    print(items)

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
    #enemy_surf, enemy_x, enemy_y = test_hammer.update(player_x, player_y, player_rect)
    #win.blit(enemy_surf, (enemy_x, enemy_y))

    # Temp Code
    pygame.draw.rect(win, (255, 0, 0), player_rect, 1)
    
    # Finalizes render / Inventory
    for item in items:
        item.render(map_surf)
        if player_x + 40 > item.mas_x-400 > player_x -40 and player_y + 40 > item.mas_y - 300 > player_y -40:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        item.color = (255,255,255)
                        item.render(map_surf)
                        items.remove(item)
                        inventory.append(item)
                        print(items)
                        for item in inventory:
                            print(item)

    # Inventory rendering
    
    inv_item1 = pygame.draw.Rect(win, (0, 0, 0), (750, 550, 50, 50))
    win.blit(inv_item1)
            
    pygame.display.flip()

# If running is set to False, runs this code.
pygame.quit()

