#   June 20th, 2022, 06:55PM Friday
#   Mohamad Chahadeh, ©2022
#   https://MoChahadeh.github.io/
#   https://twitter.com/MoChahadeh

# libraries and settings
import pygame
import numpy as np
from neuralnet import NeuralNet
from snake import Snake
from copy import deepcopy
from settings import *


# first population initalization
for i in range(population):
    nets.append(NeuralNet(12, 18, 4))
    snakes.add(Snake(index=i))


# Draws labels on WINDOW
def drawLabels():

    genText = writer.render("Generation "+str(genNumber), True, (255,255,255))  #   Generation Number Label
    aliveText = writer.render("Alive: " + str(sum(map(lambda x : x ==False, dead))), True, (255,255,255))   #   number of birds alive Label
    bestFitness = writer.render("Best Fitness: " + str(max(fitness)), True, (255,255,255))  #   Fitness of best performing Model

    #   Drawing the labels on the screen
    WINDOW.blit(bestFitness, (10,50))
    WINDOW.blit(aliveText, (10,30))
    WINDOW.blit(genText, (10,10))

# Game Loop
def main_loop():
    global dead
    running = True
    while running:
        WINDOW.fill(BGCOLOR)    # background
        for event in pygame.event.get():    # pygame window events
            if(event == pygame.QUIT):   # quitting event
                running = False     # exists the loop
            elif (event.type == pygame.KEYDOWN):    # Key down events
                if(event.key == pygame.K_SPACE):
                    dead = [True] * population  # kills all snakes immediately which triggers the next generation

        for currentSnake in snakes.sprites():   # looping over all the snakes

            if not currentSnake.dead:   # checks if the snake is dead before it updates its states

                # neural network inputs
                inputs = [[currentSnake.pos.x < currentSnake.food.x, currentSnake.pos.x > currentSnake.food.x, currentSnake.food.y < currentSnake.pos.y, currentSnake.food.y > currentSnake.pos.y, currentSnake.direction == "UP", currentSnake.direction == "DOWN", currentSnake.direction == "RIGHT", currentSnake.direction == "LEFT", currentSnake.dangerUp(), currentSnake.dangerDown(), currentSnake.dangerRight(), currentSnake.dangerLeft()]]

                nnOutput = nets[currentSnake.index].forward(inputs)     # Forward propogation on Neural Network

                decision = np.flip(np.argsort(nnOutput.T[0]))[0]    # gets the index of the neuron with the heighest value, no negative values due to sigmoid activation function

                # neuron 0: UP, neuron 1: DOWN, neuron 2: RIGHT, neuron 3: LEFT
                if(decision == 0):
                    currentSnake.changeDirection("UP")
                elif(decision == 1):
                    currentSnake.changeDirection("DOWN")
                elif(decision == 2):
                    currentSnake.changeDirection("RIGHT")
                elif(decision == 3):
                    currentSnake.changeDirection("LEFT")
                
                # increments the fitness by 1 in each frame
                fitness[currentSnake.index] += 1

                if(currentSnake.eatenFood):
                    fitness[currentSnake.index] += foodReward   # rewards the snake with extra fitness for eating the food
                    print("FOOD", currentSnake.index)         
            else:
                dead[currentSnake.index] = True     # if the snake's internal variable DEAD is true, sets the outside variable to true as well
            
        if(all(d == True for d in dead)):   # if all snakes are dead
            print(fitness)
            restartAndMutate()      # resets the state variables with mutations and selection of Neural Networks

        snakes.update()     # triggers update method for all snakes
        drawLabels()        # draws the labels onto the screen in each frame
        pygame.display.update()     # updates the pygame window to show the new drawings on the screen
        clock.tick(FPS)     # sets the frame rate of the loop


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
        nets[i] = deepcopy(nets[maximums[i%copyBest]])
        # Mutates the newly assigned neural net by a random rate between -15% and +15%
        nets[i].mutate(mutationRate)

if __name__ == "__main__":
    main_loop()