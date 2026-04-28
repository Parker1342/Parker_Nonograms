from typing import List, Tuple

import pygame

from config import COLORS, DIMENSIONS, SIZINGS, FONTS


class Renderer:
    def __init__(
        self,
        screen: pygame.Surface,
        row_clues: List[List[int]],
        col_clues: List[List[int]],
        grid_width: int,
        grid_height: int,
    ):
        self.screen = screen
        self.row_clues = row_clues
        self.col_clues = col_clues
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.cell_size = SIZINGS["cell_size"]
        self.clue_panel_size = SIZINGS["clue_panel_size"]
        self.status_height = SIZINGS["status_height"]

        self.grid_origin = self._compute_grid_origin()
        self.static_surface = self._build_static_surface()

    def _compute_grid_origin(self) -> Tuple[int, int]:
        total_width = (
            self.clue_panel_size + self.grid_width * self.cell_size
        )
        total_height = (
            self.clue_panel_size
            + self.grid_height * self.cell_size
            + self.status_height
        )

        win_w = DIMENSIONS["window_width"]
        win_h = DIMENSIONS["window_height"]

        offset_x = (win_w - total_width) // 2
        offset_y = (win_h - total_height) // 2 + self.status_height
        return offset_x + self.clue_panel_size, offset_y

    def _build_static_surface(self) -> pygame.Surface:
        win_w = DIMENSIONS["window_width"]
        win_h = DIMENSIONS["window_height"]
        surface = pygame.Surface((win_w, win_h))
        surface.fill(COLORS["background"])

        self._draw_clue_panels(surface)
        self._draw_grid_lines(surface)
        return surface

    def _draw_clue_panels(self, surface: pygame.Surface):
        # Draw row clues (left)
        for r, clues in enumerate(self.row_clues):
            text = " ".join(map(str, clues))
            img = FONTS["clue"].render(text, True, COLORS["text"])
            x = self.grid_origin[0] - 10
            y = self.grid_origin[1] + r * self.cell_size + self.cell_size // 2
            rect = img.get_rect(right=x, centery=y)
            surface.blit(img, rect)

        # Draw column clues (top)
        for c, clues in enumerate(self.col_clues):
            text = "\n".join(map(str, clues))
            lines = text.split("\n")
            x = self.grid_origin[0] + c * self.cell_size + self.cell_size // 2
            base_y = self.grid_origin[1] - 10
            for i, line in enumerate(reversed(lines)):
                img = FONTS["clue"].render(line, True, COLORS["text"])
                rect = img.get_rect(centerx=x, bottom=base_y - i * 18)
                surface.blit(img, rect)

    def _draw_grid_lines(self, surface: pygame.Surface):
        x0, y0 = self.grid_origin
        w = self.grid_width * self.cell_size
        h = self.grid_height * self.cell_size

        for r in range(self.grid_height + 1):
            y = y0 + r * self.cell_size
            thickness = (
                SIZINGS["bold_line_thickness"]
                if r % 5 == 0
                else SIZINGS["line_thickness"]
            )
            color = COLORS["grid_bold"] if r % 5 == 0 else COLORS["grid"]
            pygame.draw.line(surface, color, (x0, y), (x0 + w, y), thickness)

        for c in range(self.grid_width + 1):
            x = x0 + c * self.cell_size
            thickness = (
                SIZINGS["bold_line_thickness"]
                if c % 5 == 0
                else SIZINGS["line_thickness"]
            )
            color = COLORS["grid_bold"] if c % 5 == 0 else COLORS["grid"]
            pygame.draw.line(surface, color, (x, y0), (x, y0 + h), thickness)

    def draw_status(self, text: str):
        img = FONTS["status"].render(text, True, COLORS["status"])
        rect = img.get_rect(
            centerx=DIMENSIONS["window_width"] // 2,
            top=5,
        )
        self.screen.blit(img, rect)

    def draw(self, grid_state):
        # Blit static background (grid + clues)
        self.screen.blit(self.static_surface, (0, 0))

        # Draw dynamic cells (filled and X marks)
        x0, y0 = self.grid_origin
        for r in range(grid_state.height):
            for c in range(grid_state.width):
                state = grid_state.get_cell_state(r, c)
                cell_rect = pygame.Rect(
                    x0 + c * self.cell_size + 1,
                    y0 + r * self.cell_size + 1,
                    self.cell_size - 2,
                    self.cell_size - 2,
                )
                if state == 1:
                    pygame.draw.rect(
                        self.screen, COLORS["filled"], cell_rect
                    )
                elif state == -1:
                    # Draw X mark
                    pygame.draw.line(
                        self.screen,
                        COLORS["marked"],
                        cell_rect.topleft,
                        cell_rect.bottomright,
                        2,
                    )
                    pygame.draw.line(
                        self.screen,
                        COLORS["marked"],
                        cell_rect.topright,
                        cell_rect.bottomleft,
                        2,
                    )

    def screen_to_grid(self, pos) -> Tuple[int, int]:
        x, y = pos
        x0, y0 = self.grid_origin
        if x < x0 or y < y0:
            return -1, -1
        col = (x - x0) // self.cell_size
        row = (y - y0) // self.cell_size
        if col < 0 or col >= self.grid_width or row < 0 or row >= self.grid_height:
            return -1, -1
        return row, col
