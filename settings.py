import pygame
from neuralnet import NeuralNet

WIDTH = 750
HEIGHT = 450

FPS = 60
clock = pygame.time.Clock()

genNumber = 1
population = 200
initialMoves = 200
copyBest = 5
mutationRate = 0.12
foodReward = 150

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeGameML")

BGCOLOR = (100,100,100)
SNAKECOLOR = (50,200,80)
WHITECOLOR = (255,255,255)

pygame.font.init()
writer = pygame.font.SysFont("Roboto", 20)

snakes = pygame.sprite.Group()

nets: list[NeuralNet] = []
fitness = [0] * population
dead = [False] * population
