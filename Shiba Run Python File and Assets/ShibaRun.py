import pygame
import os
import sys
import random
pygame.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

sc_height = 384
sc_width = 682
screen = pygame.display.set_mode((sc_width, sc_height))
pygame.display.set_caption('Shiba Run')
BG = pygame.image.load(os.path.join('Assets/Other', 'background.png'))

running = [pygame.image.load(resource_path('Assets/Dog/dog1.png')),
           pygame.image.load(resource_path('Assets/Dog/dog2.png')),
           pygame.image.load(resource_path('Assets/Dog/dog3.png')),
           pygame.image.load(resource_path('Assets/Dog/dog4.png'))]

jumping = pygame.image.load(resource_path('Assets/Dog/dogjump.png'))

ducking = [pygame.image.load(resource_path('Assets/Dog/duck1.png')),
           pygame.image.load(resource_path('Assets/Dog/duck2.png')),
           pygame.image.load(resource_path('Assets/Dog/duck3.png')),
           pygame.image.load(resource_path('Assets/Dog/duck4.png'))]

BIRD = [pygame.image.load(resource_path('Assets/Obstacles/bird1.png')),
        pygame.image.load(resource_path('Assets/Obstacles/bird2.png'))]

FIREHYDRANT = [pygame.image.load(resource_path('Assets/Obstacles/firehydrant.png')),
               pygame.image.load(resource_path('Assets/Obstacles/firehydrant2.png'))]
CAT = [pygame.image.load(resource_path('Assets/Obstacles/cat.png')),
       pygame.image.load(resource_path('Assets/Obstacles/cat2.png'))]
FENCE = [pygame.image.load(resource_path('Assets/Obstacles/fence.png')),
         pygame.image.load(resource_path('Assets/Obstacles/fence2.png'))]

StartScreen = pygame.image.load(resource_path('Assets/Other/shibaRun.png'))
GameOver = pygame.image.load(resource_path('Assets/Other/gameover.png'))
DogStart = pygame.image.load(resource_path('Assets/Dog/dogstart.png'))
DogOver = pygame.image.load(resource_path('Assets/Dog/dogover.png'))

class Shiba:
    X_POS = 70
    Y_POS = 290
    Y_POS_DUCK = 310
    JUMP_VEL = 7

    def __init__(self):
        self.duck_img = ducking
        self.run_img = running
        self.jump_img = jumping

        self.shiba_duck = False
        self.shiba_run = True
        self.shiba_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.shiba_rect = self.image.get_rect()
        self.shiba_rect.x = self.X_POS
        self.shiba_rect.y = self.Y_POS

    def update(self, userInput):
        if self.shiba_duck:
            self.duck()
        if self.shiba_run:
            self.run()
        if self.shiba_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.shiba_jump:
            self.shiba_duck = False
            self.shiba_run = False
            self.shiba_jump = True
        elif userInput[pygame.K_DOWN] and not self.shiba_jump:
            self.shiba_duck = True
            self.shiba_run = False
            self.shiba_jump = False
        elif not (self.shiba_jump or userInput[pygame.K_DOWN]):
            self.shiba_duck = False
            self.shiba_run = True
            self.shiba_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.shiba_rect = self.image.get_rect()
        self.shiba_rect.x = self.X_POS
        self.shiba_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.shiba_rect = self.image.get_rect()
        self.shiba_rect.x = self.X_POS
        self.shiba_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.shiba_jump:
            self.shiba_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.shiba_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, screen):
        screen.blit(self.image, (self.shiba_rect.x, self.shiba_rect.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = sc_width

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.image[self.type], self.rect)


class FireHydrant(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 270


class Fence(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 270

class Cat(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0,1)
        super().__init__(image, self.type)
        self.rect.y = 310

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        h = random.randint(0,1)
        if h == 0:
            self.rect.y = 290
        elif h == 1:
            self.rect.y = 255
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        screen.blit(self.image[self.index//5], self.rect)
        self.index += 1

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, high_score
    run = True
    clock = pygame.time.Clock()
    player = Shiba()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 0
    points = 0
    finalpts = 0
    high_score = 0
    font = pygame.font.Font(os.path.join('Assets/Other', 'dotgothic16.ttf'), 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:
            game_speed += 1

        text = font.render("Score: " + str(points), True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (600,10)
        screen.blit(text, textRect)

    def highscore():
        global points, high_score
            
        high_sc = open(os.path.join('Assets/Other', 'highscore.txt'), 'r')
        hi_score = high_sc.read()
        high_score = int(hi_score)
        if points>high_score:
            hisc = open(os.path.join('Assets/Other', 'highscore.txt'), 'w')
            hisc.write(str(points))
            hisc.close()
        high_sc.close()
    
    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        screen.blit(BG, (x_pos_bg, y_pos_bg))
        screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            screen.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                

        screen.fill((255, 255, 255))
        userInput = pygame.key.get_pressed()
        background()
        player.draw(screen)
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 3) == 0:
                obstacles.append(FireHydrant(FIREHYDRANT))
            elif random.randint(0, 3) == 1:
                obstacles.append(Fence(FENCE))
            elif random.randint(0, 3) == 2:
                obstacles.append(Bird(BIRD))
            elif random.randint(0,3) == 3:
                obstacles.append(Cat(CAT))

        for obstacle in obstacles:
            obstacle.draw(screen)
            obstacle.update()
            if player.shiba_rect.colliderect(obstacle.rect):
                pygame.time.delay(1500)
                highscore()
                death_count += 1
                menu(death_count)
                
        score()
        clock.tick(30)
        pygame.display.update()
    
def menu(death_count):
    global points, high_score
    run = True

    while run:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(os.path.join('Assets/Other', 'dotgothic16.ttf'), 30)
        sm_font = pygame.font.Font(os.path.join('Assets/Other', 'dotgothic16.ttf'), 20)
        
        if death_count == 0:
            screen.blit(BG, (0,0))
            screen.blit(StartScreen, (125,80))
            screen.blit(DogStart, (275,190))
            text = font.render("Press any Key to Start", True, (0, 0, 0))
            
        elif death_count > 0:
            screen.fill((105,105,105))
            screen.blit(GameOver, (125, 80))
            screen.blit(DogOver, (275,190))
            
            hs = open(os.path.join('Assets/Other', 'highscore.txt'), 'r')
            high = hs.read()
            
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = sm_font.render("Current Score: " + str(points), True, (0, 0, 0))
            HSfont = sm_font.render("High Score: " + high, True, (0, 0, 0))

            scoreRect = score.get_rect()
            scoreRect.center = (sc_width // 2, sc_height // 2 + 30)
            screen.blit(score, scoreRect)

            hiscRect = HSfont.get_rect()
            hiscRect.center = (sc_width // 2, sc_height // 2 + 50)
            screen.blit(HSfont, hiscRect)
            
        textRect = text.get_rect()
        textRect.center = (sc_width // 2, sc_height// 2)
        screen.blit(text, textRect)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hs = open(os.path.join('Assets/Other', 'highscore.txt'), 'w')
                hs.write("0")
                hs.close()
                
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()

menu(0)

