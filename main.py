import pygame
import numpy as np
from snake import Snake


WIDTH = 750
HEIGHT = 450

FPS = 10
clock = pygame.time.Clock()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeGameML")

snake = Snake()


def main_loop():

    running = True
    while running:
        WINDOW.fill((100,100,100))
        for event in pygame.event.get():
            if(event == pygame.QUIT):
                running = False
            elif (event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_UP):
                    snake.changeDirection("UP")
                elif(event.key == pygame.K_DOWN):
                    snake.changeDirection("DOWN")
                elif(event.key == pygame.K_LEFT):
                    snake.changeDirection("LEFT")
                elif(event.key == pygame.K_RIGHT):
                    snake.changeDirection("RIGHT")
        

        snake.update(WINDOW)
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main_loop()