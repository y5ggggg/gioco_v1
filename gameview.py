import arcade
import arcade.future.background as background


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
CAMERA_SPEED = 0.1


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color =  arcade.csscolor.CORNFLOWER_BLUE
        #(162, 84, 162, 255)
        self.camera = arcade.Camera2D()
        self.backgrounds = background.ParallaxGroup()

        bg_size = (WINDOW_WIDTH, WINDOW_HEIGHT)

        self.backgrounds.add_from_file("./immagini/sfondo1.png",    size=bg_size, depth=10.0)
        self.backgrounds.add_from_file("./immagini/tiles/dietro.png",   size=(WINDOW_WIDTH, 578), depth=3.0)
        self.backgrounds.add_from_file("./immagini/tiles/tribuna.png",   size=(WINDOW_WIDTH, 292), depth=1.5)
        self.player_sprite = arcade.Sprite("./pilota/pilota1.png", scale=0.5)
        self.player_sprite.bottom = 128 # mette il giocatore in basso
        self.x_velocity = 0 # usata per la gestione del movimento, per spostare il giocatore

    def on_draw(self):
        self.clear() # pulisco lo schermo
        self.camera.use()

        bg = self.backgrounds

        # Sposta i layer simulando la profondità
        bg.offset = self.camera.bottom_left
        # Segue la camera per simulare un "mondo infinito"
        bg.pos = self.camera.bottom_left

        bg.draw()
        arcade.draw_sprite(self.player_sprite)

    def pan_camera_to_player(self):
        # La camera segue il giocatore in modo "smooth" (lerp). Guarda l'altro blog sulla camera
        self.camera.position = arcade.math.lerp_2d(
            self.camera.position,
            (self.player_sprite.center_x, self.height // 2),
            CAMERA_SPEED
        )

    def on_update(self, delta_time: float):
        self.player_sprite.center_x += self.x_velocity * delta_time
        self.pan_camera_to_player()
