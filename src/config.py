import pygame

pygame.init()

# Colors grouped in a dictionary
COLORS = {
    "background": (30, 30, 30),
    "grid": (200, 200, 200),
    "grid_bold": (255, 255, 255),
    "filled": (60, 160, 220),
    "marked": (200, 80, 80),
    "text": (240, 240, 240),
    "status": (255, 255, 0),
}

# Dimensions grouped in a dictionary
DIMENSIONS = {
    "grid_width": 10,
    "grid_height": 10,
    "window_width": 800,
    "window_height": 800,
}

# Sizings grouped in a dictionary
SIZINGS = {
    "cell_size": 32,
    "line_thickness": 1,
    "bold_line_thickness": 3,
    "clue_margin": 10,
    "clue_panel_size": 150,
    "status_height": 40,
}

FONT_NAME = "arial"
FPS = 60

# Preload fonts
FONTS = {
    "clue": pygame.font.SysFont(FONT_NAME, 18),
    "status": pygame.font.SysFont(FONT_NAME, 22),
}
