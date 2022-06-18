import pygame
from random import randint

directions = ["UP", "RIGHT", "DOWN", "LEFT"]

class Snake(pygame.sprite.Sprite):

    def __init__(self, *groups) -> None:
        super().__init__(*groups)
        self.pos = pygame.Vector2(randint(4, 70)*10, randint(2, 40)*10)
        self.body = [pygame.Vector2(self.pos.x,self.pos.y), pygame.Vector2(self.pos.x-10, self.pos.y), pygame.Vector2(self.pos.x-20, self.pos.y)]
        self.color = (50,200,80)
        self.food = pygame.rect.Rect(randint(4, 70)*10, randint(2, 40)*10, 10, 10)
        self.direction = "RIGHT"
    def draw(self, WINDOW: pygame.Surface):
        for i in range(len(self.body)):
            pygame.draw.rect(WINDOW, self.color, pygame.Rect(self.body[i].x, self.body[i].y, 10, 10))
        pygame.draw.rect(WINDOW, (255,255,255), self.food)

    def update(self, WINDOW):

        if(self.direction == "RIGHT"):
            self.pos.x += 10
        elif(self.direction == "LEFT"):
            self.pos.x -= 10
        elif(self.direction == "UP"):
            self.pos.y -= 10
        elif (self.direction == "DOWN"):
            self.pos.y += 10

        self.body.insert(0, pygame.Vector2(self.pos.x, self.pos.y))

        if(self.foodCollision()):
            self.food.x = randint(4, 70)*10
            self.food.y = randint(2, 40)*10
        else : self.body.pop()
        
        self.draw(WINDOW)
    
    def foodCollision(self):
        return self.pos.x == self.food.x and self.pos.y == self.food.y
    
    def changeDirection(self, direction: str):
        
        if (self.direction == directions[(directions.index(direction)+2) % 4]): return
        self.direction = direction

