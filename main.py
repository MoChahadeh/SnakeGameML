import pygame
import numpy as np


WIDTH = 750
HEIGHT = 450

FPS = 60
clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeGameML")


def main_loop():

    running = True
    while running:

        for event in pygame.event.get():

            if(event == pygame.QUIT):
                running = False
        
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_loop()