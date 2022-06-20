#   June 20th, 2022, 06:55PM Friday
#   Mohamad Chahadeh, ©2022
#   https://MoChahadeh.github.io/
#   https://twitter.com/MoChahadeh

# libraries and settings
import pygame
from random import *
from settings import *

# possible directions
directions = ["UP", "RIGHT", "DOWN", "LEFT"]


# Snake Class
class Snake(pygame.sprite.Sprite):

    # Class Contructor
    def __init__(self, *groups, index = None) -> None:
        super().__init__(*groups)   #calling superclass (Sprite) constructor
        self.pos = pygame.Vector2(randint(1, (WIDTH-10)/10)*10, randint(1, (HEIGHT-10)/10)*10)      # inital position of snake (Random)

        self.body = [pygame.Vector2(self.pos.x,self.pos.y), pygame.Vector2(self.pos.x-10, self.pos.y), pygame.Vector2(self.pos.x-20, self.pos.y)]   # Body of snake as a list of Vector positions
        self.color = SNAKECOLOR
        self.food = pygame.rect.Rect(randint(1, (WIDTH-10)/10)*10, randint(1, (HEIGHT-10)/10)*10, 10, 10)   # food for the Snake, Initialized at a random position
        self.direction = choice(directions)     # random first direction of snake
        self.dead = False   # dead state variable of the snake
        self.eatenFood = False
        self.index = index  # index of snake in the Snakes Sprite Group defined in settings.py
        self.movesLeft = initialMoves   # number of moves left for the snake before it dies, initialized in settings.py

    # Draws the snake's body and food on the WINDOW
    def draw(self):
        for i in range(len(self.body)):
            pygame.draw.rect(WINDOW, self.color, pygame.Rect(self.body[i].x, self.body[i].y, 10, 10))   # draws the body
        pygame.draw.rect(WINDOW, WHITECOLOR, self.food)     # draws the food

    def update(self):

        self.eatenFood = False      # resets the variable if the food was eaten in the previous frame..

        if(not self.dead):      # updates the snake's states if it's not dead already

            # moves the snake in the set direction
            if(self.direction == "RIGHT"):
                self.pos.x += 10
            elif(self.direction == "LEFT"):
                self.pos.x -= 10
            elif(self.direction == "UP"):
                self.pos.y -= 10
            elif (self.direction == "DOWN"):
                self.pos.y += 10

            
            if(self.bodyCollision()):   # kills the snake if it "Touches" itself ;)
                self.dead = True

            
            self.body.insert(0, pygame.Vector2(self.pos.x, self.pos.y))     # adds a new rect at the head of the snake, effectively making it grow

            if(self.foodCollision()):       # if the snake ate the food
                self.eatenFood = True
                self.food.x = randint(4, 70)*10    # VVVV
                self.food.y = randint(2, 40)*10    # Resets the food's position randomly
                self.movesLeft += 80    # rewards the snake with more moves
                # print("FOOD INSIDE")
            else : self.body.pop()      # if the snake didn't eat the food, it removes the last rect from the body, creating the motion effect...

            if (self.borderCollision()):    # if snake collides with the borders of the screen
                self.dead = True
            
            if(self.movesLeft <= 0):    # if the snake runs out of moves
                self.dead = True
                print("ran out of moves", self.index)

            self.movesLeft -= 1     # decreases the moves with each frame
            self.draw()     # draws the snake on the screen

    def foodCollision(self):        # self explanatory
        return self.pos.x == self.food.x and self.pos.y == self.food.y
    
    def borderCollision(self):      # self explanatory
        return self.pos.x == -10 or self.pos.x == WIDTH or self.pos.y == -10 or self.pos.y == HEIGHT
    
    def bodyCollision(self):
        return next((rect for rect in self.body if rect.x == self.pos.x and rect.y == self.pos.y), None) != None

    def changeDirection(self, direction: str):
        
        if (self.direction == directions[(directions.index(direction)+2) % 4]): self.dead = True    # checks if the direction to change to is opposite of current direction
        else: self.direction = direction
    
    # checking for danger (i.e. moving in this direction would kill the snake)
    def dangerRight(self):
        return self.pos.x+10 == WIDTH or next((rect for rect in self.body if rect.x == self.pos.x+10 and rect.y == self.pos.y), None) != None
    def dangerLeft(self):
        return self.pos.x-10 == -10 or next((rect for rect in self.body if rect.x == self.pos.x-10 and rect.y == self.pos.y), None) != None
    def dangerUp(self):
        return self.pos.y-10 == -10 or next((rect for rect in self.body if rect.x == self.pos.x and rect.y == self.pos.y-10), None) != None
    def dangerDown(self):
        return self.pos.y+10 == HEIGHT or next((rect for rect in self.body if rect.x == self.pos.x and rect.y == self.pos.y+10), None) != None
    
    def danger(self):
        return self.dangerRight() or self.dangerLeft() or self.dangerDown() or self.dangerUp()

