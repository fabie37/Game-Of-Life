import pygame
import numpy as np
import sys


class GameOfLife:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.reset()

    def reset(self):
        self.grid = np.random.choice([0, 1], size=(
            self.rows, self.cols), p=[0.7, 0.3])
        return self.grid

    def update(self):
        new_grid = np.zeros(self.grid.shape)
        for i in range(self.rows):
            for j in range(self.cols):
                new_grid[i][j] = self.is_alive(i, j)
        self.grid = new_grid
        return self.grid

    def is_alive(self, row, col):

        live_neighbours = 0
        for i in range(row-1, row+2):
            for j in range(col-1, col+2):
                if i < 0 or i >= self.rows or j < 0 or j >= self.cols or (i == row and j == col):
                    continue
                live_neighbours += self.grid[i][j]

        if self.grid[row][col] == 0:
            return self.dead_rules(live_neighbours)
        return self.alive_rules(live_neighbours)

    def dead_rules(self, live_neighbours):
        if live_neighbours == 3:
            return 1
        return 0

    def alive_rules(self, live_neighbours):
        if live_neighbours < 2 or live_neighbours > 3:
            return 0
        return 1


class GridDisplay:
    def __init__(self, width=800, height=800, cell_size=20):
        pygame.init()
        self.width = width
        self.height = height
        self.cell_size = cell_size

        self.cols = width // cell_size
        self.rows = height // cell_size
        self.grid = np.zeros((self.rows, self.cols))

        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("NumPy Grid Display")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)

    def draw_grid(self):
        self.screen.fill(self.BLACK)

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size
                y = row * self.cell_size

                cell_color = self.WHITE if self.grid[row][col] == 1 else self.BLACK
                pygame.draw.rect(self.screen, cell_color,
                                 (x, y, self.cell_size, self.cell_size))

                pygame.draw.rect(self.screen, self.GRAY,
                                 (x, y, self.cell_size, self.cell_size), 1)

    def set_reset(self, reset_function):
        self.reset = reset_function

    def reset_grid(self):
        if self.reset:
            self.grid = self.reset()

    def set_update(self, update_function):
        self.update = update_function

    def update_grid(self):
        if self.update:
            self.grid = self.update()

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_SPACE:
                        self.reset_grid()

            self.draw_grid()
            pygame.display.flip()
            clock.tick(30)
            self.update_grid()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    display = GridDisplay(800, 800, 20)  # 800x800 window with 20x20 cells
    game_of_life = GameOfLife(display.cols, display.rows)
    display.set_update(game_of_life.update)
    display.set_reset(game_of_life.reset)
    display.run()
