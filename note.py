# note class by Kieron Pang, for Music Game
import pygame

class Note():
    def __init__(self, x, y, width, height, colour):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = colour
        self.hit_colour = None
        self.hit_timer = 0
        self.speed = 0.25 # less is slower

    def fall(self, dt):
        self.y += self.speed * dt # default speed

        if self.hit_timer > 0:
            self.hit_timer -= dt
            if self.hit_timer < 0:
                self.hit_timer = 0
    
    def draw(self, surface):
        center_x = int(self.x + self.width / 2)
        center_y = int(self.y + self.height / 2)
        radius = min(self.width, self.height) // 2

        draw_colour = self.hit_colour if self.hit_timer > 0 and self.hit_colour else self.colour
        pygame.draw.circle(surface, draw_colour, (center_x, center_y), radius)

    def is_in_hit_area(self, hit_y, tolerance):
        note_center_y = self.y + self.height / 2 # y position of the center of the note
        return hit_y - tolerance <= note_center_y <= hit_y + tolerance # check if the note is in the hit area