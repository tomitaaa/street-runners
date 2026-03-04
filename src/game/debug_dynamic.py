"""Classe de testes"""
import pygame
from pygame.math import Vector2
from game.dynamic_object import DynamicObject


class DebugDynamic(DynamicObject):
    def __init__(self, position: Vector2):
        super().__init__(position)
        self.velocity = Vector2(120.0, 0.0)  # 120 unidades por segundo
        self.linear_drag = 0.2               # desacelera com o tempo

    def draw(self, screen):
        # Converte float -> int só na renderização
        p = (int(self.position.x), int(self.position.y))
        pygame.draw.circle(screen, (200, 50, 50), p, 10)