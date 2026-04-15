import pygame
from pygame.math import Vector2
from core.game_object import GameObject


class DebugHUD(GameObject):
    def __init__(self, car, track, clock, cars, total_laps: int = 3):
        super().__init__(Vector2(0.0, 0.0))

        self.car = car
        self.track = track
        self.clock = clock
        self.cars = cars
        self.total_laps = total_laps

        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 16)
        self.title_font = pygame.font.SysFont("consolas", 18, bold=True)

        self.color = (255, 255, 255)
        self.panel_color = (0, 0, 0, 160)

    def draw_text(self, screen, text, x, y, font=None, color=None):
        if font is None:
            font = self.font
        if color is None:
            color = self.color

        surface = font.render(text, True, color)
        screen.blit(surface, (x, y))

    def draw_panel(self, screen, x, y, width, height):
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill(self.panel_color)
        screen.blit(panel, (x, y))

    def get_standings(self):
        return sorted(self.cars, key=lambda car: car.get_progress_score(), reverse=True)

    def draw(self, screen):
        speed = self.car.velocity.length()
        pos = self.car.position
        angle = self.car.angle
        on_road = self.track.is_on_road(self.car.position)
        fps = self.clock.get_fps()

        standings = self.get_standings()
        player_position = standings.index(self.car) + 1

        # painel esquerdo: debug
        self.draw_panel(screen, 10, 10, 260, 130)
        self.draw_text(screen, "DEBUG", 20, 18, font=self.title_font)

        debug_lines = [
            f"FPS: {fps:.1f}",
            f"Speed: {speed:.1f}",
            f"Angle: {angle:.1f}",
            f"Position: ({pos.x:.1f}, {pos.y:.1f})",
            f"On Road: {on_road}",
        ]

        y = 45
        for line in debug_lines:
            self.draw_text(screen, line, 20, y)
            y += 18

        # painel direito: corrida
        standings_height = 110 + len(self.cars) * 18
        self.draw_panel(screen, 520, 10, 270, standings_height)

        self.draw_text(screen, "RACE INFO", 530, 18, font=self.title_font)
        self.draw_text(screen, f"Player: {self.car.name}", 530, 45)
        self.draw_text(screen, f"Lap: {self.car.completed_laps}/{self.total_laps}", 530, 63)
        self.draw_text(screen, f"Position: {player_position}/{len(self.cars)}", 530, 81)
        self.draw_text(screen, f"Cars in race: {len(self.cars)}", 530, 99)

        self.draw_text(screen, "STANDINGS", 530, 126, font=self.title_font)

        y = 150
        for index, car in enumerate(standings, start=1):
            self.draw_text(screen, f"{index}. {car.name} - Lap {car.completed_laps}", 530, y)
            y += 18