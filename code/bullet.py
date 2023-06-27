import pygame
import random

class Bullet:
    def __init__(self, x, y, to_x, to_y):
        color_list = [(255,0,0), (0,255,0), (0,0,254)]  # red, green, blue
        radius_list = [4, 8, 12]
        self.pos = [x, y]
        self.to = [to_x, to_y]
        self.radius = radius_list[random.randint(0,2)]
        self.color = color_list[random.randint(0,2)]  
    
    def update_and_draw(self, dt, screen):
        width, height = screen.get_size()
        self.pos[0] = (self.pos[0] + dt * self.to[0] * 0.5) % width
        self.pos[1] = (self.pos[1] + dt * self.to[1] * 0.5) % height
        pygame.draw.circle(screen, self.color, self.pos, self.radius)