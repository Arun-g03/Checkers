from Visualiser import Board
from Constants import BLACK, WHITE

class GameState:
    def __init__(self):
        # Initialize the game board and game state
        self.board = Board(tile_size=100)
        self.current_turn = BLACK
        self.previous_turn = None
        self.player1_points = 0
        self.player2_points = 0
        self.selected_piece = None

    def switch_turn(self):
        # Switch the current turn between BLACK and WHITE
        self.current_turn = WHITE if self.current_turn == BLACK else BLACK

    def increment_points(self, color):
        # Increment points for the player who captured a piece
        if color == WHITE:
            self.player1_points += 1
        else:
            self.player2_points += 1

    def is_game_over(self):
        # Check if the game is over and return the winner or game state
        player1_pieces = [tile.piece for row in self.board.tiles for tile in row if tile.piece and tile.piece.color == BLACK]
        player2_pieces = [tile.piece for row in self.board.tiles for tile in row if tile.piece and tile.piece.color == WHITE]

        def has_valid_moves(player_pieces):
            # Check if a player has any valid moves left
            for piece in player_pieces:
                if piece.get_possible_moves(self.board.tiles) or piece.get_possible_captures(self.board.tiles):
                    return True
            return False

        # Check various game-over conditions
        if not player1_pieces and not player2_pieces:
            return 0  # Draw (no pieces left for both players)

        if not player1_pieces or not has_valid_moves(player1_pieces):
            return WHITE  # White wins
        elif not player2_pieces or not has_valid_moves(player2_pieces):
            return BLACK  # Black wins

        if not has_valid_moves(player1_pieces) and not has_valid_moves(player2_pieces):
            return "Stalemate"  # No valid moves for both players

        return None  # Game is not over

    def handle_click(self, row, col):
        # Handle user click on the board
        clicked_tile = self.board.tiles[row][col]
        clicked_tile.selected = not clicked_tile.selected

        if clicked_tile.piece and clicked_tile.piece.color == self.current_turn:
            # Select the clicked piece
            if self.selected_piece:
                self.selected_piece.tile.selected = False

            self.selected_piece = clicked_tile.piece
        elif self.selected_piece:
            # Try to move the selected piece to the clicked tile
            self.try_move(self.selected_piece, row, col)

    def try_move(self, piece, new_row, new_col):
        # Attempt to move a piece to a new position
        if piece.is_valid_move(new_row, new_col, self.board.tiles):
            self.move_piece(piece, new_row, new_col)
            if abs(new_row - piece.row) == 2 and abs(new_col - piece.col) == 2:
                # Capture opponent's piece if it's a jump move
                self.capture_opponent(piece, new_row, new_col)

            # Check if the piece should be promoted to a king
            if piece.color == BLACK and new_row == 7:
                piece.make_king()
            elif piece.color == WHITE and new_row == 0:
                piece.make_king()

            self.switch_turn()
            self.selected_piece = None

    def move_piece(self, piece, new_row, new_col):
        # Move a piece to a new position on the board
        self.board.tiles[piece.row][piece.col].set_piece(None)
        piece.row = new_row
        piece.col = new_col
        self.board.tiles[new_row][new_col].set_piece(piece)

    def capture_opponent(self, piece, new_row, new_col):
        # Capture an opponent's piece during a jump move
        opponent_color = WHITE if piece.color == BLACK else BLACK
        mid_row = (piece.row + new_row) // 2
        mid_col = (piece.col + new_col) // 2

        if abs(new_row - piece.row) == 2 and abs(new_col - piece.col) == 2:
            if (
                0 <= mid_row < 8
                and 0 <= mid_col < 8
                and self.board.tiles[mid_row][mid_col].piece
                and self.board.tiles[mid_row][mid_col].piece.color == opponent_color
            ):
                self.board.tiles[mid_row][mid_col].set_piece(None)
                self.increment_points(opponent_color)


class Game:
    def __init__(self, screen, ai_mode=False, ai_player=None):
        # Initialize the game with screen, AI mode, and AI player
        self.screen = screen
        self.state = GameState()
        self.ai_mode = ai_mode
        self.ai_player = ai_player

    def update(self, events):
        # Update the game state and handle events
        self.state.board.draw(self.screen)
        self.state.board.handle_events(events)

        if self.ai_mode and self.state.current_turn == self.ai_player.color:
            # Make AI move if it's AI's turn
            self.ai_player.make_move(self.state)

    def handle_click(self, row, col):
        # Handle user click on the game board
        self.state.handle_click(row, col)
