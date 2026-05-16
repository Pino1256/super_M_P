import arcade
from gameview import GameView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "M&P")
        
        menu = GameView()
        self.show_view(menu)

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()