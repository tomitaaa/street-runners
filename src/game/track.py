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
        self.start_line_color = (255, 255, 255)

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

    def is_on_road(self, position: Vector2) -> bool:
        point = (position.x, position.y)
        return self.outer_rect.collidepoint(point) and not self.inner_rect.collidepoint(point)

    def draw(self, screen):
        screen.fill(self.grass_color)

        pygame.draw.rect(screen, self.road_color, self.outer_rect)
        pygame.draw.rect(screen, self.grass_color, self.inner_rect)

        pygame.draw.rect(screen, self.border_color, self.outer_rect, 4)
        pygame.draw.rect(screen, self.border_color, self.inner_rect, 4)

        self.draw_center_guides(screen)
        self.draw_start_line(screen)

        if self.show_waypoints:
            self.draw_waypoints(screen)

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

    def draw_start_line(self, screen):
        pygame.draw.rect(screen, self.start_line_color, pygame.Rect(170, 120, 12, 40))

    def draw_waypoints(self, screen):
        for point in self.waypoints:
            pygame.draw.circle(screen, (255, 80, 80), (int(point.x), int(point.y)), 5)