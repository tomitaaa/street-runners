from __future__ import annotations

from pygame.math import Vector2
from game.game_object import GameObject


class DynamicObject(GameObject):
    def __init__(self, position: Vector2 | None = None):
        super().__init__(position)
        self.velocity: Vector2 = Vector2(0.0, 0.0)
        self.acceleration: Vector2 = Vector2(0.0, 0.0)
        self.linear_drag: float = 0.0

    def apply_force(self, force: Vector2):
        self.acceleration += force

    def update(self, dt: float):
        if dt <= 0.0:
            return

        self.velocity += self.acceleration * dt

        if self.linear_drag > 0.0:
            drag_factor = max(0.0, 1.0 - self.linear_drag * dt)
            self.velocity *= drag_factor

        self.position += self.velocity * dt

        self.acceleration.update(0.0, 0.0)