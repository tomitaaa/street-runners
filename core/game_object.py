from __future__ import annotations
from pygame.math import Vector2

class GameObject:
    """Gerencia os objetos, a posição e atualiza a cada frame, atualiza e desenha ."""
    def __init__(self, position: Vector2 | None = None):
        self.position = position or Vector2(0.0, 0.0)
        self.active: bool = True

    def update(self, dt: float):
        """Atualizar a lógica do objeto"""
        pass

    def draw(self, screen):
        """Renderizar o objeto"""
        pass