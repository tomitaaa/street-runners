import math
import pygame
from pygame.math import Vector2
from game.dynamic_object import DynamicObject


class Car(DynamicObject):
    def __init__(self, position: Vector2, track):
        super().__init__(position)

        self.track = track

        self.angle: float = 0.0

        self.engine_force: float = 800.0
        self.brake_force: float = 500.0
        self.max_speed: float = 500.0

        self.on_road_drag: float = 1.8
        self.off_road_drag: float = 6.0

        self.steering_speed: float = 180.0

        self.width: float = 40.0
        self.height: float = 20.0

        self.linear_drag = self.on_road_drag

    def get_forward_vector(self) -> Vector2:
        angle_rad = math.radians(self.angle)
        return Vector2(math.cos(angle_rad), math.sin(angle_rad))

    def handle_input(self, dt: float):
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

    def update_track_state(self):
        if self.track.is_on_road(self.position):
            self.linear_drag = self.on_road_drag
        else:
            self.linear_drag = self.off_road_drag

    def update(self, dt: float):
        self.handle_input(dt)
        self.update_track_state()

        super().update(dt)

        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if self.velocity.length() < 5.0:
            self.velocity.update(0.0, 0.0)

    def draw(self, screen):
        half_w = self.width / 2.0
        half_h = self.height / 2.0

        local_points = [
            Vector2(+half_w, 0.0),
            Vector2(-half_w, -half_h),
            Vector2(-half_w, +half_h),
        ]

        world_points = []
        for point in local_points:
            rotated = point.rotate(self.angle)
            world = self.position + rotated
            world_points.append((int(world.x), int(world.y)))

        color = (50, 200, 50) if self.track.is_on_road(self.position) else (200, 120, 50)
        pygame.draw.polygon(screen, color, world_points)