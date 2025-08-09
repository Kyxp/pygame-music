# note class
import pygame

class Note():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.speed = 0.2

    def fall(self, dt):
        self.y += self.speed * dt # default speed
    
    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, self.colour, rect)