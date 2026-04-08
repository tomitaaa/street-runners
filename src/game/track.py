import pygame
from pygame.math import Vector2
from game.game_object import GameObject


class Track(GameObject):
    def __init__(self):
        super().__init__(Vector2(0.0, 0.0))

        self.outer_rect = pygame.Rect(100, 100, 600, 400)
        self.inner_rect = pygame.Rect(250, 180, 300, 240)

        self.road_color        = (70, 70, 70)
        self.border_color      = (220, 220, 220)
        self.grass_color       = (30, 120, 30)
        self.center_line_color = (240, 220, 80)
        self.start_line_color  = (255, 255, 255)

        self.waypoints: list[Vector2] = [
            Vector2(180.0, 140.0),
            Vector2(620.0, 140.0),
            Vector2(660.0, 220.0),
            Vector2(660.0, 380.0),
            Vector2(620.0, 460.0),
            Vector2(180.0, 460.0),
            Vector2(140.0, 380.0),
            Vector2(140.0, 220.0),
        ]

        self.show_waypoints = False

    # ------------------------------------------------------------------
    def is_on_road(self, position: Vector2) -> bool:
        point = (position.x, position.y)
        return (self.outer_rect.collidepoint(point)
                and not self.inner_rect.collidepoint(point))

    # ------------------------------------------------------------------
    def draw(self, screen):
        screen.fill(self.grass_color)

        pygame.draw.rect(screen, self.road_color,  self.outer_rect)
        pygame.draw.rect(screen, self.grass_color, self.inner_rect)

        pygame.draw.rect(screen, self.border_color, self.outer_rect, 4)
        pygame.draw.rect(screen, self.border_color, self.inner_rect, 4)

        self._draw_center_guides(screen)
        self._draw_start_grid(screen)

        if self.show_waypoints:
            self._draw_waypoints(screen)

    # ------------------------------------------------------------------
    def _draw_center_guides(self, screen):
        """Linha central tracejada em todas as secoes da pista."""
        dash_long  = 30
        dash_short = 6
        gap        = 20

        # reta superior — guias horizontais
        y_top = (self.outer_rect.top + self.inner_rect.top) // 2
        x = self.outer_rect.left
        while x < self.outer_rect.right:
            pygame.draw.rect(screen, self.center_line_color,
                             pygame.Rect(x, y_top - dash_short // 2,
                                         dash_long, dash_short))
            x += dash_long + gap

        # reta inferior — guias horizontais
        y_bot = (self.inner_rect.bottom + self.outer_rect.bottom) // 2
        x = self.outer_rect.left
        while x < self.outer_rect.right:
            pygame.draw.rect(screen, self.center_line_color,
                             pygame.Rect(x, y_bot - dash_short // 2,
                                         dash_long, dash_short))
            x += dash_long + gap

        # lado esquerdo — guias verticais
        x_left = (self.outer_rect.left + self.inner_rect.left) // 2
        y = self.inner_rect.top
        while y < self.inner_rect.bottom:
            pygame.draw.rect(screen, self.center_line_color,
                             pygame.Rect(x_left - dash_short // 2, y,
                                         dash_short, dash_long))
            y += dash_long + gap

        # lado direito — guias verticais
        x_right = (self.inner_rect.right + self.outer_rect.right) // 2
        y = self.inner_rect.top
        while y < self.inner_rect.bottom:
            pygame.draw.rect(screen, self.center_line_color,
                             pygame.Rect(x_right - dash_short // 2, y,
                                         dash_short, dash_long))
            y += dash_long + gap

    def _draw_start_grid(self, screen):
        """Tabuleiro xadrez na linha de largada."""
        sq = 10
        x0 = 168
        y0 = self.outer_rect.top
        y1 = self.inner_rect.top
        rows = (y1 - y0) // sq

        for row in range(rows):
            for col in range(2):
                color = (240, 240, 240) if (row + col) % 2 == 0 else (15, 15, 15)
                pygame.draw.rect(screen, color,
                                 pygame.Rect(x0 + col * sq,
                                             y0 + row * sq, sq, sq))

        # linha fina branca à direita do xadrez
        pygame.draw.rect(screen, self.start_line_color,
                         pygame.Rect(x0 + sq * 2, y0, 3, y1 - y0))

    def _draw_waypoints(self, screen):
        for point in self.waypoints:
            pygame.draw.circle(screen, (255, 80, 80),
                               (int(point.x), int(point.y)), 5)
