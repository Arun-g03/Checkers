import pygame
from Player import Piece, Pawn, King
from Constants import BLACK, WHITE, END_ROW_BLACK, END_ROW_WHITE

class Tile:
    def __init__(self, row, col, tile_size):
        # Initialize tile properties
        self.row = row
        self.col = col
        self.piece = None
        self.selected = False
        self.tile_size = tile_size

    def set_piece(self, piece):
        # Set a piece on the tile and update the piece's tile reference
        self.piece = piece
        if piece:
            piece.tile = self

    def draw(self, screen):
        # Define colors for the tiles
        DARK_BROWN, LIGHT_BROWN = (139, 69, 19), (222, 184, 135)
        tile_color = DARK_BROWN if (self.row + self.col) % 2 == 0 else LIGHT_BROWN
        outline_color = (255, 255, 0)

        # Draw the tile
        pygame.draw.rect(screen, tile_color, (self.col * self.tile_size, self.row * self.tile_size + 100, self.tile_size, self.tile_size))
        
        # Draw selection outline if the tile is selected
        if self.selected:
            pygame.draw.rect(screen, outline_color, (self.col * self.tile_size, self.row * self.tile_size + 100, self.tile_size, self.tile_size), 5)
        
        # Draw the piece if there is one on the tile
        if self.piece:
            self.piece.draw(screen, self.col * self.tile_size + self.tile_size // 2, self.row * self.tile_size + self.tile_size // 2 + 100)


class Board:
    def __init__(self, tile_size=100):
        # Initialize board properties
        self.tile_size = tile_size
        self.tiles = [[Tile(row, col, tile_size) for col in range(8)] for row in range(8)]
        self.initialize_pieces()
        self.current_turn = BLACK  # Starting turn
        self.previous_turn = None  # Previous move
        self.selected_piece = None
        self.player1_points = 0
        self.player2_points = 0
        self.font = pygame.font.Font(None, 36)

    def initialize_pieces(self):
        # Place initial pieces on the board
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.tiles[row][col].set_piece(Pawn(row, col, WHITE))
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    self.tiles[row][col].set_piece(Pawn(row, col, BLACK))

    def get_turn_name(self):
        # Get the name of the current player
        return "Player 1" if self.current_turn == BLACK else "Player 2"

    def draw(self, screen):
        # Draw the board
        for row in range(8):
            for col in range(8):
                self.tiles[row][col].draw(screen)
        
        # Draw the top bar
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, 800, 100))  # Light grey bar
        
        # Draw player points
        player1_points_text = self.font.render(f"Player 1: {self.player1_points}", True, (0, 0, 0))
        player2_points_text = self.font.render(f"Player 2: {self.player2_points}", True, (0, 0, 0))
        screen.blit(player1_points_text, (10, 35))
        screen.blit(player2_points_text, (600, 35))
        
        # Draw turn indicator
        turn_indicator_text = self.font.render(f"Turn: {self.get_turn_name()}", True, (0, 0, 0))
        screen.blit(turn_indicator_text, (350, 35))

    def handle_events(self, events):
        # Handle pygame events
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row = (mouse_y - 100) // self.tile_size
                clicked_col = mouse_x // self.tile_size
                if 0 <= clicked_row < 8 and 0 <= clicked_col < 8:
                    self.handle_click(clicked_row, clicked_col)

    def handle_click(self, row, col):
        # Handle user clicks on the board
        clicked_tile = self.tiles[row][col]
        clicked_tile.selected = not clicked_tile.selected

        if clicked_tile.piece and clicked_tile.piece.color == self.current_turn:
            if self.selected_piece:
                self.selected_piece.tile.selected = False

            self.selected_piece = clicked_tile.piece
        elif self.selected_piece:
            self.try_move(self.selected_piece, row, col)

    def try_move(self, piece, new_row, new_col):
        # Attempt to move a piece
        if piece.is_valid_move(new_row, new_col, self.tiles):
            self.move_piece(piece, new_row, new_col)
            if abs(new_row - piece.row) == 2 and abs(new_col - piece.col) == 2:
                self.capture_opponent(piece, new_row, new_col)

            # Check if the piece should be promoted to a king
            if piece.color == BLACK and new_row == END_ROW_BLACK:
                piece.make_king()
            elif piece.color == WHITE and new_row == END_ROW_WHITE:
                piece.make_king()

            # Switch turns
            self.current_turn = WHITE if self.current_turn == BLACK else BLACK
            self.selected_piece = None

    def move_piece(self, piece, new_row, new_col):
        # Move a piece to a new position
        self.tiles[piece.row][piece.col].set_piece(None)
        piece.row = new_row
        piece.col = new_col
        self.tiles[new_row][new_col].set_piece(piece)

    def is_piece_attacked(self, piece):
        # Check if a piece is under attack
        opponent_color = WHITE if piece.color == BLACK else BLACK

        for row in range(8):
            for col in range(8):
                current_tile = self.tiles[row][col]
                opponent_piece = current_tile.piece

                if opponent_piece and opponent_piece.color == opponent_color:
                    if opponent_piece.is_valid_move(piece.row + 1, piece.col + 1, self.tiles) or \
                       opponent_piece.is_valid_move(piece.row + 1, piece.col - 1, self.tiles) or \
                       (opponent_piece.king and (opponent_piece.is_valid_move(piece.row - 1, piece.col + 1, self.tiles) or
                                                  opponent_piece.is_valid_move(piece.row - 1, piece.col - 1, self.tiles))):
                        return True

        return False

    def capture_opponent(self, piece, new_row, new_col):
        # Capture an opponent's piece
        opponent_color = WHITE if piece.color == BLACK else BLACK
        mid_row = (piece.row + new_row) // 2
        mid_col = (piece.col + new_col) // 2

        if abs(new_row - piece.row) == 2 and abs(new_col - piece.col) == 2:
            if (
                0 <= mid_row < 8
                and 0 <= mid_col < 8
                and self.tiles[mid_row][mid_col].piece
                and self.tiles[mid_row][mid_col].piece.color == opponent_color
            ):
                self.tiles[mid_row][mid_col].set_piece(None)
                if opponent_color == WHITE:
                    self.player1_points += 1
                else:
                    self.player2_points += 1

    def check_winner(self):
        # Check if there's a winner or if the game is a draw
        player1_pieces = [tile.piece for row in self.tiles for tile in row if tile.piece and tile.piece.color == BLACK]
        player2_pieces = [tile.piece for row in self.tiles for tile in row if tile.piece and tile.piece.color == WHITE]

        def has_valid_moves(player_pieces):
            for piece in player_pieces:
                if piece.get_possible_moves(self.tiles) or piece.get_possible_captures(self.tiles):
                    return True
            return False

        if not player1_pieces and not player2_pieces:
            return 0

        if not player1_pieces or not has_valid_moves(player1_pieces):
            return WHITE
        elif not player2_pieces or not has_valid_moves(player2_pieces):
            return BLACK

        if not has_valid_moves(player1_pieces) and not has_valid_moves(player2_pieces):
            return "Stalemate"

        return None
