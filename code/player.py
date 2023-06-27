import pygame

class Player:
    def __init__(self, screen):
        width, height = screen.get_size()
        self.image = pygame.image.load('player.png')
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.explosion_image = pygame.image.load('explosion.png')
        self.explosion_image = pygame.transform.scale(self.explosion_image, (64, 64))
        self.pos = [width/2, height/2]  # 가로, 세로
        self.to = [0, 0]
        self.angle = 0
        self.invinciblemode = False
        self.invincibletime = 0
        
    def draw(self, screen):
        if self.to == [-1,-1]:
            self.angle = 45
        elif self.to == [-1,0]:
            self.angle = 90
        elif self.to == [-1,1]:
            self.angle = 135
        elif self.to == [0,1]:
            self.angle = 180
        elif self.to == [1,1]:
            self.angle = 225
        elif self.to == [1,0]:
            self.angle = 270
        elif self.to == [1,-1]:
            self.angle = 315
        elif self.to == [0,-1]:
            self.angle = 0
        rotated = pygame.transform.rotate(self.image, self.angle)
        
        calib_pos = (
            self.pos[0] - rotated.get_size()[0]/2,
            self.pos[1] - rotated.get_size()[1]/2
        )
        
        if self.invinciblemode == False:    
            screen.blit(rotated, calib_pos)
        else:   # 무적 상태라면
            self.invincibletime -= 1    
            if self.invincibletime < 0:
                self.invinciblemode = False
            if self.invincibletime % 3 == 0:    # 3틱 마다 나타나기 --> 깜빡거리기
                screen.blit(rotated, calib_pos)
        
    def goto(self, x, y):
        self.to[0] += x
        self.to[1] += y        
        
    def update(self, dt, screen):
        width, height = screen.get_size()
        # self.pos[0] = (self.pos[0] + dt * 0.5) % width  #대각선 방향
        # self.pos[1] = (self.pos[1] + dt * 0.3) % height #대각선 방향
        self.pos[0] = (self.pos[0] + dt * self.to[0] * 0.5)
        self.pos[1] = (self.pos[1] + dt * self.to[1] * 0.5) 
        # print("self.pos = ", self.pos)
        # print("self.to = ", self.to)
        
        # if self.pos[0] < 16:
        #     self.pos[0] = 16
        # if self.pos[0] > width-16:
        #     self.pos[0] = width-16
        # if self.pos[1] < 16:
        #     self.pos[1] = 16
        # if self.pos[1] > height-16:
        #     self.pos[1] = height-16
        self.pos[0] = min(width-16, max(16, self.pos[0]))
        self.pos[1] = min(height-16, max(16, self.pos[1]))
    
    # 총알 맞았을 때
    def explosion(self, screen):
        explosion_width = self.explosion_image.get_width()
        explosion_height = self.explosion_image.get_height()
        screen.blit(self.explosion_image, (self.pos[0] - explosion_width / 2, self.pos[1] - explosion_height / 2))
        
    def be_invincible(self):
        self.invincibletime = 30
        self.invinciblemode = True