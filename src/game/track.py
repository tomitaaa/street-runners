import pygame
from pygame.math import Vector2
from game.game_object import GameObject


class Track(GameObject):
    def __init__(self):
        super().__init__(Vector2(0.0, 0.0))

        self.outer_rect = pygame.Rect(100, 100, 600, 400)
        self.inner_rect = pygame.Rect(250, 180, 300, 240)

        self.road_color = (70, 70, 70)
        self.border_color = (220, 220, 220)
        self.grass_color = (30, 120, 30)
        self.center_line_color = (240, 220, 80)

    def is_on_road(self, position: Vector2) -> bool:
        """
        Retorna True se a posição estiver na pista:
        - dentro do retângulo externo
        - fora do retângulo interno
        """
        point = (position.x, position.y)
        return self.outer_rect.collidepoint(point) and not self.inner_rect.collidepoint(point)

    def draw(self, screen):
        screen.fill(self.grass_color)

        pygame.draw.rect(screen, self.road_color, self.outer_rect)
        pygame.draw.rect(screen, self.grass_color, self.inner_rect)

        pygame.draw.rect(screen, self.border_color, self.outer_rect, 4)
        pygame.draw.rect(screen, self.border_color, self.inner_rect, 4)

        self.draw_center_guides(screen)

    def draw_center_guides(self, screen):
        dash_w = 30
        dash_h = 6
        gap = 20

        y_top = 140
        x = 140
        while x < 660:
            if not self.inner_rect.collidepoint(x, y_top):
                pygame.draw.rect(
                    screen,
                    self.center_line_color,
                    pygame.Rect(x, y_top, dash_w, dash_h)
                )
            x += dash_w + gap

        y_bottom = 454
        x = 140
        while x < 660:
            if not self.inner_rect.collidepoint(x, y_bottom):
                pygame.draw.rect(
                    screen,
                    self.center_line_color,
                    pygame.Rect(x, y_bottom, dash_w, dash_h)
                )
            x += dash_w + gap