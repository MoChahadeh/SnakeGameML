import pygame
from random import randint

directions = ["UP", "RIGHT", "DOWN", "LEFT"]

class Snake(pygame.sprite.Sprite):

    def __init__(self, *groups, index = None) -> None:
        super().__init__(*groups)
        self.pos = pygame.Vector2(randint(4, 70)*10, randint(2, 40)*10)
        self.body = [pygame.Vector2(self.pos.x,self.pos.y), pygame.Vector2(self.pos.x-10, self.pos.y), pygame.Vector2(self.pos.x-20, self.pos.y)]
        self.color = (50,200,80)
        self.food = pygame.rect.Rect(randint(4, 70)*10, randint(2, 40)*10, 10, 10)
        self.direction = "RIGHT"
        self.dead = False
        self.eatenFood = False
        self.index = index
        self.movesLeft = 200
    def draw(self, WINDOW: pygame.Surface):
        for i in range(len(self.body)):
            pygame.draw.rect(WINDOW, self.color, pygame.Rect(self.body[i].x, self.body[i].y, 10, 10))
        pygame.draw.rect(WINDOW, (255,255,255), self.food)

    def update(self, WINDOW):
        self.eatenFood = False
        if(not self.dead):
            if(self.direction == "RIGHT"):
                self.pos.x += 10
            elif(self.direction == "LEFT"):
                self.pos.x -= 10
            elif(self.direction == "UP"):
                self.pos.y -= 10
            elif (self.direction == "DOWN"):
                self.pos.y += 10

            if(self.bodyCollision()):
                self.dead = True

            self.body.insert(0, pygame.Vector2(self.pos.x, self.pos.y))

            if(self.foodCollision()):
                self.eatenFood = True
                self.food.x = randint(4, 70)*10
                self.food.y = randint(2, 40)*10
                self.movesLeft += 80
                # print("FOOD INSIDE")
            else : self.body.pop()

            if (self.borderCollision()):
                self.dead = True
            
            if(self.movesLeft <= 0):
                self.dead = True
                print("ran out of moves", self.index)

            self.movesLeft -= 1
            self.draw(WINDOW)

    def foodCollision(self):
        return self.pos.x == self.food.x and self.pos.y == self.food.y
    
    def borderCollision(self):
        return self.pos.x == 0 or self.pos.x == 750 or self.pos.y == 0 or self.pos.y == 450
    
    def bodyCollision(self):
        return next((rect for rect in self.body if rect.x == self.pos.x and rect.y == self.pos.y), None) != None

    def changeDirection(self, direction: str):
        
        if (self.direction == directions[(directions.index(direction)+2) % 4]): self.dead = True
        else: self.direction = direction
    
    def dangerRight(self):
        return self.pos.x+10 == 750 or next((rect for rect in self.body if rect.x == self.pos.x+10 and rect.y == self.pos.y), None) != None
    def dangerLeft(self):
        return self.pos.x-10 == 0 or next((rect for rect in self.body if rect.x == self.pos.x-10 and rect.y == self.pos.y), None) != None
    def dangerUp(self):
        return self.pos.y-10 == 0 or next((rect for rect in self.body if rect.x == self.pos.x and rect.y == self.pos.y-10), None) != None
    def dangerDown(self):
        return self.pos.y+10 == 450 or next((rect for rect in self.body if rect.x == self.pos.x and rect.y == self.pos.y+10), None) != None
    
    def danger(self):
        return self.dangerRight() or self.dangerLeft() or self.dangerDown() or self.dangerUp()

