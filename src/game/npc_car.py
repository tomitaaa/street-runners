import math
from pygame.math import Vector2
from game.car import Car


class NPCCar(Car):
    def __init__(self, position: Vector2, track, name: str = "NPC", waypoint_index: int = 0):
        super().__init__(position, track, name=name, waypoint_index=waypoint_index)

        self.color_on_road = (70, 140, 240)
        self.color_off_road = (180, 120, 60)

        self.engine_force = 620.0
        self.brake_force = 500.0
        self.max_speed = 240.0
        self.steering_speed = 120.0

        # usar look-ahead pequeno para não "pular" demais o caminho
        self.look_ahead_offset = 1

        # raio maior ajuda a não ficar preso orbitando waypoint
        self.waypoint_radius = 55.0

    def get_steering_target(self) -> Vector2:
        """
        Alvo usado para direção.
        Mantemos o waypoint atual para progressão,
        mas podemos olhar um pouco à frente para suavizar.
        """
        index = (self.current_waypoint_index + self.look_ahead_offset) % len(self.track.waypoints)
        return self.track.waypoints[index]

    def control(self, dt: float):
        # waypoint atual = progresso real da pista
        current_waypoint = self.get_current_waypoint()

        # alvo de direção = waypoint atual ou um pouco à frente
        steering_target = self.get_steering_target()

        # se estiver muito longe do waypoint atual, prioriza ele
        # isso evita orbitar para sempre sem avançar a volta
        if self.position.distance_to(current_waypoint) > 120.0:
            steering_target = current_waypoint

        to_target = steering_target - self.position

        if to_target.length_squared() <= 0.0:
            return

        desired_angle = math.degrees(math.atan2(to_target.y, to_target.x))
        angle_diff = self.normalize_angle(desired_angle - self.angle)

        # esterçamento proporcional, mais suave
        steer_strength = max(-1.0, min(1.0, angle_diff / 50.0))
        self.angle += steer_strength * self.steering_speed * dt

        forward = self.get_forward_vector()

        abs_diff = abs(angle_diff)
        speed = self.velocity.length()

        # aceleração conforme curva
        if abs_diff < 20.0:
            throttle = 1.0
        elif abs_diff < 45.0:
            throttle = 0.75
        elif abs_diff < 80.0:
            throttle = 0.45
        else:
            throttle = 0.20

        self.apply_force(forward * (self.engine_force * throttle))

        # freio leve em curva muito fechada e velocidade alta
        if abs_diff > 70.0 and speed > 120.0:
            self.apply_force(-forward * (self.brake_force * 0.35))