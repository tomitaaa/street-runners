import pygame
from typing import Callable


class Menu:
    def __init__(self, activate_callback: Callable[[], None], title: str = "Street Runners"):
        pygame.font.init()
        self.active = True
        self.title = title
        self.options = ["Iniciar", "Sair"]
        self.selected = 0
        self.font_title = pygame.font.SysFont(None, 64)
        self.font_option = pygame.font.SysFont(None, 36)
        self.activate_callback = activate_callback
        self.is_menu = True
        # retângulos das opções para detectar cliques/hover
        self.option_rects: list[pygame.Rect] = []

    def set_mode(self, mode: str):
        """Mode: 'main' or 'pause'"""
        if mode == "main":
            self.title = "Street Runners"
            self.options = ["Iniciar", "Sair"]
        elif mode == "pause":
            self.title = "Pausado"
            self.options = ["Continuar", "Sair"]
        self.selected = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self._activate_selected()

        elif event.type == pygame.MOUSEMOTION:
            pos = event.pos
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(pos):
                    self.selected = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                pos = event.pos
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(pos):
                        self.selected = i
                        self._activate_selected()
                        break

    def _activate_selected(self):
        choice = self.options[self.selected]
        if choice in ("Iniciar", "Continuar"):
            try:
                self.activate_callback()
            finally:
                self.active = False
        elif choice == "Sair":
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt):
        pass

    def draw(self, screen):
        w, h = screen.get_size()
        screen.fill((20, 20, 40))

        title_surf = self.font_title.render(self.title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(w // 2, h // 4))
        screen.blit(title_surf, title_rect)

        # desenhar opções e armazenar retângulos
        self.option_rects = []
        for i, opt in enumerate(self.options):
            color = (255, 220, 100) if i == self.selected else (200, 200, 200)
            opt_surf = self.font_option.render(opt, True, color)
            opt_rect = opt_surf.get_rect(center=(w // 2, h // 2 + i * 50))
            screen.blit(opt_surf, opt_rect)
            self.option_rects.append(opt_rect)
