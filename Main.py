import pygame
from Game import Game
from AI_Player import AIPlayer
from Constants import WIDTH, HEIGHT, BLACK, WHITE

class Main:
    def __init__(self):
        # Initialize Pygame and set up the game window
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
        pygame.display.set_caption("Checkers Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)  # Font for displaying text
        self.mode = None  # Mode will be set by the menu

    def run(self):
        # Main game loop
        while self.mode is None:
            self.show_menu()
        self.game_loop()

    def show_menu(self):
        # Display the main menu and handle user selection
        self.screen.fill((255, 255, 255))  # Fill the screen with white

        # Draw menu options
        pvp_text = self.font.render("Player vs Player", True, (0, 0, 0))
        pvai_text = self.font.render("Player vs AI", True, (0, 0, 0))
        self.screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(pvai_text, (WIDTH // 2 - pvai_text.get_width() // 2, HEIGHT // 2 + 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Check if Player vs Player option is clicked
                if WIDTH // 2 - pvp_text.get_width() // 2 <= mouse_x <= WIDTH // 2 + pvp_text.get_width() // 2:
                    if HEIGHT // 2 - 50 <= mouse_y <= HEIGHT // 2 - 50 + pvp_text.get_height():
                        self.mode = 'pvp'
                        self.game = Game(self.screen, ai_mode=False)
                    # Check if Player vs AI option is clicked
                    elif HEIGHT // 2 + 50 <= mouse_y <= HEIGHT // 2 + 50 + pvai_text.get_height():
                        self.mode = 'pvai'
                        self.game = Game(self.screen, ai_mode=True, ai_player=AIPlayer(BLACK))

    def game_loop(self):
        # Main game loop for handling events and updating the game state
        running = True
        while running:
            events = pygame.event.get()  # Get the current events
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_mouse_click()  # Call the handle_mouse_click method

            # Call Game.update with events
            self.game.update(events)

            pygame.display.flip()
            self.clock.tick(60)

    def handle_mouse_click(self):
        # Handles mouse click events by translating click position to board coordinates and passing them to the game.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        clicked_row = (mouse_y - 100) // self.game.state.board.tile_size
        clicked_col = mouse_x // self.game.state.board.tile_size
        self.game.handle_click(clicked_row, clicked_col)

if __name__ == "__main__":
    main = Main()
    main.run()
