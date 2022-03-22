# Main file for running the Backrooms game

import pygame
running = True

print("Welcome to the Backrooms")

while running:
    screen = pygame.display.set_mode((800, 600))
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
pygame.quit()


