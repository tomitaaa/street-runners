import math
import pygame
from pygame.math import Vector2
from core.dynamic_object import DynamicObject


class Car(DynamicObject):
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

        self.color_on_road = (50, 200, 50)
        self.color_off_road = (200, 120, 50)

        self.current_waypoint_index: int = waypoint_index
        self.waypoint_radius: float = 35.0
        self.completed_laps: int = 0

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

        color = self.color_on_road if self.track.is_on_road(self.position) else self.color_off_road
        pygame.draw.polygon(screen, color, world_points)