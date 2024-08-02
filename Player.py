import pygame
from Constants import BLACK, WHITE

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.selected = False
        self.tile = None

    def make_king(self):
        self.king = True

    def draw(self, screen, x, y):
        radius = 40
        king_radius = 20

        if self.king:
            pygame.draw.circle(screen, (255, 255, 255), (x, y), king_radius)
        else:
            if self.selected:
                # Draw a yellow border around the selected piece
                pygame.draw.circle(screen, (255, 255, 0), (x, y), radius + 5)
            pygame.draw.circle(screen, self.color, (x, y), radius)

    def is_valid_move(self, new_row, new_col, tiles):
        raise NotImplementedError("Subclasses must implement is_valid_move")

    def get_possible_moves(self, tiles):
        raise NotImplementedError("Subclasses must implement get_possible_moves")

    def get_possible_captures(self, tiles):
        raise NotImplementedError("Subclasses must implement get_possible_captures")


class Pawn(Piece):
    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.color, (x, y), 40)

    def is_valid_move(self, new_row, new_col, tiles):
        # Determine the direction of movement based on the piece color
        direction = 1 if self.color == WHITE else -1  # WHITE moves up, BLACK moves down

        # Check for a regular move (one step diagonally)
        if (new_row - self.row) == direction and abs(new_col - self.col) == 1:
            return tiles[new_row][new_col].piece is None

        # Check for a capture move (two steps diagonally)
        elif (new_row - self.row) == 2 * direction and abs(new_col - self.col) == 2:
            mid_row = (self.row + new_row) // 2
            mid_col = (self.col + new_col) // 2
            opponent_color = WHITE if self.color == BLACK else BLACK
            return (
                0 <= mid_row < 8
                and 0 <= mid_col < 8
                and tiles[mid_row][mid_col].piece
                and tiles[mid_row][mid_col].piece.color == opponent_color
            )
        return False

    def get_possible_moves(self, tiles):
        direction = 1 if self.color == WHITE else -1
        moves = []

        # Check for possible regular moves
        if 0 <= self.row + direction < 8:
            for col_offset in [-1, 1]:
                new_col = self.col + col_offset
                if 0 <= new_col < 8:
                    if tiles[self.row + direction][new_col].piece is None:
                        moves.append((self.row + direction, new_col))
        
        return moves

    def get_possible_captures(self, tiles):
        direction = 1 if self.color == WHITE else -1
        captures = []

        # Check for possible capture moves
        if 0 <= self.row + 2 * direction < 8:
            for col_offset in [-2, 2]:
                new_col = self.col + col_offset
                if 0 <= new_col < 8:
                    mid_row = (self.row + self.row + 2 * direction) // 2
                    mid_col = (self.col + new_col) // 2
                    opponent_color = WHITE if self.color == BLACK else BLACK
                    if (
                        tiles[self.row + 2 * direction][new_col].piece is None
                        and tiles[mid_row][mid_col].piece
                        and tiles[mid_row][mid_col].piece.color == opponent_color
                    ):
                        captures.append((self.row + 2 * direction, new_col))
        
        return captures


class King(Piece):
    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.color, (x, y), 40)
        pygame.draw.circle(screen, WHITE, (x, y), 20)

    def is_valid_move(self, new_row, new_col, tiles):
        # Check if the move is diagonal
        if abs(new_row - self.row) == abs(new_col - self.col):
            row_direction = 1 if new_row > self.row else -1
            col_direction = 1 if new_col > self.col else -1

            current_row, current_col = self.row, self.col
            # Check if the path is clear
            while current_row != new_row and current_col != new_col:
                current_row += row_direction
                current_col += col_direction

                if 0 <= current_row < 8 and 0 <= current_col < 8:
                    if tiles[current_row][current_col].piece is not None:
                        return False

            return tiles[new_row][new_col].piece is None

        return False

    def get_possible_moves(self, tiles):
        moves = []
        # Check all diagonal directions
        for row_offset in [-1, 1]:
            for col_offset in [-1, 1]:
                new_row, new_col = self.row + row_offset, self.col + col_offset
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    if tiles[new_row][new_col].piece is None:
                        moves.append((new_row, new_col))
                    else:
                        break
                    new_row += row_offset
                    new_col += col_offset
        return moves

    def get_possible_captures(self, tiles):
        captures = []
        # Check all diagonal directions for possible captures
        for row_offset in [-1, 1]:
            for col_offset in [-1, 1]:
                new_row, new_col = self.row + 2 * row_offset, self.col + 2 * col_offset
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    mid_row, mid_col = (self.row + new_row) // 2, (self.col + new_col) // 2
                    opponent_color = WHITE if self.color == BLACK else BLACK
                    if (
                        tiles[new_row][new_col].piece is None
                        and tiles[mid_row][mid_col].piece
                        and tiles[mid_row][mid_col].piece.color == opponent_color
                    ):
                        captures.append((new_row, new_col))
                    new_row += 2 * row_offset
                    new_col += 2 * col_offset
        return captures
