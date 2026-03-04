import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # delta time em segundos
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self, dt):
        for obj in self.objects:
            if obj.active:
                obj.update(dt)

    def draw(self):
        self.screen.fill((30, 30, 30))
        for obj in self.objects:
            if obj.active:
                obj.draw(self.screen)
        pygame.display.flip()