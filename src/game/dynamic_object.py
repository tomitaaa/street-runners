from __future__ import annotations
from pygame.math import Vector2
from game.game_object import GameObject


class DynamicObject(GameObject):
    """
    Objeto com física básica (integração explícita):
      v += a * dt
      pos += v * dt

    position, velocity, acceleration são Vector2 (floats).
    """

    def __init__(self, position: Vector2 | None = None):
        super().__init__(position)
        self.velocity: Vector2 = Vector2(0.0, 0.0)
        self.acceleration: Vector2 = Vector2(0.0, 0.0)

        # Parâmetros úteis
        self.linear_drag: float = 0.0  # 0 = sem arrasto (quanto maior, mais freia)

    def apply_force(self, force: Vector2):
        """
        Aplica uma "força" como aceleração direta (massa = 1). Ajustável, caso necessário.
        """
        self.acceleration += force

    def update(self, dt: float):
        if dt <= 0.0:
            return

        # 1) Integra velocidade pela aceleração
        self.velocity += self.acceleration * dt

        # 2) Arrasto linear simples (freio/atrito no ar), opcional
        if self.linear_drag > 0.0:
            # Exponencial para ficar estável com dt variável
            drag_factor = max(0.0, 1.0 - self.linear_drag * dt)
            self.velocity *= drag_factor

        # 3) Integra posição pela velocidade
        self.position += self.velocity * dt

        # 4) Zera a aceleração a cada frame (forças devem ser reaplicadas)
        self.acceleration.update(0.0, 0.0)