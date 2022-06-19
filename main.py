import pygame
import numpy as np
from neuralnet import NeuralNet
from snake import Snake
from copy import deepcopy


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

for i in range(population):

    nets.append(NeuralNet(12, 18, 4))
    snakes.add(Snake(index=i))


def drawLabels():
    genText = writer.render("Generation "+str(genNumber), True, (255,255,255))  #   Generation Number Label
    aliveText = writer.render("Alive: " + str(sum(map(lambda x : x ==False, dead))), True, (255,255,255))   #   number of birds alive Label
    bestFitness = writer.render("Best Fitness: " + str(max(fitness)), True, (255,255,255))  #   Fitness of best performing Model

    #   Drawing the labels on the screen
    WINDOW.blit(bestFitness, (10,50))
    WINDOW.blit(aliveText, (10,30))
    WINDOW.blit(genText, (10,10))

def main_loop():
    global dead
    running = True
    while running:
        WINDOW.fill((100,100,100))
        for event in pygame.event.get():
            if(event == pygame.QUIT):
                running = False
            elif (event.type == pygame.KEYDOWN):
                dead = [True] * population
        
        for currentSnake in snakes.sprites():

            if not currentSnake.dead:

                inputs = [[currentSnake.pos.x < currentSnake.food.x, currentSnake.pos.x > currentSnake.food.x, currentSnake.food.y < currentSnake.pos.y, currentSnake.food.y > currentSnake.pos.y, currentSnake.direction == "UP", currentSnake.direction == "DOWN", currentSnake.direction == "RIGHT", currentSnake.direction == "LEFT", currentSnake.dangerUp(), currentSnake.dangerDown(), currentSnake.dangerRight(), currentSnake.dangerLeft()]]

                nnOutput = nets[currentSnake.index].forward(inputs)
                decision = np.flip(np.argsort(nnOutput.T[0]))[0]

                if(decision == 0):
                    currentSnake.changeDirection("UP")
                elif(decision == 1):
                    currentSnake.changeDirection("DOWN")
                elif(decision == 2):
                    currentSnake.changeDirection("RIGHT")
                elif(decision == 3):
                    currentSnake.changeDirection("LEFT")
                
                fitness[currentSnake.index] += 1

                if(currentSnake.eatenFood):
                    fitness[currentSnake.index] += 150
                    print("FOOD", currentSnake.index)
                
                # if(currentSnake.danger()): fitness[currentSnake.index] -= 1
                
            else:
                dead[currentSnake.index] = True
            
        if(all(d == True for d in dead)): 
            print(fitness)
            restartAndMutate()

        snakes.update(WINDOW)
        drawLabels()
        pygame.display.update()
        clock.tick(FPS)


def restartAndMutate():
    global genNumber
    genNumber += 1  #   incrementing Generation Number
    maximums = np.flip(np.argsort(fitness)) #   sorts the indices of the fitnesses highest to lowest, which are the same indices for the corresponding neural nets
    fitness.clear() # resets the fitness list
    dead.clear()    # resets the dead list

    #   resetting the sprite groups:
    for snake in snakes: snake.kill()

    #   re-assigns new values to the state variables
    for i in range(population):
        fitness.append(0)
        snakes.add(Snake(index = i))
        dead.append(False)

        # Copies one of the three best performing neurons and appends it the list of neurons
        nets[i] = deepcopy(nets[maximums[i%3]])
        # Mutates the newly assigned neural net by a random rate between -15% and +15%
        nets[i].mutate(0.12)

if __name__ == "__main__":
    main_loop()