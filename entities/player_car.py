import pygame
from pygame.math import Vector2
from entities.car import Car


class PlayerCar(Car):
    def __init__(self, position: Vector2, track,
                 name: str = "Python",
                 waypoint_index: int = 1,
                 sound_manager=None):
        super().__init__(position, track, name=name, waypoint_index=waypoint_index)

        self.sprite_file = "player_car.png"
        self.color_on_road  = (50, 200, 50)
        self.color_off_road = (200, 120, 50)

        self._sfx = sound_manager
        self._was_offroad = False

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

    def update(self, dt: float):
        super().update(dt)

        if self._sfx is None:
            return

        speed_ratio = min(1.0, self.velocity.length() / self.max_speed)
        self._sfx.play_engine(speed_ratio)

        on_road = self.track.is_on_road(self.position)
        if self._was_offroad is False and not on_road:
            self._sfx.play("offroad")
        self._was_offroad = not on_road