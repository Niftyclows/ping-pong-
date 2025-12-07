import pygame 

class Sprite:
    def __init__(self, center, image):
        self.image = image 
        self.rect = image.get_frect()
        self.rect.center = center 

    def render(self, surface):
        surface.blit(self.image, self.rect)

         



window = pygame.Window('Ping Pong', (800, 600),pygame.WINDOWPOS_CENTERED)     

surface = window.get_surface()
clock = pygame.Clock()

image = pygame.Surface( (40, 100) )
image.fill('pink')
left_player = Sprite( (40, 300), image  )

running = True 
while running:
    # обработка событий 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # обновление обьектов 

    # отрисовка 
    surface.fill('white')
    left_player.render(surface)
    left_player.rect.x += 1



    window.flip()
    clock.tick(60)
    window.title = 'FPS:'+ str(round(clock.get_fps()))
