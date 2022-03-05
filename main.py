import pygame
from board import Board

WIDTH = 500
HEIGHT = 500
FPS = 5
COLUMNS = 10
ROWS = 10
SQUARE_SIZE = WIDTH/COLUMNS

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")
pygame.font.init()


def get_click_pos(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return int(row), int(col)


def main():
    game_on = True
    clock = pygame.time.Clock()
    board = Board(window=WINDOW, tile_size=SQUARE_SIZE, height=ROWS, width=COLUMNS, num_bombs=10)

    while game_on:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_click_pos(pos)
                if event.button == 3:
                    board.flag(y=row, x=col)
                elif event.button == 1:
                    board.left_click(y=row, x=col)
            elif event.type == pygame.QUIT:
                game_on = False

        board.draw()
        pygame.display.update()
    pygame.quit()


if __name__ == "__main__":
    main()
