import pygame
from random import randint, choice

pygame.init()
WIDTH = 500
HEIGHT = 700
tetrominos = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]
COLORS = ["", "blue", "gray", "green", "lightblue", "orange", "purple", "red"]

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = randint(0, len(tetrominos) - 1)
        self.color = randint(1, len(COLORS) - 1) #can't have 0 because grid[x][y] = 0
        self.rotation = 0
    def image(self):
        return tetrominos[self.type][self.rotation]
        
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(tetrominos[self.type])

class Tetris:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = [[0 for _ in range(columns)] for _ in range(rows)]
        self.state = "start"
        self.score = 0
        self.tetromino = None
        self.cell_size = 30

    def new_figure(self):
        self.tetromino = Tetromino(3, 0)    
    
    def draw_grid(self, screen):
        offset_x = (WIDTH - self.columns * self.cell_size) // 2
        offset_y = (HEIGHT - self.rows * self.cell_size) // 2
        for i in range(self.rows):  
            for j in range(self.columns):  
                x = offset_x + j * self.cell_size
                y = offset_y + i * self.cell_size
                if self.grid[i][j] == 0:
                    pygame.draw.rect(screen, (40, 42, 54), (x, y, self.cell_size, self.cell_size), 1)
                else:
                    color_image = pygame.image.load(f'graphics/{COLORS[self.grid[i][j]]}.png').convert_alpha()
                    color_image = pygame.transform.scale(color_image, (self.cell_size, self.cell_size))
                    screen.blit(color_image, (x, y))


    def update(self):
        if self.tetromino is None:
            self.new_figure()
     

            
def main():
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption('Tetris')
    
    clock = pygame.time.Clock()
    running = True
    tetris = Tetris(20, 10)

    #text
    font = pygame.font.Font('Font.ttf', 50)
    game_message = font.render('Press space to start',False,(250,65,92))
    game_message_rect = game_message.get_rect(center = (WIDTH // 2,200))

    #intro screen
    game_name = font.render('TETRIS',False,(250,65,92))
    game_name_rect = game_name.get_rect(center = (WIDTH // 2,80))
    pic = pygame.image.load('graphics/intro.jpg').convert_alpha() 
    pic_scaled =  pygame.transform.scale(pic, (250, 250))
    pic_rec = pic_scaled.get_rect(center = (WIDTH // 2, 400))

    #timer for tetrominos speed
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 2000)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if tetris.state == "start" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    tetris.state = "active"
       
                                 
        if tetris.state == "active":

            tetris.update()

            screen.fill("purple")
            tetris.draw_grid(screen)


            pygame.display.flip()

    
        if tetris.state == "start": 
            screen.fill((28, 28, 28))
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
            screen.blit(pic_scaled, pic_rec)
        
        pygame.display.update()
        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()