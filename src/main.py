from pygame.math import Vector2
from game.game import Game
from game.track import Track
from game.player_car import PlayerCar
from game.npc_car import NPCCar
from game.debug_hud import DebugHUD
from game.menu import Menu


if __name__ == "__main__":
    game = Game()

    track = Track()

    player_car = PlayerCar(Vector2(220.0, 140.0), track, name="Python", waypoint_index=1)
    player_car.angle = 0.0

    npc_car_1 = NPCCar(Vector2(300.0, 140.0), track, name="NPC 1", waypoint_index=1)
    npc_car_2 = NPCCar(Vector2(340.0, 155.0), track, name="NPC 2", waypoint_index=1)
    npc_car_3 = NPCCar(Vector2(380.0, 170.0), track, name="NPC 3", waypoint_index=1)

    npc_car_1.angle = 0.0
    npc_car_2.angle = 0.0
    npc_car_3.angle = 0.0

    cars = [player_car, npc_car_1, npc_car_2, npc_car_3]

    hud = DebugHUD(
        car=player_car,
        track=track,
        clock=game.clock,
        cars=cars,
        total_laps=3
    )

    game.add_object(track)
    game.add_object(player_car)
    game.add_object(npc_car_1)
    game.add_object(npc_car_2)
    game.add_object(npc_car_3)
    game.add_object(hud)

    # começar com objetos do jogo desativados; serão ativados pelo menu
    for o in (track, player_car, npc_car_1, npc_car_2, npc_car_3, hud):
        o.active = False

    def start_or_resume():
        # ativa todos os objetos do jogo e esconde o menu
        for o in (track, player_car, npc_car_1, npc_car_2, npc_car_3, hud):
            o.active = True

    menu = Menu(start_or_resume)
    menu.set_mode("main")
    game.add_object(menu)

    game.run()