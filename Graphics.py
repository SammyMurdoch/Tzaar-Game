import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((736, 826))

pygame.display.set_caption("TZAAR")

clock = pygame.time.Clock()

#test_surface = pygame.Surface((100, 200))

background_surface = pygame.image.load("Board.jpg").convert_alpha()
pygame.draw.circle(screen, (12, 12, 12), (500, 500), 20, 10)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background_surface, (0, 0))

    pygame.display.update()
    clock.tick(60)

