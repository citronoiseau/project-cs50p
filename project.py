import pygame
from random import randint, choice

pygame.init()
WIDTH = 500
HEIGHT = 700
tetrominos = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],#I
        [[1, 2, 5, 6]], #O
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]], #T
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], #J
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]], #L
        [[6, 7, 9, 10], [1, 5, 6, 10]], #S
        [[4, 5, 9, 10], [2, 6, 5, 9]], #Z
    ]

COLORS = ["", "blue",  "green", "lightblue", "orange", "purple", "red"]

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
        self.offset_x = (WIDTH - self.columns * self.cell_size) // 2
        self.offset_y = (HEIGHT - self.rows * self.cell_size) // 2

    def new_tetromino(self):
        self.tetromino = Tetromino(3, 0)    
    
    def draw_grid(self, screen):
        for i in range(self.rows):  
            for j in range(self.columns):  
                x = self.offset_x + j * self.cell_size
                y = self.offset_y + i * self.cell_size
                if self.grid[i][j] == 0:
                    pygame.draw.rect(screen, (40, 42, 54), (x, y, self.cell_size, self.cell_size), 1)
                else:
                    color_image = pygame.image.load(f'graphics/{COLORS[self.grid[i][j]]}.png').convert_alpha()
                    color_image = pygame.transform.scale(color_image, (self.cell_size, self.cell_size))
                    screen.blit(color_image, (x, y))

    def draw_tetromino(self, screen):
        if self.tetromino is not None:
            for i in range(4):
                for j in range(4):
                    if i * 4 + j in self.tetromino.image():
                        x = self.offset_x + (self.tetromino.x + j) * self.cell_size
                        y = self.offset_y + (self.tetromino.y + i) * self.cell_size
                        color_image = pygame.image.load(f'graphics/{COLORS[self.tetromino.color]}.png').convert_alpha()
                        color_image = pygame.transform.scale(color_image, (self.cell_size, self.cell_size))
                        screen.blit(color_image, (x, y))

    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetromino.image():
                    if i + self.tetromino.y > self.rows - 1 or \
                            j + self.tetromino.x > self.columns - 1 or \
                            j + self.tetromino.x < 0 or \
                            self.grid[i + self.tetromino.y][j + self.tetromino.x] > 0:
                        return True
        return False

    def stop(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetromino.image():
                    self.grid[i + self.tetromino.y][j + self.tetromino.x] = self.tetromino.color
        self.clear_lines()
        self.new_tetromino()
        if self.intersects():
            self.state = "gameover"

    def clear_lines(self):
        lines_to_clear = 0

        for i in range(1, self.rows):
            empty_cells = 0
            for j in range(self.columns):
                if self.grid[i][j] == 0:
                    empty_cells += 1
            if empty_cells == 0:
                lines_to_clear += 1
                for k in range(i, 1, -1):
                    for j in range(self.columns):
                        self.grid[k][j] = self.grid[k-1][j]
        self.score += lines_to_clear ** 2 

    def move_down(self):
        self.tetromino.y += 1
        if self.intersects():
            self.tetromino.y -= 1
            self.stop()  

    def update(self):
        if self.tetromino is None:
            self.new_tetromino()


class Button:
    def __init__(self):
        self.color = (40, 42, 54)
        self.hover_color = (60, 62, 74)
        self.text_color = (129,239,128)     
        self.music_on = False
        self.width = 120
        self.height = 30
        self.x = WIDTH - self.width - 10
        self.y = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.font = pygame.font.Font('Font.ttf', 30)

    def draw_button(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        music_status = 'On' if self.music_on else 'Off'
        text = self.font.render(f'Music: {music_status}', True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def toggle_music(self):
        if self.music_on:
            pygame.mixer.music.stop()  
        else:
            pygame.mixer.music.load('bgmusic.mp3')
            pygame.mixer.music.play(-1)
        self.music_on = not self.music_on


def main():
    screen = pygame.display.set_mode((500, 700))
    pygame.display.set_caption('Tetris')
    
    clock = pygame.time.Clock()
    running = True
    tetris = Tetris(20, 10)
    button = Button()

    #text
    font = pygame.font.Font('Font.ttf', 50)
    #intro screen
    game_name = font.render('TETRIS',False,(129,239,128))
    game_name_rect = game_name.get_rect(center = (WIDTH // 2,80))
    pic = pygame.image.load('graphics/intro.jpg').convert_alpha() 
    pic_scaled =  pygame.transform.scale(pic, (250, 250))
    pic_rec = pic_scaled.get_rect(center = (WIDTH // 2, 400))
    game_message = font.render('Press space to start',False,(129,239,128))
    game_message_rect = game_message.get_rect(center = (WIDTH // 2,200))


    #gameover screen
    game_name_over = font.render('TETRIS',False,(250,65,92))
    game_name_over_rect = game_name.get_rect(center = (WIDTH // 2,80))
    game_over_message = font.render('GAME OVER',False,(250,65,92))
    game_over_message_rect = game_over_message.get_rect(center = (WIDTH // 2, 160))
    restart_message = font.render('Press ESCAPE to restart',False,(250,65,92))
    restart_message_rect = restart_message.get_rect(center = (WIDTH // 2, 300))

    #timer for tetrominos speed
    tetromino_timer = pygame.USEREVENT + 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if tetris.state == "start" and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    tetris.state = "active"
                    pygame.time.set_timer(tetromino_timer, 500)
            if tetris.state == "active":
                if event.type == tetromino_timer:
                    tetris.move_down()
                if event.type == pygame.KEYDOWN:
                    move_x = {pygame.K_a: -1, pygame.K_LEFT: -1, pygame.K_d: 1, pygame.K_RIGHT: 1}
                    if event.key in move_x:
                        previous = tetris.tetromino.x
                        tetris.tetromino.x += move_x[event.key]
                        if tetris.intersects():
                            tetris.tetromino.x = previous
                
                    elif event.key in (pygame.K_w, pygame.K_UP):  # Rotate
                        print("entered rotate")
                        previous = tetris.tetromino.rotation
                        tetris.tetromino.rotate()
                        if tetris.intersects():
                            tetris.tetromino.rotation = previous

                    elif event.key == pygame.K_SPACE and tetris.tetromino:
                        while not tetris.intersects():
                            tetris.tetromino.y += 1
                        tetris.tetromino.y -= 1
                        tetris.stop()  
                             
            if tetris.state == "gameover":
                pygame.time.set_timer(tetromino_timer, 0)   
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        tetris.__init__(20,10)
                        tetris.state = "start"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.rect.collidepoint(event.pos):
                    button.toggle_music()             
                          
        if tetris.state == "active":
            tetris.update()
            screen.fill("black")
            score = tetris.score
            score_message = font.render(f'Score: {score}',False,(129,239,128))
            score_message_rect = score_message.get_rect(center = (WIDTH // 2, 25))
            screen.blit(score_message,score_message_rect)
            tetris.draw_grid(screen)
            tetris.draw_tetromino(screen)


            pygame.display.flip()

    
        if tetris.state == "start": 
            screen.fill((28, 28, 28))
            screen.blit(game_name,game_name_rect)
            screen.blit(game_message,game_message_rect)
            screen.blit(pic_scaled, pic_rec)
            button.draw_button(screen)

        if tetris.state == "gameover":
            screen.fill((28, 28, 28))
            screen.blit(game_name_over,game_name_over_rect)
            screen.blit(game_over_message,game_over_message_rect)
            score_message_rect = score_message.get_rect(center = (WIDTH // 2, 250))
            screen.blit(score_message,score_message_rect)
            screen.blit(restart_message, restart_message_rect)
            

        pygame.display.update()
        clock.tick(60)  

    pygame.quit()

if __name__ == "__main__":
    main()