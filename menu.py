import arcade
# from gameview import GameView

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

class MenuView (arcade.View):
    def __init__(self, game_view):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.game_view = game_view

        self.sfondo_menu = None
        self.lista_sfondo = arcade.SpriteList()

        self.sfondo()

    def sfondo(self):
        self.sfondo_menu = arcade.Sprite("./assets/font/foglio.png")
        self.sfondo_menu.center_x  = SCREEN_WIDTH // 2
        self.sfondo_menu.center_y = SCREEN_HEIGHT //2
        self.sfondo_menu.scale = 1
        self.lista_sfondo.append(self.sfondo_menu)

    def on_draw(self):
        self.clear()
        self.lista_sfondo.draw()
        arcade.draw_text(f"vuoi vendere 1 di grano? il tuo grano: {self.game_view.harvested_grano}", SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, arcade.color.BLACK, 20)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.T:
            self.game_view.harvested_grano -= 1
        if key == arcade.key.L:
            self.window.show_view(self.game_view)
    
