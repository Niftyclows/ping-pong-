from random import random
import pygame
import sys
import os


class Sprite:
    def __init__(self, center, image):
        self.image = image
        self.rect = image.get_frect()
        # rect - rectangle - прямоугольник
        self.rect.center = center

    def render(self, surface):
        surface.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, center, image, speed):
        super().__init__(center, image)
        self.start_center = center
        self.speed = speed
        self.move_up = False
        self.move_down = False
        
    def reset(self):
        self.rect.center = self.start_center 
        self.move_up = False 
        self.move_down = False


    def update(self):
        if self.move_up != self.move_down:
            if self.move_up:
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600


class Ball(Sprite):
    def __init__(self, center, image, speed):
        super().__init__(center, image)
        self.start_center = center
        self.start_speed = speed
        self.speed = speed
        self.velocity = pygame.Vector2(1, 0)

    def reset(self):
        self.rect.center = self.start_center
        self.speed = self.start_speed
        self.velocity.update(1, 0)



    def check_x_collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.velocity.x > 0:
                self.rect.right = player.rect.left
            else:
                self.rect.left = player.rect.right
            self.velocity.x = -self.velocity.x
            self.velocity.rotate_ip((random() - 0.5) * 15)
            self.speed += 0.5
            hit_sound.play()

    def check_y_collision(self, player):
        if self.rect.colliderect(player.rect):
            if self.velocity.y > 0:
                self.rect.bottom = player.rect.top
            else:
                self.rect.top = player.rect.bottom
            self.velocity.y = -self.velocity.y

    def update(self, left_player, right_player):
        vector = self.velocity * self.speed

        self.rect.x += vector.x
        self.check_x_collision(left_player)
        self.check_x_collision(right_player)

        self.rect.y += vector.y
        self.check_y_collision(left_player)
        self.check_y_collision(right_player)

        if self.rect.top <= 0:
            self.rect.top = 0
            self.velocity.y = -self.velocity.y
        if self.rect.bottom >= 600:
            self.rect.bottom = 600
            self.velocity.y = -self.velocity.y


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)


    


pygame.init()
window = pygame.Window("Ping Pong", (800, 600), pygame.WINDOWPOS_CENTERED)
surface = window.get_surface()  # surface - поверхность
clock = pygame.Clock()
font = pygame.Font(None, 32)


image = pygame.image.load(get_path('images/ракетка 2.jpg'))
image = pygame.transform.scale(image,(150,150))
left_player = Player((40, 300), image, 10)
right_player = Player((760, 300), image, 10)

image = pygame.image.load(get_path("images/мячик для тениса.jpg"))
image = pygame.transform.scale(image,(80,80))
image.set_colorkey("white")
ball = Ball((400, 300), image, 5)


background = pygame.image.load(get_path('images/fon.jpg'))
background = pygame.transform.scale(background,(800,600))

running = True
left_score = 0
right_score = 0

pygame.mixer.music.load(get_path('sounds/Erika_-_I_Dont_Know_66178755.mp3'))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops = -1 )

hit_sound = pygame.mixer.Sound(get_path('sounds/ball-bounce.mp3'))
hit_sound.set_volume(1.0)
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # При нажатии на клавишу...
        elif event.type == pygame.KEYDOWN:
            # Левый игрок
            if event.key == pygame.K_w:
                left_player.move_up = True
            elif event.key == pygame.K_s:
                left_player.move_down = True

            # Правый игрок
            elif event.key == pygame.K_UP:
                right_player.move_up = True
            elif event.key == pygame.K_DOWN:
                right_player.move_down = True

        # При отпускании клавиши...
        elif event.type == pygame.KEYUP:
            # Левый игрок
            if event.key == pygame.K_w:
                left_player.move_up = False
            elif event.key == pygame.K_s:
                left_player.move_down = False

            # Правый игрок
            elif event.key == pygame.K_UP:
                right_player.move_up = False
            elif event.key == pygame.K_DOWN:
                right_player.move_down = False

    # Обновление объектов
    left_player.update()
    right_player.update()
    ball.update(left_player, right_player)

    if ball.rect.right >= 800:
        left_score += 1
        left_player.reset()
        right_player.reset()
        ball.reset()
    if ball.rect.left <= 0:
        right_score += 1
        left_player.reset()
        right_player.reset()
        ball.reset()

    # Отрисовка
    surface.blit(background, (0,0))

    left_player.render(surface)   
    right_player.render(surface)
    ball.render(surface)

    text = f"{left_score}:{right_score}"
    text_image = font.render(text, True, "black" )
    xy = (400 - text_image.get_width()/2, 10)
    surface.blit(text_image,xy )

    window.flip()
    clock.tick(60)
    window.title = "FPS: " + str(round(clock.get_fps()))