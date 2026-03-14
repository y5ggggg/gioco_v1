import arcade
import random
import gameview
import arcade.future.background as background

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
CAMERA_SPEED = 0.1
PLAYER_SCALE = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.12
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

# ---------------- PLAYER ----------------
'''class Player(arcade.Sprite):
    def __init__(self):
        super().__init__(scale=PLAYER_SCALE)

        base_path = "./gioco_v1/pilota"

        self.idle_texture = arcade.load_texture(f"{base_path}/pilota1.png")

        self.walk_textures = [
            arcade.load_texture(f"{base_path}/pilota2.png"),
            arcade.load_texture(f"{base_path}/pilota3.png"),
            arcade.load_texture(f"{base_path}/pilota4.png"),
            arcade.load_texture(f"{base_path}/pilota5.png"),
            arcade.load_texture(f"{base_path}/pilota6.png"),
            arcade.load_texture(f"{base_path}/pilota7.png"),
            arcade.load_texture(f"{base_path}/pilota8.png"),
            arcade.load_texture(f"{base_path}/pilota9.png"),
        ]

        self.texture = self.idle_texture
        self.cur_texture = 0
        self.facing_direction = 0  # 0 = destra, 1 = sinistra

    def update_animation(self, delta_time: float = 1 / 60):

        # Direzione
        if self.change_x < 0:
            self.facing_direction = 1
        elif self.change_x > 0:
            self.facing_direction = 0

        # Idle
        if self.change_x == 0:
            self.texture = (
                self.idle_texture.flip_left_right()
                if self.facing_direction == 1
                else self.idle_texture
            )
            return

        # Animazione camminata
        self.cur_texture += 1
        if self.cur_texture >= len(self.walk_textures) * 5:
            self.cur_texture = 0

        frame = self.cur_texture // 5
        texture = self.walk_textures[frame]

        self.texture = (
            texture.flip_left_right()
            if self.facing_direction == 1
            else texture
        )'''

class mywindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        self.gameview = gameview.GameView()
        self.pilota = None
        self.player_sprite = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.gui_camera = None
        self.score = 0
        self.score_text = None
        self.scene = None
        self.tile_map = None
        self.camera = arcade.Camera2D()
        
        
        #self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        #self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.lista_pilota = arcade.SpriteList()
        self.sfondo = arcade.load_texture("./immagini/sfondo1.png")
        self.pilota = arcade.load_texture("./pilota/pilota1.png")
        
        self.setup()
        self.gameview.pan_camera_to_player()
    
    def setup(self):
        '''
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True
            }
        }

        self.tile_map = arcade.load_tilemap(
            ":resources:tiled_maps/map.json",
            scaling=TILE_SCALING,
            layer_options=layer_options
        )

        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        '''
        self.scene = arcade.Scene()
        self.player_sprite = self.gameview.player_sprite
        self.player_list=arcade.SpriteList()
        self.player_sprite.scale = 0.5
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        for x in range(0, 10000, 64):
            wall = arcade.Sprite("./immagini/tiles/terreno.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)


        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in range(128, 10000, 256):
            wall = arcade.Sprite("./immagini/tiles/muro.png", scale=TILE_SCALING)
            wall.scale= 0.1211
            #wall.position = coordinate
            wall.center_x = random.randint(10, 9800)
            wall.center_y = 96
            self.scene.add_sprite("Walls", wall)
        
        for x in range(128, 10000, 256):
            coin = arcade.Sprite("./immagini/item.png", scale=COIN_SCALING)
            coin.center_x = random.randint(10, 9800)
            coin.center_y = random.randint(96, 256)
            self.scene.add_sprite("Coins", coin)
            #39 coins totali
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )
        self.velocita = 4

        
        self.score = 0
        self.score_text = arcade.Text(f"Score: {self.score}", x = 0, y = 5, color = arcade.csscolor.BLACK, font_size = 20)
    
    def on_draw(self):
        self.clear()
        self.gameview.camera.use()
        bg = self.gameview.backgrounds

        # Sposta i layer simulando la profondità
        bg.offset = self.gameview.camera.bottom_left
        # Segue la camera per simulare un "mondo infinito"
        bg.pos = self.gameview.camera.bottom_left

        bg.draw()
        self.scene.draw()
        
        self.score_text.draw()
        

    def on_update(self, delta_time: float):
        self.gameview.on_update(delta_time)
        self.physics_engine.update()
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            #arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"
        

    def on_key_press(self, tasto, modificatori):
        if tasto == arcade.key.ESCAPE:
            self.setup()
        if tasto == arcade.key.UP or tasto == arcade.key.W or tasto == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if tasto == arcade.key.LEFT or tasto == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif tasto == arcade.key.RIGHT or tasto == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            
        '''if tasto == arcade.key.UP or tasto == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)'''
    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        
        if tasto == arcade.key.LEFT or tasto == arcade.key.A:
            self.player_sprite.change_x = 0
            self.score_text.x = self.player_sprite.center_x
        elif tasto == arcade.key.RIGHT or tasto == arcade.key.D:
            self.player_sprite.change_x = 0
            self.score_text.x = self.player_sprite.center_x
            
        

def main():
    window = mywindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()