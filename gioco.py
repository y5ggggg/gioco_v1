import arcade
import random
import gameview
from nemico import Nemico

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
CAMERA_SPEED = 0.1
PLAYER_SCALE = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.12
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 23

class mywindow(arcade.View):
    def __init__(self):
        super().__init__()
        self.gameview = gameview.GameView()
        self.enemy = Nemico()
        self.pilota = None
        self.player_sprite = None
        self.enemy_sprite = None
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
        self.era_in_aria = False
        self.shift = False
        self.tempo_crouch = 0.0
        self.win_rate = 0
        self.movement_left = PLAYER_MOVEMENT_SPEED
        self.movement_right = PLAYER_MOVEMENT_SPEED
        self.jump = PLAYER_JUMP_SPEED
        self.camera = arcade.Camera2D()
        self.enemy_list = self.enemy.enemy_list
        self.vita_5 = arcade.load_texture("./immagini/tiles/vita_5.png")
        self.vita_4 = arcade.load_texture("./immagini/tiles/vita_4.png")
        self.vita_3 = arcade.load_texture("./immagini/tiles/vita_3.png")
        self.vita_2 = arcade.load_texture("./immagini/tiles/vita_2.png")
        self.vita_1 = arcade.load_texture("./immagini/tiles/vita_1.png")
        self.vita_0 = arcade.load_texture("./immagini/tiles/vita_0.png")
        self.font = arcade.load_font("8094231822.ttf")
        self.life = self.vita_5
        self.conta_vita = 5
        self.loser = False
        #self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        #self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.timer_text = arcade.Text(f"Time: 00:00.000", x=730, y=1000, color = arcade.csscolor.BLACK, font_size = 20)
        self.timer_fine_livello_text = arcade.Text(f"Time: 00:00.000", x=500, y=800, color = arcade.csscolor.BLACK, font_name="Broadway BT", font_size = 30)
        self.lose = arcade.Text("HAI PERSO!", x=0, y=WINDOW_HEIGHT // 2, anchor_x="center", anchor_y="center", color = arcade.csscolor.PURPLE, font_name="Broadway BT", font_size=200)
        self.conto_win = arcade.Text(f"Ti mancano 5 livelli per vincere", x=0, y=800, anchor_x="center", anchor_y="center", color = arcade.csscolor.DARK_RED, font_name="Broadway BT", font_size=20)   
        self.setup()
        self.gameview.pan_camera_to_player()

    
    def setup(self):
        self.scene = arcade.Scene()
        self.enemy_list = self.enemy.enemy_list
        self.player_sprite = self.gameview.player_sprite
        self.vettura_sprite = arcade.Sprite("./immagini/tiles/vettura2.png", scale=0.25)
        self.player_list=arcade.SpriteList()
        self.player_sprite.scale = 0.5
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        self.scene.add_sprite_list("Enemy", use_spatial_hash=True)
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)
        self.scene.add_sprite_list("Bandiera", use_spatial_hash=True)
        for x in range(0, 12000, 64):
            wall = arcade.Sprite("./immagini/tiles/terreno.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        for x in range(0, 12000, 64):
            wall = arcade.Sprite("./immagini/tiles/terreno.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = WINDOW_HEIGHT + 50
            self.scene.add_sprite("Walls", wall)

        for x in range(10):
            spawn_x = random.randint(500, 8800)
            enemy = self.enemy._crea_nemico(spawn_x, 110)
            self.scene.add_sprite("Enemy", enemy)
            self.enemy_list.append(enemy)

        for x in range(500, 9200, 500):
            wall = arcade.Sprite("./immagini/tiles/terreno_alto.png", scale=TILE_SCALING)
            wall.center_x = random.randint(500, 8800)
            wall.center_y = 440
            self.scene.add_sprite("Walls", wall)
            # potrei mettere nemico sul terreno alto con x = wall.center_x + qualcosa e y = wall.center_y + 150
            enemy = self.enemy._crea_nemico(wall.center_x + 50, wall.center_y + 76)
            if random.random() < 0.6: # 60% di possibilità di spawnare un nemico sul terreno alto
                self.scene.add_sprite("Enemy", enemy)
                self.enemy_list.append(enemy)

        for x in range(128, 9200, 750):
            wall = arcade.Sprite("./immagini/tiles/muro.png", scale=TILE_SCALING)
            wall.scale= 0.16
            wall.center_x = random.randint(300, 9000)
            wall.center_y = 110
            self.scene.add_sprite("Walls", wall)

        coordinate_list = [[-100, 165], [12000, 165], [-100, 96], [12000, 96], [-100, 234], [12000, 234], [-100, 303], [12000, 303], [-100, 372], [12000, 372], [-100, 441], [12000, 441], [-100, 510], [12000, 510], [-100, 579], [12000, 579], [-100, 648], [12000, 648], [-100, 717], [12000, 717], [-100, 786], [12000, 786], [-100, 855], [12000, 855], [-100, 924], [12000, 924], [-100, 993], [12000, 993], [-100, 1062], [12000, 1062]]
        for coordinate in coordinate_list:
            walls = arcade.Sprite("./immagini/tiles/muro.png", scale=0.16)
            walls.position = coordinate
            self.scene.add_sprite("Walls", walls)
        
        for x in range(128, 9600, 700):
            coin = arcade.Sprite("./immagini/item.png", scale=COIN_SCALING)
            coin.center_x = random.randint(300, 9100)
            coin.center_y = random.randint(96, 650)
            self.scene.add_sprite("Coins", coin)
            #14 coins totali

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
        self.score_text = arcade.Text(f"Score: {self.score}", x=0, y=1000, anchor_x="center", color = arcade.csscolor.BLACK, font_size = 30)
        self.avviso = arcade.Text(f"Raccogli tutti i 14 pezzi di motore per attivare la vettura!", x=0, y=1050, anchor_x="center", color = arcade.csscolor.BLACK, font_size = 20)
        self.pause_text = arcade.Text(f"Premi ESC per mettere in pausa", x=-800, y=1000, color = arcade.csscolor.BLACK, font_size = 15)
        
    
    def _aggiorna_animazione(self):
        ps = self.player_sprite
        on_ground = self.physics_engine.can_jump()

        if self.era_in_aria and on_ground:
            self.tempo_crouch = 0.4

        self.era_in_aria = not on_ground

        if self.win is not None:
            ps.imposta_animazione("lose")
        elif not on_ground:
            ps.imposta_animazione("jump")
        elif self.tempo_crouch > 0:
            ps.imposta_animazione("crouch")
        elif ps.change_x != 0:
            ps.imposta_animazione("run")
        else:
            ps.imposta_animazione("idle")

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
        arcade.draw_texture_rect(self.life, arcade.LBWH(self.position_1, WINDOW_HEIGHT - 350, 781, 350))
        self.score_text.draw()
        self.timer_text.draw()
        self.pause_text.draw()
        self.conto_win.draw()
        if self.loser:
            self.window.clear()
            self.lose.draw()
        if self.win!= None:
            self.window.clear()
            self.win.draw()
            self.timer_fine_livello_text.draw()
    def on_update(self, delta_time: float):
        self.vettura_sprite.center_x -= self.velocita * delta_time
        self.gameview.on_update(delta_time)
        self.physics_engine.update()
        self.physics_engine_macchine.update()
        self.enemy.on_update(delta_time)
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            #arcade.play_sound(self.collect_coin_sound)
            self.score += 1
            self.score_text.text = f"Score: {self.score}"
            
        vettura_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Vettura"]
        )
        for vettura in vettura_hit_list:
            if self.score == 1050:
                self.scene["Vettura"].remove(vettura)
                self.jump = 0
                self.movement_left = 0
                self.movement_right = 10
                self.scene["Player"].remove(self.player_sprite)
                self.vettura_sprite.center_x = 9300
                self.vettura_sprite.center_y = 128
                self.scene.add_sprite("Vettura_p", self.vettura_sprite)
             
        enemy_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Enemy"]
        )
        for enemy in enemy_hit_list:
            self.conta_vita -= 1
            if self.conta_vita == 4:
                self.life = self.vita_4
            elif self.conta_vita == 3:
                self.life = self.vita_3
            elif self.conta_vita == 2:
                self.life = self.vita_2
            elif self.conta_vita == 1:
                self.life = self.vita_1
            elif self.conta_vita == 0:
                self.life = self.vita_0
                self.loser = True
                self.jump = 0
                self.movement_left = 0 
                self.movement_right = 0
            self.setup()
        
        bandiera_hit_list = arcade.check_for_collision_with_list(
            self.vettura_sprite, self.scene["Bandiera"]
        )
        for bandiera in bandiera_hit_list:
            self.win_rate += 1
            self.setup()
            self.conto_win.text = f"Ti mancano {5 - self.win_rate} livelli per vincere"
            self.jump = PLAYER_JUMP_SPEED
            self.movement_left = PLAYER_MOVEMENT_SPEED 
            self.movement_right = PLAYER_MOVEMENT_SPEED
            if self.win_rate == 5:
                self.andata = False
                self.jump = 0
                self.movement_left = 0 
                self.movement_right = 0
                self.timer_fine_livello = self.elapsed_time
                minutes = int(self.timer_fine_livello) // 60
                seconds = int(self.timer_fine_livello) % 60
                millesimi = int((self.timer_fine_livello % 1) * 1000)
                self.timer_fine_livello_text.text = f"Hai vinto in: {minutes:02d}:{seconds:02d}.{millesimi:03d}"
                self.win = arcade.Text("HAI VINTO!", x=self.player_sprite.center_x, y=300, anchor_x="center", anchor_y="center", color = arcade.csscolor.PURPLE, font_name="Broadway BT", font_size=200)
        
        if self.andata:
            self.elapsed_time += delta_time
        minutes = int(self.elapsed_time) // 60
        seconds = int(self.elapsed_time) % 60
        millesimi = int((self.elapsed_time % 1) * 1000)
        self.time = f"{minutes:02d}:{seconds:02d}.{millesimi:03d}"
        self.timer_text.text = f"Time: {self.time}"

        self.timer_text.x = self.player_sprite.center_x + 730
        self.score_text.x = self.player_sprite.center_x
        self.avviso.x = self.player_sprite.center_x
        self.pause_text.x = self.player_sprite.center_x - 850
        self.conto_win.x = self.player_sprite.center_x
        self.lose.x = self.player_sprite.center_x
        
        if self.player_sprite.change_x < 0: 
            self.player_sprite.scale = (-0.5, 0.5)
        elif self.player_sprite.change_x > 0:
            self.player_sprite.scale = (0.5, 0.5)
        
        if self.tempo_crouch > 0:
            self.tempo_crouch -= delta_time

        self.position_1 = self.player_sprite.center_x - 380

        self._aggiorna_animazione()

    def on_key_press(self, tasto, modificatori):
        if tasto == arcade.key.MOD_SHIFT or tasto == arcade.key.LSHIFT or tasto == arcade.key.RSHIFT:
            self.shift = True
        import pause
        if tasto == arcade.key.ESCAPE:
            pause_view = pause.PauseView(self)
            self.window.show_view(pause_view)
        if tasto == arcade.key.UP or tasto == arcade.key.W or tasto == arcade.key.SPACE:
            if self.shift:
                jump = self.jump + 7
            else:
                jump = self.jump
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = jump
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
        elif tasto == arcade.key.MOD_SHIFT or tasto == arcade.key.LSHIFT or tasto == arcade.key.RSHIFT:
            self.shift = False