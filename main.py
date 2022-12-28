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

    decided = False
    while not decided:
        decision = input("Do you want to train a new model (1) or load a saved model (2)? (e for exit):  ")

        if(decision == "1"):
            for i in range(population):
                nets.append(NeuralNet(24, 30, 28, 4))
                snakes.add(Snake(index=i))
            decided = True
        elif(decision == "2"):

            modelname = input("enter model name: ")
            modelNet = NeuralNet(24, 30, 28, 4)
            modelNet.load(modelname)
            for i in range(population):
                net = deepcopy(modelNet)
                net.mutate(mutationRate + (mutationRate * i%2))
                nets.append(net)
                snakes.add(Snake(index=i))
            decided = True
        elif(decision == "e"):
            exit()
        else:
            print("Invalid Input")
            continue


    running = True
    ticks = -1
    timelapse = False
    while running:
        WINDOW.fill(BGCOLOR)    # background
        for event in pygame.event.get():    # pygame window events
            if(event == pygame.QUIT):   # quitting event
                running = False     # exists the loop
            elif (event.type == pygame.KEYDOWN):    # Key down events
                if(event.key == pygame.K_SPACE):
                    dead = [True] * population  # kills all snakes immediately which triggers the next generation
                if(event.key == pygame.K_t):
                    timelapse = not timelapse
                if(event.key == pygame.K_s):
                    nets[np.flip(np.argsort(fitness))[0]].save()

        for currentSnake in snakes.sprites():   # looping over all the snakes

            if not currentSnake.dead:   # checks if the snake is dead before it updates its states

                # neural network inputs
                inputs = [[currentSnake.pos.x < currentSnake.food.x, currentSnake.pos.x > currentSnake.food.x, currentSnake.food.y < currentSnake.pos.y, currentSnake.food.y > currentSnake.pos.y, currentSnake.direction == "UP", currentSnake.direction == "DOWN", currentSnake.direction == "RIGHT", currentSnake.direction == "LEFT", currentSnake.directionHistory[-2] == "UP", currentSnake.directionHistory[-2] == "DOWN", currentSnake.directionHistory[-2] == "RIGHT", currentSnake.directionHistory[-2] == "LEFT",  currentSnake.directionHistory[-3] == "UP", currentSnake.directionHistory[-3] == "DOWN", currentSnake.directionHistory[-3] == "RIGHT", currentSnake.directionHistory[-3] == "LEFT", currentSnake.directionHistory[-4] == "UP", currentSnake.directionHistory[-4] == "DOWN", currentSnake.directionHistory[-4] == "RIGHT", currentSnake.directionHistory[-4] == "LEFT", currentSnake.dangerUp(), currentSnake.dangerDown(), currentSnake.dangerRight(), currentSnake.dangerLeft()]]

                nnOutput = nets[currentSnake.index].forward(inputs)     # Forward propogation on Neural Network

                decision = np.flip(np.argsort(nnOutput.T[0]))[0]    # gets the index of the neuron with the heighest value, no negative values due to sigmoid activation function

                if(decision == 0):
                    # Don't change direction if the snake is already going in that direction
                    if(currentSnake.direction == "UP"):
                        continue
                    currentSnake.changeDirection("UP")
                elif(decision == 1):
                    if(currentSnake.direction == "DOWN"):
                        continue
                    currentSnake.changeDirection("DOWN")
                elif(decision == 2):
                    if(currentSnake.direction == "RIGHT"):
                        continue
                    currentSnake.changeDirection("RIGHT")
                elif(decision == 3):
                    if(currentSnake.direction == "LEFT"):
                        continue
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
        ticks += 1
        if(not timelapse):
            drawLabels()        # draws the labels onto the screen in each frame
            pygame.display.update()     # updates the pygame window to show the new drawings on the screen
            clock.tick(FPS)     # sets the frame rate of the loop
        elif(ticks % 15 == 0):
                drawLabels()        # draws the labels onto the screen in each frame
                pygame.display.update()     # updates the pygame window to show the new drawings on the screen

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

        # Copies one of the best performing neurons and appends it the list of neurons
        nets[i] = deepcopy(nets[maximums[i%copyBest]])
        # Mutates the newly assigned neural net by a random rate between -+mutationRate defined in settings.py
        nets[i].mutate(mutationRate + (mutationRate * i%2))

if __name__ == "__main__":
    main_loop()