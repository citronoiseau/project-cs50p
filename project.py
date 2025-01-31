import pygame
from shapes import get_shapes
from random import randint, choice

pygame.init()
WIDTH = 500
HEIGHT = 700
SHAPES = get_shapes()
COLORS = ["blue", "gray", "green", "lightblue", "orange", "purple", "red"]

class Tetris:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.game_active = False
        self.score = 0

class Tetromino:
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = pygame.image.load(f'graphics/{choice(COLORS)}.png').convert_alpha()
        self.rotation = 0

def main():
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption('Tetris')
    
    clock = pygame.time.Clock()
    running = True
    tetris = Tetris(WIDTH, HEIGHT)

    #text
    font = pygame.font.Font('Font.ttf', 50)
    game_message = font.render('Press space to start',False,(250,65,92))
    game_message_rect = game_message.get_rect(center = (250,200))

    #intro screen
    game_name = font.render('TETRIS',False,(250,65,92))
    game_name_rect = game_name.get_rect(center = (250,80))

    pic = pygame.image.load('graphics/intro.jpg').convert_alpha()  
    pic_rec = pic.get_rect(center = (400,200))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not tetris.game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    tetris.game_active = True
       
                                 
        if tetris.game_active:

            screen.fill("purple")

            # RENDER YOUR GAME HERE

            pygame.display.flip()

    
        else: 
            screen.fill((28, 28, 28))
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
        
        pygame.display.update()
        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()