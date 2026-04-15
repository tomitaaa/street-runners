import sys
from pathlib import Path

# Add root directory to Python path so modules can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from pygame.math import Vector2

from core.game import Game
from systems.track import Track
from entities.player_car import PlayerCar
from entities.npc_car import NPCCar
from ui.debug_hud import DebugHUD
from ui.menu import Menu
from systems.race_manager import RaceManager
from ui.results_screen import ResultsScreen

TOTAL_LAPS = 3


def main() -> bool:
    """Executa uma sessao completa do jogo. Retorna True se o jogador
    escolheu 'Jogar Novamente', False se escolheu 'Sair'."""

    game  = Game()
    track = Track()

    # Grade de largada: 2 colunas x 2 linhas, a direita da linha de largada
    #   col A (x=210)   col B (x=248)
    #   [player] [NPC2]    <- linha 1 (y=128)
    #   [NPC 1]  [NPC3]    <- linha 2 (y=152)
    player_car = PlayerCar(Vector2(210.0, 128.0), track, name="Python",   waypoint_index=1)
    npc_car_1  = NPCCar(   Vector2(210.0, 152.0), track, name="NPC 1",    waypoint_index=1)
    npc_car_2  = NPCCar(   Vector2(248.0, 128.0), track, name="NPC 2",    waypoint_index=1)
    npc_car_3  = NPCCar(   Vector2(248.0, 152.0), track, name="NPC 3",    waypoint_index=1)

    for car in (player_car, npc_car_1, npc_car_2, npc_car_3):
        car.angle = 0.0

    cars = [player_car, npc_car_1, npc_car_2, npc_car_3]

    hud = DebugHUD(
        car=player_car,
        track=track,
        clock=game.clock,
        cars=cars,
        total_laps=TOTAL_LAPS,
    )

    game_objects = [track, player_car, npc_car_1, npc_car_2, npc_car_3, hud]

    # estado mutavel para capturar a escolha do jogador apos a corrida
    state = {'restart': False}

    def on_race_finish():
        for o in [*game_objects, race_manager]:
            o.active = False

        results = ResultsScreen(
            cars=cars,
            player_car=player_car,
            total_laps=TOTAL_LAPS,
            on_restart=lambda: _on_restart(),
        )
        game.add_object(results)

    def _on_restart():
        state['restart'] = True
        game.running = False

    race_manager = RaceManager(cars, total_laps=TOTAL_LAPS, on_finish=on_race_finish)

    for o in game_objects:
        game.add_object(o)
    game.add_object(race_manager)

    # iniciar desativados; o menu os ativa
    for o in [*game_objects, race_manager]:
        o.active = False

    def start_or_resume():
        for o in [*game_objects, race_manager]:
            o.active = True

    menu = Menu(start_or_resume)
    menu.set_mode('main')
    game.add_object(menu)

    game.run()

    return state['restart']


if __name__ == '__main__':
    while main():
        pass   # reinicia ate o jogador escolher Sair
    sys.exit(0)
