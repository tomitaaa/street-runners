import pygame
from pygame.math import Vector2
from game.car import Car


class PlayerCar(Car):
    def __init__(self, position: Vector2, track, name: str = "Python", waypoint_index: int = 1):
        super().__init__(position, track, name=name, waypoint_index=waypoint_index)

        self.color_on_road = (50, 200, 50)
        self.color_off_road = (200, 120, 50)

    def control(self, dt: float):
        keys = pygame.key.get_pressed()

        if self.velocity.length_squared() > 1.0:
            if keys[pygame.K_LEFT]:
                self.angle -= self.steering_speed * dt

            if keys[pygame.K_RIGHT]:
                self.angle += self.steering_speed * dt

        forward = self.get_forward_vector()

        if keys[pygame.K_UP]:
            self.apply_force(forward * self.engine_force)

        if keys[pygame.K_DOWN]:
            self.apply_force(-forward * self.brake_force)