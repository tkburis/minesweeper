from random import sample, seed
import pygame
import easygui


class Tile:  # template class for tiles
    def __init__(self, y, x):
        self.y = y
        self.x = x
        self.flagged = False
        self.opened = False

    def draw(self, y, x, window, tile_size):
        ...


class BlankTile(Tile):
    def draw(self, y, x, window, tile_size):
        if self.opened:
            img = pygame.image.load("assets/blank.png")
        elif self.flagged:
            img = pygame.image.load("assets/flag.png")
        else:
            img = pygame.image.load("assets/tile.png")
        img = pygame.transform.scale(img, (tile_size, tile_size))
        window.blit(img, (x, y))


class NumberedTile(Tile):
    def __init__(self, y, x):
        super().__init__(y, x)
        self.number = 0

    def draw(self, y, x, window, tile_size):
        if self.opened:
            img = pygame.image.load(f"assets/{self.number}.png")
        elif self.flagged:
            img = pygame.image.load("assets/flag.png")
        else:
            img = pygame.image.load("assets/tile.png")
        img = pygame.transform.scale(img, (tile_size, tile_size))
        window.blit(img, (x, y))


class BombTile(Tile):
    def draw(self, y, x, window, tile_size):
        if self.opened:
            img = pygame.image.load("assets/bomb.png")
        elif self.flagged:
            img = pygame.image.load("assets/flag.png")
        else:
            img = pygame.image.load("assets/tile.png")
        img = pygame.transform.scale(img, (tile_size, tile_size))
        window.blit(img, (x, y))


class Board:
    def __init__(self, window, tile_size, height=5, width=5, num_bombs=10):
        self.window = window
        self.tile_size = tile_size
        self.height = height
        self.width = width
        self.num_bombs = num_bombs

        self.game_ended = False

        self.grid: list[list[Tile]] = [[BlankTile(y, x) for x in range(self.width)] for y in range(self.height)]
        self.has_grid_init = False

    def init_grid(self, first_y, first_x):  # don't put a bomb on (first_y, first_x)
        seed()
        all_coords = set((y, x) for y in range(self.height) for x in range(self.width))
        all_coords.remove((first_y, first_x))  # so it doesn't get chosen to be a bomb
        bomb_coords = set(sample(all_coords, self.num_bombs))  # coordinates for bombs

        for (y, x) in bomb_coords:  # set all bombs to BombTile
            self.grid[y][x] = BombTile(y, x)
            for c_y in range(max(0, y-1), min(self.height, y+2)):  # set all neighbours to NumberedTile (and add 1)
                for c_x in range(max(0, x-1), min(self.width, x+2)):
                    if (c_y, c_x) != (y, x):
                        if isinstance(self.grid[c_y][c_x], BlankTile):
                            self.grid[c_y][c_x] = NumberedTile(c_y, c_x)
                            self.grid[c_y][c_x].number += 1
                        elif isinstance(self.grid[c_y][c_x], NumberedTile):
                            self.grid[c_y][c_x].number += 1

    def draw(self):
        for y in range(self.height):
            for x in range(self.width):
                tile = self.grid[y][x]
                pos_y = y * self.tile_size
                pos_x = x * self.tile_size
                tile.draw(pos_y, pos_x, self.window, self.tile_size)

    def check_win(self):  # won if all non-bomb tiles are opened
        return all([t.opened for row in self.grid for t in row if not isinstance(t, BombTile)])

    def flag(self, y, x):
        if not self.game_ended:
            self.grid[y][x].flagged = not self.grid[y][x].flagged  # toggle flag

    def left_click(self, y, x):
        if self.game_ended:
            return

        if not self.has_grid_init:
            self.init_grid(first_y=y, first_x=x)
            self.has_grid_init = True
        visited = set()
        stack = []

        if self.grid[y][x].opened:  # if opened already and left click, at least open up all neighbours as well
            for c_y in range(max(0, y - 1), min(self.height, y + 2)):
                for c_x in range(max(0, x - 1), min(self.width, x + 2)):
                    if not self.grid[c_y][c_x].flagged:
                        visited.add((c_y, c_x))
                        stack.append((c_y, c_x))
        else:  # if not opened already, open only itself at least (if NumberedTile, only it will be opened in the end)
            visited.add((y, x))
            stack.append((y, x))

        while len(stack) > 0:  # DFS
            curr_y, curr_x = stack.pop(-1)
            visited.add((curr_y, curr_x))
            for c_y in range(max(0, curr_y-1), min(self.height, curr_y+2)):
                for c_x in range(max(0, curr_x-1), min(self.width, curr_x+2)):
                    if (c_y, c_x) != (curr_y, curr_x) and (c_y, c_x) not in visited:
                        if not self.grid[c_y][c_x].flagged:
                            if isinstance(self.grid[curr_y][curr_x], BlankTile):  # stop at NumberedTile
                                stack.append((c_y, c_x))

        for (c_y, c_x) in visited:  # opened up all visited tiles
            self.grid[c_y][c_x].opened = True
            if isinstance(self.grid[c_y][c_x], BombTile):
                self.lose()

        if self.check_win():
            self.win()

    def win(self):
        easygui.msgbox("You win", title="You win")
        self.game_ended = True

    def lose(self):
        for y in range(self.height):
            for x in range(self.width):
                if isinstance(self.grid[y][x], BombTile):
                    self.grid[y][x].opened = True
        easygui.msgbox("You lose", title="You lose")
        self.game_ended = True

    def __str__(self):
        ret = ""
        for r in self.grid:
            row = ""
            for tile in r:
                if isinstance(tile, BlankTile):
                    row += "_ "
                elif isinstance(tile, NumberedTile):
                    row += str(tile.number) + ' '
                elif isinstance(tile, BombTile):
                    row += "X "
            ret += row + '\n'
        return ret


if __name__ == "__main__":
    ...
