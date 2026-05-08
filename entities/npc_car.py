import math
import random
from pygame.math import Vector2
from entities.car import Car


# Sprites disponíveis para os NPCs (escolhidos aleatoriamente ou por índice)
_NPC_SPRITES = [
    "npc_car_blue.png",
    "npc_car_red.png",
    "npc_car_orange.png",
    "npc_car_purple.png",
]


class NPCCar(Car):
    # Contador de instâncias para distribuir as cores em sequência
    _instance_count: int = 0

    def __init__(self, position: Vector2, track, name: str = "NPC", waypoint_index: int = 0):
        super().__init__(position, track, name=name, waypoint_index=waypoint_index)

        # Alterna sprites em sequência para variedade visual
        idx = NPCCar._instance_count % len(_NPC_SPRITES)
        self.sprite_file = _NPC_SPRITES[idx]
        NPCCar._instance_count += 1

        self.color_on_road = (70, 140, 240)
        self.color_off_road = (180, 120, 60)

        self.engine_force = 620.0
        self.brake_force = 500.0
        self.max_speed = 240.0
        self.steering_speed = 120.0

        self.look_ahead_offset = 1
        self.waypoint_radius = 55.0

    def get_steering_target(self) -> Vector2:
        index = (self.current_waypoint_index + self.look_ahead_offset) % len(self.track.waypoints)
        return self.track.waypoints[index]

    def control(self, dt: float):
        current_waypoint = self.get_current_waypoint()
        steering_target = self.get_steering_target()

        if self.position.distance_to(current_waypoint) > 120.0:
            steering_target = current_waypoint

        to_target = steering_target - self.position

        if to_target.length_squared() <= 0.0:
            return

        desired_angle = math.degrees(math.atan2(to_target.y, to_target.x))
        angle_diff = self.normalize_angle(desired_angle - self.angle)

        steer_strength = max(-1.0, min(1.0, angle_diff / 50.0))
        self.angle += steer_strength * self.steering_speed * dt

        forward = self.get_forward_vector()

        abs_diff = abs(angle_diff)
        speed = self.velocity.length()

        if abs_diff < 20.0:
            throttle = 1.0
        elif abs_diff < 45.0:
            throttle = 0.75
        elif abs_diff < 80.0:
            throttle = 0.45
        else:
            throttle = 0.20

        self.apply_force(forward * (self.engine_force * throttle))

        if abs_diff > 70.0 and speed > 120.0:
            self.apply_force(-forward * (self.brake_force * 0.35))
