import arcade
import random
import gameview


WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"
CAMERA_SPEED = 0.1
PLAYER_SCALE = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.12
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 25

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

class mywindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.gameview = gameview.GameView()
        self.pilota = None
        self.player_sprite = None
        self.vettura_sprite = None
        self.player_list = None
        self.wall_list = None
        self.coin_list = None
        self.gui_camera = None
        self.elapsed_time = 0.0
        self.score = 0
        self.timer_text = None
        self.score_text = None
        self.scene = None
        self.tile_map = None
        self.win = None
        self.andata = True
        self.movement_left = PLAYER_MOVEMENT_SPEED
        self.movement_right = PLAYER_MOVEMENT_SPEED
        self.jump = PLAYER_JUMP_SPEED
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
        self.vettura_sprite = arcade.Sprite("./immagini/tiles/vettura2.png", scale=0.25)
        #self.player_list=arcade.SpriteList()
        self.player_sprite.scale = 0.5
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        self.scene.add_sprite_list("Bandiera", use_spatial_hash=True)
        for x in range(0, 12000, 64):
            wall = arcade.Sprite("./immagini/tiles/terreno.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        for x in range(500, 9200, 500):
            wall = arcade.Sprite("./immagini/tiles/terreno_alto.png", scale=TILE_SCALING)
            wall.center_x = random.randint(500, 8800)
            wall.center_y = 300
            self.scene.add_sprite("Walls", wall)


        for x in range(128, 9200, 750):
            wall = arcade.Sprite("./immagini/tiles/muro.png", scale=TILE_SCALING)
            wall.scale= 0.1211
            #wall.position = coordinate
            wall.center_x = random.randint(300, 9000)
            wall.center_y = 96
            self.scene.add_sprite("Walls", wall)

        coordinate_list = [[-100, 165], [12000, 165], [-100, 96], [12000, 96], [-100, 234], [12000, 234], [-100, 303], [12000, 303]]
        for coordinate in coordinate_list:
            walls = arcade.Sprite("./immagini/tiles/muro.png", scale=0.1211)
            walls.position = coordinate
            self.scene.add_sprite("Walls", walls)
        
        for x in range(128, 9600, 700):
            coin = arcade.Sprite("./immagini/item.png", scale=COIN_SCALING)
            coin.center_x = random.randint(300, 9100)
            coin.center_y = random.randint(96, 500)
            self.scene.add_sprite("Coins", coin)
            #38 coins totali

        for x in range(11000, 11001):
            bandiera = arcade.Sprite("./immagini/tiles/bandiera.png", scale=0.5)
            bandiera.center_x = 11000
            bandiera.center_y = 270
            self.scene.add_sprite("Bandiera", bandiera)

        
        vettura = arcade.Sprite("./immagini/tiles/vettura1.png", scale=0.5)
        vettura.position = (9500, 176)
        self.scene.add_sprite("Vettura", vettura)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.scene["Walls"], gravity_constant=GRAVITY
        )

        self.physics_engine_macchine = arcade.PhysicsEngineSimple(
            self.vettura_sprite, walls=self.scene["Walls"]
        )
        self.velocita = 4

        self.score = 0
        self.elapsed_time = 0.0
        self.score_text = arcade.Text(f"Score: {self.score}", x=0, y=5, anchor_x="center", color = arcade.csscolor.BLACK, font_size = 30)
        self.timer_text = arcade.Text(f"Time: 00:00.000", x=350, y=650, color = arcade.csscolor.BLACK, font_size = 20)

    def on_draw(self):
        self.window.clear()
        self.gameview.camera.use()
        bg = self.gameview.backgrounds

        # Sposta i layer simulando la profondità
        bg.offset = self.gameview.camera.bottom_left
        # Segue la camera per simulare un "mondo infinito"
        bg.pos = self.gameview.camera.bottom_left

        bg.draw()
        self.scene.draw()
        
        self.score_text.draw()
        self.timer_text.draw()
        if self.win!= None:
            self.win.draw()
    def on_update(self, delta_time: float):
        self.vettura_sprite.center_x -= self.velocita * delta_time
        self.gameview.on_update(delta_time)
        self.physics_engine.update()
        self.physics_engine_macchine.update()
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            #arcade.play_sound(self.collect_coin_sound)
            self.score += 75
            self.score_text.text = f"Score: {self.score}"
            
        vettura_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Vettura"]
        )
        for vettura in vettura_hit_list:
            self.scene["Vettura"].remove(vettura)
            self.jump = 0
            self.movement_left = 0
            self.movement_right = 10
            self.scene["Player"].remove(self.player_sprite)
            self.vettura_sprite.center_x = 9300
            self.vettura_sprite.center_y = 128
            self.scene.add_sprite("Vettura_p", self.vettura_sprite)

        bandiera_hit_list = arcade.check_for_collision_with_list(
            self.vettura_sprite, self.scene["Bandiera"]
        )
        for bandiera in bandiera_hit_list:
            self.andata = False
            self.win = arcade.Text("HAI VINTO!", x=self.player_sprite.center_x, y=self.player_sprite.center_y +300, anchor_x="center", anchor_y="center", color = arcade.csscolor.PURPLE, font_size=200)

        if self.andata:
            self.elapsed_time += delta_time
        minutes = int(self.elapsed_time) // 60
        seconds = int(self.elapsed_time) % 60
        millesimi = int((self.elapsed_time % 1) * 1000)
        self.time = f"{minutes:02d}:{seconds:02d}.{millesimi:03d}"
        self.timer_text.text = f"Time: {self.time}"
        

        self.timer_text.x = self.player_sprite.center_x + 350
        self.score_text.x = self.player_sprite.center_x
        
        

    def on_key_press(self, tasto, modificatori):
        import pause
        if tasto == arcade.key.ESCAPE:
            pause_view = pause.PauseView(self)
            self.window.show_view(pause_view)
        if tasto == arcade.key.R:
            self.setup()
            self.jump=PLAYER_JUMP_SPEED
            self.movement_left=PLAYER_MOVEMENT_SPEED
            self.movement_right=PLAYER_MOVEMENT_SPEED
        if tasto == arcade.key.UP or tasto == arcade.key.W or tasto == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = self.jump
        if tasto == arcade.key.LEFT or tasto == arcade.key.A:
            self.player_sprite.change_x = -self.movement_left
            self.vettura_sprite.change_x = -self.movement_left
        elif tasto == arcade.key.RIGHT or tasto == arcade.key.D:
            self.player_sprite.change_x = self.movement_right
            self.vettura_sprite.change_x = self.movement_right

        '''if tasto == arcade.key.UP or tasto == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)'''
    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        
        if tasto == arcade.key.LEFT or tasto == arcade.key.A:
            self.player_sprite.change_x = 0
            self.vettura_sprite.change_x = 0
        elif tasto == arcade.key.RIGHT or tasto == arcade.key.D:
            self.player_sprite.change_x = 0
            self.vettura_sprite.change_x = 0
            