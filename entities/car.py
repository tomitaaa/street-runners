import math
import os
import pygame
from pygame.math import Vector2
from core.dynamic_object import DynamicObject


def _load_sprite(filename: str) -> pygame.Surface | None:
    """Carrega um sprite PNG com suporte a transparência."""
    assets_dir = os.path.join(os.path.dirname(__file__), "..", "assets", "images")
    path = os.path.normpath(os.path.join(assets_dir, filename))
    if os.path.exists(path):
        return pygame.image.load(path).convert_alpha()
    return None


class Car(DynamicObject):
    # Cache de sprites compartilhado entre instâncias (carrega 1x por processo)
    _sprite_cache: dict[str, pygame.Surface] = {}

    def __init__(self, position: Vector2, track, name: str = "Car", waypoint_index: int = 0):
        super().__init__(position)

        self.track = track
        self.name = name

        self.angle: float = 0.0

        self.engine_force: float = 900.0
        self.brake_force: float = 600.0
        self.max_speed: float = 500.0

        self.on_road_drag: float = 1.5
        self.off_road_drag: float = 5.5

        self.steering_speed: float = 180.0
        self.lateral_friction: float = 0.90

        self.width: float = 40.0
        self.height: float = 20.0

        self.linear_drag = self.on_road_drag

        # Cor de fallback (triângulo) caso sprite não carregue
        self.color_on_road = (50, 200, 50)
        self.color_off_road = (200, 120, 50)

        # Nome do arquivo de sprite (sobrescrito nas subclasses)
        self.sprite_file: str = "player_car.png"

        self.current_waypoint_index: int = waypoint_index
        self.waypoint_radius: float = 35.0
        self.completed_laps: int = 0

    # ──────────────────────────────────────────────────────────────
    # Helpers de sprite
    # ──────────────────────────────────────────────────────────────

    def _get_sprite(self) -> pygame.Surface | None:
        """Retorna sprite do cache (carrega na primeira chamada)."""
        if self.sprite_file not in Car._sprite_cache:
            surf = _load_sprite(self.sprite_file)
            if surf is not None:
                # Redimensiona para as dimensões exatas do carro
                surf = pygame.transform.scale(surf, (int(self.width), int(self.height)))
            Car._sprite_cache[self.sprite_file] = surf  # None se não achar
        return Car._sprite_cache[self.sprite_file]

    # ──────────────────────────────────────────────────────────────
    # Lógica de movimento (inalterada)
    # ──────────────────────────────────────────────────────────────

    def get_forward_vector(self) -> Vector2:
        angle_rad = math.radians(self.angle)
        return Vector2(math.cos(angle_rad), math.sin(angle_rad))

    def get_right_vector(self) -> Vector2:
        forward = self.get_forward_vector()
        return Vector2(-forward.y, forward.x)

    def get_current_waypoint(self) -> Vector2:
        return self.track.waypoints[self.current_waypoint_index]

    def normalize_angle(self, angle: float) -> float:
        while angle > 180.0:
            angle -= 360.0
        while angle < -180.0:
            angle += 360.0
        return angle

    def advance_waypoint_if_needed(self):
        target = self.get_current_waypoint()
        distance = self.position.distance_to(target)

        if distance <= self.waypoint_radius:
            previous_index = self.current_waypoint_index
            self.current_waypoint_index = (self.current_waypoint_index + 1) % len(self.track.waypoints)

            if previous_index == len(self.track.waypoints) - 1 and self.current_waypoint_index == 0:
                self.completed_laps += 1

    def get_progress_score(self) -> float:
        total_waypoints = len(self.track.waypoints)
        target = self.get_current_waypoint()
        distance = self.position.distance_to(target)

        return (self.completed_laps * total_waypoints) + self.current_waypoint_index - (distance / 10000.0)

    def control(self, dt: float):
        pass

    def update_track_state(self):
        if self.track.is_on_road(self.position):
            self.linear_drag = self.on_road_drag
        else:
            self.linear_drag = self.off_road_drag

    def apply_lateral_friction(self):
        forward = self.get_forward_vector()
        right = self.get_right_vector()

        forward_speed = self.velocity.dot(forward)
        lateral_speed = self.velocity.dot(right)

        forward_velocity = forward * forward_speed
        lateral_velocity = right * lateral_speed

        lateral_velocity *= (1.0 - self.lateral_friction)

        self.velocity = forward_velocity + lateral_velocity

    def update(self, dt: float):
        self.control(dt)
        self.update_track_state()

        super().update(dt)

        self.apply_lateral_friction()
        self.advance_waypoint_if_needed()

        speed = self.velocity.length()
        if speed > self.max_speed:
            self.velocity.scale_to_length(self.max_speed)

        if self.velocity.length() < 5.0:
            self.velocity.update(0.0, 0.0)

    # ──────────────────────────────────────────────────────────────
    # Desenho com sprite 8-bit (fallback para triângulo)
    # ──────────────────────────────────────────────────────────────

    def draw(self, screen: pygame.Surface):
        sprite = self._get_sprite()

        if sprite is not None:
            # Rotaciona o sprite ao redor do centro.
            # pygame.transform.rotate gira no sentido anti-horário,
            # mas nosso ângulo cresce no sentido horário → negamos.
            rotated = pygame.transform.rotate(sprite, -self.angle)
            rect = rotated.get_rect(center=(int(self.position.x), int(self.position.y)))
            screen.blit(rotated, rect)
        else:
            # ── Fallback: triângulo original ──────────────────────
            half_w = self.width / 2.0
            half_h = self.height / 2.0

            local_points = [
                Vector2(+half_w, 0.0),
                Vector2(-half_w, -half_h),
                Vector2(-half_w, +half_h),
            ]

            world_points = []
            for point in local_points:
                rotated_pt = point.rotate(self.angle)
                world = self.position + rotated_pt
                world_points.append((int(world.x), int(world.y)))

            color = self.color_on_road if self.track.is_on_road(self.position) else self.color_off_road
            pygame.draw.polygon(screen, color, world_points)
