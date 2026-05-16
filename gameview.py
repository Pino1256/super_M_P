import arcade
from sprite_animato import SpriteAnimato

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

TILE_SCALING = 1.5

class Player(SpriteAnimato): 
    def __init__(self):
        super().__init__(scale = 1)

        file_animazioni = {
            "destra": "assets/font/run_right.png",
            "sinistra": "assets/font/run_left.png",
            "giu": "assets/font/run_down.png",
            "su": "assets/font/run_up.png",
            "idle": "assets/font/run_idle.png"
        }

        for dir, percorso in file_animazioni.items():
            self.aggiungi_animazione(
                nome = f"run_{dir}",
                percorso = percorso,
                frame_width = 96,
                frame_height = 80,
                num_frame = 8,
                colonne = 8,
                durata = 1
            )
        
        self.direzione = "idle"
        self.change_x = 0
        self.change_y = 0

    def update_animation(self, delta_time):
        if self.change_y > 0:
            self.direzione = "su"
        elif self.change_y < 0:
            self.direzione = "giu"
        elif self.change_x > 0:
            self.direzione = "destra"
        elif self.change_x < 0:
            self.direzione = "sinistra"
        
        if self.change_x != 0 or self.change_y != 0:
            self.imposta_animazione(f"run_{self.direzione}")
        else:
            self.direzione = "idle"
            self.imposta_animazione(f"run_{self.direzione}")
        
        super().update_animation(delta_time)

class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.AERO_BLUE)

        # personaggio
        self.personaggio = None
        self.speed = 5

        # movimento
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        # camera
        self.camera = arcade.camera.Camera2D()
        self.camera_ui = arcade.camera.Camera2D()

        # tile map
        self.tile_map = None
        self.scene = None
        self.cambio_mappa = False
        self.mappa_corrente = "esterno"
        # self.casa_mappa = True
        # self.fuori_mappa = False

        self.layer_options = {
            "Livello tile 1":{
                "use_spatial_hash": True
            }
        }

        self.setup()
    
    def setup(self):

        self.tile_map = arcade.load_tilemap(
            "./assets/mappe/map_1.tmx",
            scaling = TILE_SCALING,
            layer_options = self.layer_options
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.personaggio = Player()
        self.personaggio.center_x = 1100
        self.personaggio.center_y = 600


        self.scene.add_sprite("personaggio", self.personaggio)

        collisioni = arcade.SpriteList()
        collisioni.extend(self.scene["casa"])
        collisioni.extend(self.scene["oggetti"])
        collisioni.extend(self.scene["aqua"])

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.personaggio,
            walls = collisioni
        )

        self.cambio_mappa = False

    def carica_casa(self):

        self.tile_map = arcade.load_tilemap(
            "./assets/mappe/home_2.tmx",
            scaling = TILE_SCALING,
            layer_options = self.layer_options
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.scene.add_sprite("personaggio", self.personaggio)

        collisioni = arcade.SpriteList()
        collisioni.extend(self.scene["sedie"])
        collisioni.extend(self.scene["oggetti"])
        collisioni.extend(self.scene["sedie2"])
        collisioni.extend(self.scene["tavolo"])
        collisioni.extend(self.scene["mura"])

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.personaggio,
            walls = collisioni
        )

        self.cambio_mappa = False

        self.personaggio.center_x = 1524
        self.personaggio.center_y = 1705

    def on_draw(self):
        self.clear()

        self.camera.use()
        self.scene.draw()

        self.camera_ui.use()

        arcade.draw_text(f"X: {self.personaggio.center_x:.0f}", 10, SCREEN_HEIGHT - 50, arcade.color.BLACK, 20)
        arcade.draw_text(f"Y: {self.personaggio.center_y:.0f}", 10, SCREEN_HEIGHT - 70, arcade.color.BLACK, 20)

    
    def on_update(self, delta_time):

        cy = 0
        cx = 0
        
        porte = self.scene.get_sprite_list("porta") if "porta" in self.scene._name_mapping else arcade.SpriteList()
        porte_toccate = arcade.check_for_collision_with_list(
            self.personaggio,
            porte
        )

        if porte_toccate and not self.cambio_mappa:
            self.cambio_mappa = True
            if self.mappa_corrente == "esterno":
                self.mappa_corrente = "casa"
                self.carica_casa()
            else:
                self.mappa_corrente = "esterno"
                self.setup()
                self.personaggio.center_x = 1189
                self.personaggio.center_y = 1620

        if self.up_pressed: cy += self.speed
        if self.down_pressed: cy -= self.speed
        if self.left_pressed: cx -= self.speed
        if self.right_pressed: cx += self.speed
    
        self.personaggio.change_x = cx
        self.personaggio.change_y = cy

        self.physics_engine.update()

        self.scene.update_animation(delta_time)

        self.camera.position = self.personaggio.center_x, self.personaggio.center_y


    def on_key_press(self, tasto, modificatori):

        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = True
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = True
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True  
        
    
    def on_key_release(self, tasto, modificatori):

        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False   
