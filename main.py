import pygame
import random

# Size of board
board_width = 90
board_height = 60
screen_width = 600
screen_height = 400


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [False] * width * height
        self.x_scale = screen_width / width
        self.y_scale = screen_height / height

    def get_cell(self, row, col) -> bool:
        return self.board[(self.width * row) + col]

    def set_cell(self, row, col, value: bool):
        self.board[(self.width * row) + col] = value

    def draw(self, display: pygame.Surface):
        for row in range(0, self.height):
            for col in range(0, self.width):
                if self.get_cell(row, col):
                    display.fill((0, 64, 255),
                                 rect=(self.x_scale * col, self.y_scale * row, self.x_scale, self.y_scale))

    def randomize(self):
        for row in range(0, self.height):
            for col in range(0, self.width):
                self.board[self.width * row + col] = random.randint(0, 1) == 1

    def neighbour_count(self, row, col) -> int:
        count = 0
        if row > 0 and col > 0 and self.get_cell(row - 1, col - 1):
            count += 1
        if row > 0 and self.get_cell(row - 1, col):
            count += 1
        if row > 0 and col < (self.width - 1) and self.get_cell(row - 1, col + 1):
            count += 1
        if col > 0 and self.get_cell(row, col - 1):
            count += 1
        if col < (self.width - 1) and self.get_cell(row, col + 1):
            count += 1
        if row < (self.height - 1) and col > 0 and self.get_cell(row + 1, col - 1):
            count += 1
        if row < (self.height - 1) and self.get_cell(row + 1, col):
            count += 1
        if row < (self.height - 1) and col < (self.width - 1) and self.get_cell(row + 1, col + 1):
            count += 1
        return count

    def do_generation(self) -> int:
        changes = 0
        new_board = [False] * self.width * self.height
        for row in range(0, self.height):
            for col in range(0, self.width):
                neighbour_count = self.neighbour_count(row, col)
                if self.get_cell(row, col):
                    new_value = neighbour_count == 2 or neighbour_count == 3
                else:
                    new_value = neighbour_count == 3
                new_board[(self.width * row) + col] = new_value
                if new_value != self.get_cell(row, col):
                    changes += 1
        self.board = new_board
        return changes

def main():
    pygame.init()
    pygame.display.set_caption('Life')

    screen = pygame.display.set_mode((screen_width, screen_height))

    board = Board(board_width, board_height)
    board.randomize()

    background_surface = pygame.Surface((screen_width, screen_height))
    background_surface.fill((0, 0, 0))

    running = True
    generation_count = 0
    while running:
        screen.blit(background_surface, dest=(0, 0))
        board.draw(screen)
        pygame.display.flip()
        generation_count += 1
        if board.do_generation() < 60 or generation_count > 5000:
            board.randomize()
            generation_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

main()
