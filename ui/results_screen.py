import pygame
from typing import Callable


class ResultsScreen:
    """Tela de resultados exibida ao fim da corrida."""

    is_results = True   # sinaliza para game.py não abrir menu de pausa por cima

    def __init__(self, cars: list, player_car, total_laps: int, on_restart: Callable):
        pygame.font.init()
        self.active = True
        self.cars = cars
        self.player_car = player_car
        self.total_laps = total_laps
        self.on_restart = on_restart

        self.font_title  = pygame.font.SysFont(None, 72)
        self.font_sub    = pygame.font.SysFont(None, 40)
        self.font_item   = pygame.font.SysFont(None, 30)

        self.selected = 0
        self.options = ["JOGAR NOVAMENTE", "SAIR"]
        self.option_rects: list[pygame.Rect] = []

        # classifica no momento em que a tela é criada
        self._standings = sorted(cars, key=lambda c: c.get_progress_score(), reverse=True)

    # ------------------------------------------------------------------
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._activate()
        elif event.type == pygame.MOUSEMOTION:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.option_rects):
                if rect.collidepoint(event.pos):
                    self.selected = i
                    self._activate()

    def _activate(self):
        if self.options[self.selected] == "JOGAR NOVAMENTE":
            self.active = False
            self.on_restart()
        else:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    # ------------------------------------------------------------------
    def update(self, dt: float):
        pass

    def draw(self, screen):
        w, h = screen.get_size()

        # overlay escuro semitransparente sobre a pista
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((5, 5, 20, 215))
        screen.blit(overlay, (0, 0))

        winner = self._standings[0]
        player_pos = self._standings.index(self.player_car) + 1

        # --- título ---
        if winner is self.player_car:
            title_text  = "VOCE VENCEU!"
            title_color = (255, 220, 50)
        else:
            title_text  = "CORRIDA FINALIZADA"
            title_color = (180, 180, 255)

        title_surf = self.font_title.render(title_text, True, title_color)
        screen.blit(title_surf, title_surf.get_rect(center=(w // 2, 85)))

        pos_text = f"Voce terminou em {player_pos}o lugar"
        pos_surf = self.font_sub.render(pos_text, True, (160, 160, 160))
        screen.blit(pos_surf, pos_surf.get_rect(center=(w // 2, 148)))

        # --- classificação ---
        header_surf = self.font_sub.render("CLASSIFICACAO FINAL", True, (130, 130, 255))
        screen.blit(header_surf, header_surf.get_rect(center=(w // 2, 205)))

        y = 248
        prefixes = ["1o", "2o", "3o", "4o"]
        for i, car in enumerate(self._standings):
            is_winner = i == 0
            is_player = car is self.player_car
            if is_winner:
                color = (255, 220, 50)
            elif is_player:
                color = (100, 220, 100)
            else:
                color = (200, 200, 200)

            prefix = prefixes[i] if i < len(prefixes) else f"{i+1}o"
            line = f"{prefix}  {car.name}  -  {car.completed_laps} voltas"
            surf = self.font_item.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(w // 2, y)))
            y += 32

        # --- botões ---
        y = h - 135
        self.option_rects = []
        for i, opt in enumerate(self.options):
            color = (255, 220, 100) if i == self.selected else (180, 180, 180)
            surf = self.font_sub.render(opt, True, color)
            rect = surf.get_rect(center=(w // 2, y))
            screen.blit(surf, rect)
            self.option_rects.append(rect)
            y += 52
