import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

TILE_SCALING = 0.5
COIN_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class mywindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE
        self.player_texture = None
        self.player_sprite = None
        self.player_list = None

        self.wall_list = None
        self.camera = None
        self.coin_list = None

        

        self.lista_pilota = arcade.SpriteList()
        self.sfondo = arcade.load_texture("./immagini/sfondo1.png")
        self.pilota = arcade.load_texture("./immagini/pilota1.png")
        self.player_sprite = arcade.Sprite(self.pilota)
        self.player_list=arcade.SpriteList()
        self.player_list.append(self.player_sprite)
        self.player_sprite.scale = 0.5
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        for x in range(0, 1250, 64):
            wall = arcade.Sprite("./immagini/tiles/terreno.png", scale=TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:
            wall = arcade.Sprite("./immagini/tiles/muro.png", scale=TILE_SCALING)
            wall.scale= 0.1211
            wall.position = coordinate
            self.wall_list.append(wall)
        for x in range(128, 1250, 256):
            coin = arcade.Sprite("./images/items.png", scale=COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.coin_list.append(coin)
        
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, walls=self.wall_list, gravity_constant=GRAVITY
        )
        self.camera = arcade.Camera2D()
        self.velocita = 4

        self.setup()
    
    def setup(self):
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)
    
    def on_draw(self):
        self.clear()
        self.camera.use()
        self.coin_list.draw()
        arcade.draw.draw_texture_rect(self.sfondo, arcade.types.Viewport(0,0,WINDOW_WIDTH,WINDOW_HEIGHT))
        self.player_list.draw()
        self.wall_list.draw()

    def on_update(self, delta_time):
        self.camera.position = self.player_sprite.position
        self.physics_engine.update()
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
    def on_key_press(self, tasto, modificatori):
        if tasto == arcade.key.ESCAPE:
            self.setup()
        if tasto == arcade.key.UP or tasto == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        if tasto == arcade.key.LEFT or tasto == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif tasto == arcade.key.RIGHT or tasto == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        
        if tasto == arcade.key.LEFT or tasto == arcade.key.A:
            self.player_sprite.change_x = 0
        elif tasto == arcade.key.RIGHT or tasto == arcade.key.D:
            self.player_sprite.change_x = 0
        

def main():
    window = mywindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()