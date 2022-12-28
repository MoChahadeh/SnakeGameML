#   June 20th, 2022, 06:55PM Friday
#   Mohamad Chahadeh, ©2022
#   https://MoChahadeh.github.io/
#   https://twitter.com/MoChahadeh


# libraries and classes
import pygame
from neuralnet import NeuralNet


# Width and Height of pygame window
WIDTH = 750
HEIGHT = 450


# Game windows initialization
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SnakeGameML")


# fps of game loop
FPS = 60
clock = pygame.time.Clock()


# gameplay settings
population = 500
initialMoves = 300
copyBest = 15
mutationRate = 0.12
foodReward = 400


# colors used in game
BGCOLOR = (100,100,100)
SNAKECOLOR = (50,200,80)
WHITECOLOR = (255,255,255)


# text writer intialization
pygame.font.init()
writer = pygame.font.SysFont("Roboto", 20)


# Snake Sprites Group
snakes = pygame.sprite.Group()


# State variables
genNumber = 1
nets: list[NeuralNet] = []
fitness = [0] * population
dead = [False] * population
