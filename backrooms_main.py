## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

## IMPORTS AND INITIALIZATIONS ##
import pygame

# Pygame standard initialization.
pygame.init()
win_x, win_y = 800, 600
win = pygame.display.set_mode((win_x, win_y))
clock = pygame.time.Clock
clock = pygame.time.Clock()
running = True

# Establishes baseline variables.
move_speed = 100
player_x, player_y = 0, 0

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
            if pygame.key == pygame.K_LSHIFT or pygame.key == pygame.K_LCTRL :
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

    # Temp code to showcase movement.
    pygame.draw.rect(win, (255, 0, 0), (0 - player_x, 0 - player_y, 10, 10), 1)

    # Draws player.
    pygame.draw.circle(win, (255, 255, 255), (win_x / 2, win_y / 2), 20)

    # Finalizes render.
    pygame.display.flip()

# If running is set to False, runs this code.
pygame.quit()

