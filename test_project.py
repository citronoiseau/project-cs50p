from project import Tetromino, Tetris, GameState

tetrominos = [
    [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
    [[1, 2, 5, 6]],  # O
    [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # T
    [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # J
    [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # L
    [[6, 7, 9, 10], [1, 5, 6, 10]],  # S
    [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z
]

COLORS = ["", "blue", "green", "lightblue", "orange", "purple", "red"]


def test_tetromino():
    tetromino = Tetromino(3, 0)
    assert tetromino.x == 3
    assert tetromino.y == 0
    assert 0 <= tetromino.type < len(tetrominos)
    assert 1 <= tetromino.color < len(COLORS)

    tetromino.rotate()
    assert tetromino.rotation == 1

    tetromino = Tetromino(3, 0)
    assert tetromino.image() in tetrominos[tetromino.type]


def test_tetris():
    tetris = Tetris(20, 10)
    assert tetris.rows == 20
    assert tetris.columns == 10
    assert tetris.state == GameState.START
    assert tetris.score == 0
    assert isinstance(tetris.tetromino[0], Tetromino)


def test_tetris_move_down():
    game = Tetris(20, 10)
    initial_y = game.tetromino[0].y
    game.move_down()
    assert game.tetromino[0].y == initial_y + 1 or game.state == "gameover"


def test_tetris_intersects():
    game = Tetris(20, 10)
    game.tetromino[0].y = game.rows - 1
    assert game.intersects() is True
