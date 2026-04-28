import pygame


class InputHandler:
    """Handles user input (mouse clicks and keyboard shortcuts)."""

    def __init__(self):
        self.left_down = False
        self.right_down = False

    def process_events(self, game) -> bool:
        """
        Process all input events.
        Returns False if user wants to quit, True otherwise.
        
        Keyboard Shortcuts:
        - H: Give hint (reveal one correct cell)
        - S: Solve (automatically solve entire puzzle)
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle mouse clicks
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.left_down = True
                    game.handle_click(event.pos, left=True)
                elif event.button == 3:  # Right click
                    self.right_down = True
                    game.handle_click(event.pos, left=False)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_down = False
                elif event.button == 3:
                    self.right_down = False

            # Handle keyboard shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Press 'H' for hint
                    game.give_hint()
                elif event.key == pygame.K_s:  # Press 'S' to solve
                    game.solve_puzzle()

        return True