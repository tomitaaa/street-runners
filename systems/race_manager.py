from core.game_object import GameObject


class RaceManager(GameObject):
    """Gerencia colisões entre carros e detecta o fim da corrida."""

    COLLISION_RADIUS = 22.0

    def __init__(self, cars: list, total_laps: int, on_finish, sound_manager=None):
        super().__init__()
        self.cars       = cars
        self.total_laps = total_laps
        self.on_finish  = on_finish
        self._sfx       = sound_manager
        self._race_over = False

        # Controla o cooldown de som de colisão para não repetir muito rápido
        self._crash_cooldown: float = 0.0

    def update(self, dt: float):
        if self._crash_cooldown > 0:
            self._crash_cooldown -= dt

        self._resolve_car_collisions()
        if not self._race_over:
            self._check_finish()

    def _resolve_car_collisions(self):
        r = self.COLLISION_RADIUS
        min_dist    = r * 2.0
        min_dist_sq = min_dist ** 2

        for i in range(len(self.cars)):
            for j in range(i + 1, len(self.cars)):
                a = self.cars[i]
                b = self.cars[j]

                delta   = a.position - b.position
                dist_sq = delta.length_squared()

                if dist_sq == 0 or dist_sq >= min_dist_sq:
                    continue

                dist    = dist_sq ** 0.5
                overlap = min_dist - dist
                normal  = delta / dist

                a.position += normal * (overlap * 0.5)
                b.position -= normal * (overlap * 0.5)

                rel_vel    = a.velocity - b.velocity
                vel_along  = rel_vel.dot(normal)

                if vel_along < 0:
                    restitution = 0.4
                    impulse     = normal * (vel_along * (1.0 + restitution) * 0.5)
                    a.velocity -= impulse
                    b.velocity += impulse

                    # Som de colisão (cooldown de 0.4s para não spammar)
                    if self._sfx and self._crash_cooldown <= 0:
                        impact_speed = abs(vel_along)
                        if impact_speed > 30:
                            self._sfx.play("crash")
                            self._crash_cooldown = 0.4

    def _check_finish(self):
        for car in self.cars:
            if car.completed_laps >= self.total_laps:
                self._race_over = True
                if self._sfx:
                    self._sfx.stop_engine()
                    self._sfx.play("lap_complete")
                self.on_finish()
                return
