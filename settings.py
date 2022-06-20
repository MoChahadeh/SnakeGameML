import pygame

WIDTH = 750
HEIGHT = 450

FPS = 60
clock = pygame.time.Clock()

genNumber = 1
population = 200

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeGameML")

pygame.font.init()
writer = pygame.font.SysFont("Roboto", 20)

snakes = pygame.sprite.Group()

nets: list[NeuralNet] = []
fitness = [0] * population
dead = [False] * population
