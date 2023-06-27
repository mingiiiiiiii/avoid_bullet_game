import pygame
import random
import time
import sys
from background import Background
from player import Player
from bullet import Bullet

def collision(a, b):
    dist = ((a.pos[0] - b.pos[0]) ** 2 + (a.pos[1] - b.pos[1]) ** 2) ** 0.5
    if dist < 20:
        return True
    else:
        return False

# def draw_text(txt, size, pos, color, screen):
def draw_text(txt, size, pos, color):    
    font = pygame.font.Font('freesansbold.ttf', size)
    r = font.render(txt, True, color)
    screen.blit(r, pos)
        
WIDTH, HEIGHT = 1000, 600

running = True
gameover = False

clock = pygame.time.Clock()
FPS = 60

time_for_adding_bullets = 0
start_time = time.time()    # 시작 시간

pygame.init()
pygame.display.set_caption("총알 피하기")

# screen 만들기
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 배경 만들기
background = Background(0, 0)

# 플레이어 만들기
player = Player(screen)

life = 10    # 생명
score = 0

# background screen
# bg_image = pygame.image.load('bg.jpg')
# bg_pos = 0

# background music
pygame.mixer_music.load('bgm.wav')
pygame.mixer.music.play(-1)

# bullet = Bullet(0,0,1,0.5)
bullets = []
for i in range(5):
    # random.random() --> 0 ~ 1 사이 랜덤
    bullets.append(Bullet(0, random.random() * HEIGHT, 2*(random.random()-0.5), 2*(random.random()-0.5)))

# Game Loop
while running:
    dt = clock.tick(FPS)    # dt = 밀리세컨드 (tick의 수)
    
    time_for_adding_bullets += dt
    if time_for_adding_bullets >= 1000:
        bullets.append(Bullet(0, random.random() * HEIGHT, 2*(random.random()-0.5), 2*(random.random()-0.5)))
        time_for_adding_bullets -= 1000
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   # 창 닫기 버튼을 눌렀을때 게임 종료
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.goto(-1,0)
                background.goto(1,0)
            elif event.key == pygame.K_RIGHT:
                player.goto(1,0)
                background.goto(-1,0)
            elif event.key == pygame.K_UP:
                player.goto(0,-1)
                background.goto(0,1)
            elif event.key == pygame.K_DOWN:
                player.goto(0,1)
                background.goto(0,-1)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.goto(1,0)
                background.goto(-1,0)
            elif event.key == pygame.K_RIGHT:
                player.goto(-1,0)
                background.goto(1,0)
            elif event.key == pygame.K_UP:
                player.goto(0,1)
                background.goto(0,-1)
            elif event.key == pygame.K_DOWN:
                player.goto(0,-1)
                background.goto(0,1)
    
    # screen.fill((0,0,0))
    # bg_pos -= 0.01 * dt
    # screen.blit(bg_image, (bg_pos, 0))
    
    player.update(dt, screen)
    background.update(dt, screen)
    
    background.draw(screen) # 화면에 background 그리기
    player.draw(screen) # 화면에 player 그리기 (순서 중요 배경보다 나중에 그려야함)
    
    for b in bullets:
        b.update_and_draw(dt, screen)
        
    for b in bullets:
        if collision(player, b) and player.invinciblemode != True:
            pygame.mixer.Sound('gun.mp3').play()    # (1) 총에 맞았을 때 효과음
            player.explosion(screen)
            player.be_invincible()
            if b.radius == 12:
                life -= 3
            elif b.radius == 8:
                life -= 2
            else:   # b.radius == 4
                life -= 1
            
            if life <= 0:
                gameover = True
                
    if gameover == True:
        f = open('score.txt', 'a')
        msg = f"{score:.3f}\n"
        f.write(msg)
        f.close()
        running = False     # goto GameOver Loop
    else:
        score = time.time() - start_time
        draw_text(f"Time: {time.time() - start_time:.2f}, Bullets: {len(bullets)}, Life: {life}  {'#' * life}", 16, (10,10), (255,255,255))
        
    pygame.display.update() # 화면에 새로운 그림을 그린다 (화면을 갱신한다)
    
f = open('score.txt', 'r')
score_list = f.readlines()  # score_list에 score 저장
for i in range(len(score_list)):
    score_list[i] = float(score_list[i].strip())  # 개행문자 제거하고 float로 저장 ( sort 위해서 )
score_list.sort(reverse = True)     # 내림차순 정렬
print(score_list)
f.close()

# GameOver Loop
while running != True:
    screen.fill((0,0,0))    # 화면에 검은색 채우기
    draw_text("GAME OVER", 100, (WIDTH/5, 0), (255,255,255))
    draw_text("PRESS ENTER TO QUIT", 50, (WIDTH/5 + 20, 100), (255,150,255))
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:   # 창 닫기 버튼을 눌렀을때
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_RETURN:    # 엔터 누르면 게임 종료
                pygame.quit()
                sys.exit()
    for i in range(min(10, len(score_list))):
        if str(score_list[i]) == f"{score:.3f}":    
            draw_text(f"{i+1:<3} : {score_list[i]:.3f}", 35, (WIDTH/3 + 40, 150 + 40*i), (0,255,255))   # 기록이 10개 안에 있으면 하늘색으로 출력
        else:   
            draw_text(f"{i+1:<3} : {score_list[i]:.3f}", 35, (WIDTH/3 + 40, 150 + 40*i), (255,255,255)) # 기록이 10개 안에 없으면 그냥 출력
    
    pygame.display.update()
