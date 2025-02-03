    # Pythis (Tetris in Python)
    #### Video Demo:  [<URL HERE>](https://youtu.be/FUhEVPGTFEY)
    #### Description:
    Project consists of two files, project.py and test_project.py
    ### project.py
    tetrominos holds all the tetromino types in list, with outer loop being figure type, and inner figure being rotation, in 4x4 grid.
    colors hold all possible colors, with first being "", as we use color indexes to mark the occupied cells on the grid. 
    
    The game uses the Tetris logic and consists of five classes: GameState, Tetris, Tetromino, Button, and Next. 
    The main function initializes all the game components and manages the game loop. `GameState` and `Button` 
    are supplementory classes. 
    `GameState` uses Enum to define constants that represent different states of the game (e.g., START, ACTIVE, GAMEOVER).. 
    `Button` is class that creates a button to toggle on/off the music.
    
     Tetromino: This class represents the falling pieces of the game. It can randomly choose its type (from the tetrominos list) 
     and color (from the colors list). The image() method returns the tetromino's type and its current rotation. 
     The rotate() method changes the rotation of the tetromino by going through the inner tetrominos list 
     for the current tetromino type, ensuring that the rotation value stays within bounds 
     using self.rotation = (self.rotation + 1) % len(tetrominos[self.type]).
    
     Tetris: The core game logic. This class initializes the game grid, sets up the current and next tetromino, and manages the game 
     state (score, level, speed). 
     The draw_grid() method draws the grid, checking each cell for tetromino presence. If the tetromino is present, it will draw the corresponding
     color of the figure. 
     The draw_tetromino() method handles the drawing of tetrominos by going through 4x4 grid (by calculating index
     of the cell in 4x4 grid, because it is flatenned to 1D list) to create tetromino parts.
     The intersects() method checks for collisions with the grid borders or other tetrominoes. 
     The stop() method "freezes" a tetromino when it reaches the bottom of the grid. 
     The clear_lines() method clears full rows and adjusts the score. 
     The update_speed() method increases the difficulty by adjusting the game speed as the level progresses. 
     The move_down() method moves the tetromino downward continuously.

     Next: This class is similar to Tetris, but it creates a smaller grid to display the next tetromino. The update_next()
     method is called during each game loop iteration to ensure the next tetromino is correctly shown.

      The main() function is responsible for initializing the game, displaying the menus and drawing necessary text. It enters a while 
      running loop that listens for user inputs (e.g., toggling menus, controlling tetromino movements).
      It also handles transitions between different game states (e.g., from START to ACTIVE to GAMEOVER).
      
      ### test_project.py
      The test_project.py file contains unit tests for the Tetromino, Tetris, and GameState classes. The tests include:
      test_tetromino(): Ensures correct initialization of the tetromino, verifies that the randomly chosen type and color are within the 
      expected range, and checks if the rotate() and image() methods work as expected.
      test_tetris(): Validates the initialization of the Tetris game grid and its core attributes (e.g., rows, columns, state, score).
      test_tetris_move_down(): Verifies that the tetromino moves down as expected in the Tetris game.
      test_tetris_intersects(): Confirms that the intersects() method works correctly when the tetromino reaches 
      the bottom of the grid and ensures collision detection.

