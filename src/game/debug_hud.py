import pygame
from pygame.math import Vector2
from game.game_object import GameObject


class DebugHUD(GameObject):

    def __init__(self, car, track, clock):
        super().__init__(Vector2(0, 0))

        self.car = car
        self.track = track
        self.clock = clock

        pygame.font.init()
        self.font = pygame.font.SysFont("consolas", 16)

        self.color = (255, 255, 255)

    def draw_text(self, screen, text, x, y):
        surface = self.font.render(text, True, self.color)
        screen.blit(surface, (x, y))

    def draw(self, screen):

        speed = self.car.velocity.length()
        pos = self.car.position
        angle = self.car.angle
        on_road = self.track.is_on_road(self.car.position)
        fps = self.clock.get_fps()

        lines = [
            f"FPS: {fps:.1f}",
            f"Speed: {speed:.1f}",
            f"Angle: {angle:.1f}",
            f"Position: ({pos.x:.1f}, {pos.y:.1f})",
            f"On Road: {on_road}",
        ]

        y = 10
        for line in lines:
            self.draw_text(screen, line, 10, y)
            y += 20