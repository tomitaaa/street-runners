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

            # lidar com ESC toggling do menu de pausa
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                menu = next((o for o in self.objects if getattr(o, "is_menu", False)), None)
                if menu:
                    if menu.active:
                        # fechar menu e reativar objetos
                        menu.active = False
                        for o in self.objects:
                            if o is not menu:
                                o.active = True
                    else:
                        # abrir menu de pausa e desativar outros objetos
                        menu.set_mode("pause")
                        menu.active = True
                        for o in self.objects:
                            if o is not menu:
                                o.active = False
                    # não propagar ESC adiante
                    continue

            # encaminhar evento para objetos que implementam handle_event
            for obj in list(self.objects):
                if hasattr(obj, "handle_event") and obj.active:
                    try:
                        obj.handle_event(event)
                    except Exception:
                        # não bloquear o loop por causa de um handler
                        pass

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