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
running = True

## MAIN GAMEPLAY LOOP ##
while running :
    # Time control.
    delta_time = clock.tick() / 1000

    ## UPDATE ##
    # (This is where we would update variables, such as reducing stamina over time if the player is running,
    # updating a continually decreasing timer, etc.) #

    ## EVENT HANDLER ##
    for event in pygame.event.get() :
        # Quits games.
        if event.type == pygame.QUIT :
            running = False

        ## KEYBOARD ONE-PRESS INPUT ##
        if event.type == pygame.KEYDOWN :
            if pygame.key == pygame.K_ESCAPE :
                running = False

        ## CONTINUOUS KEYBOARD INPUT ##
        keys = pygame.key.get_pressed()


# If running is set to False, runs this code.
pygame.quit()
quit()