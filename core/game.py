import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE

"""motor principal do jogo, armazena objetos, gerencia estados e o loop (update e render)."""
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock   = pygame.time.Clock()
        self.running = True
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # ESC: abre/fecha menu de pausa — ignorar se tela de resultados estiver ativa
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                results_active = any(
                    getattr(o, 'is_results', False) and o.active
                    for o in self.objects
                )
                if not results_active:
                    menu = next(
                        (o for o in self.objects if getattr(o, 'is_menu', False)),
                        None
                    )
                    if menu:
                        if menu.active:
                            menu.active = False
                            for o in self.objects:
                                if o is not menu:
                                    o.active = True
                        else:
                            menu.set_mode('pause')
                            menu.active = True
                            for o in self.objects:
                                if o is not menu:
                                    o.active = False
                        continue

            for obj in list(self.objects):
                if hasattr(obj, 'handle_event') and obj.active:
                    try:
                        obj.handle_event(event)
                    except Exception:
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
