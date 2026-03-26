from pygame.math import Vector2
from game.game import Game
from game.car import Car
from game.track import Track
from game.debug_hud import DebugHUD
from game.menu import Menu


if __name__ == "__main__":

    game = Game()

    track = Track()
    car = Car(Vector2(400.0, 140.0), track)

    hud = DebugHUD(car, track, game.clock)

    # começar com objetos do jogo desativados; serão ativados pelo menu
    track.active = False
    car.active = False
    hud.active = False

    game.add_object(track)
    game.add_object(car)
    game.add_object(hud)

    # callback para iniciar o jogo: ativa os objetos principais
    def start_game():
        track.active = True
        car.active = True
        hud.active = True

    menu = Menu(start_game)
    game.add_object(menu)

    game.run()