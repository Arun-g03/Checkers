import random

class AIPlayer:
    def __init__(self, color):
        # Initialize the AI player with a color (black or white)
        self.color = color

    def make_move(self, game_state):
        possible_moves = []
        possible_captures = []

        # Iterate through all tiles on the board
        for row in range(8):
            for col in range(8):
                tile = game_state.board.tiles[row][col]
                # Check if the tile has a piece of the AI's color
                if tile.piece and tile.piece.color == self.color:
                    # Get all possible moves and captures for the piece
                    moves = tile.piece.get_possible_moves(game_state.board.tiles)
                    captures = tile.piece.get_possible_captures(game_state.board.tiles)
                    # Add moves and captures to their respective lists
                    for move in moves:
                        possible_moves.append((tile.piece, move[0], move[1]))
                    for capture in captures:
                        possible_captures.append((tile.piece, capture[0], capture[1]))

        # Choose a move, prioritizing captures over normal moves
        if possible_captures:
            # Randomly select a capture move if available
            piece, new_row, new_col = random.choice(possible_captures)
        elif possible_moves:
            # Randomly select a normal move if no captures are available
            piece, new_row, new_col = random.choice(possible_moves)
        else:
            # No valid moves available, end the turn
            return

        # Execute the chosen move
        game_state.try_move(piece, new_row, new_col)
