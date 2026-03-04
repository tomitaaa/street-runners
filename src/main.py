from pygame.math import Vector2
from game.game import Game
from game.debug_dynamic  import DebugDynamic

if __name__ == "__main__":
    game = Game()
    game.add_object(DebugDynamic(Vector2(100.0, 300.0)))
    game.run()