from pygame.math import Vector2
from game.game import Game
from game.car import Car
from game.track import Track
from game.debug_hud import DebugHUD


if __name__ == "__main__":

    game = Game()

    track = Track()
    car = Car(Vector2(400.0, 140.0), track)

    hud = DebugHUD(car, track, game.clock)

    game.add_object(track)
    game.add_object(car)
    game.add_object(hud)

    game.run()