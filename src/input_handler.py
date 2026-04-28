import pygame


class InputHandler:
    def __init__(self):
        self.left_down = False
        self.right_down = False

    def process_events(self, game) -> bool:
        """
        Returns False if the user requested to quit, True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.left_down = True
                    game.handle_click(event.pos, left=True)
                elif event.button == 3:
                    self.right_down = True
                    game.handle_click(event.pos, left=False)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.left_down = False
                elif event.button == 3:
                    self.right_down = False

        return True