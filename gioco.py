import arcade

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"

class mywindow(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.lista_pilota = arcade.SpriteList()
        #self.sfondo = arcade.load_texture("")
        self.jump_pressed = False
        self.left_pressed = False
        self.right_pressed = False
        self.pilota = arcade.load_texture("./immagini/pilota1.png")
        self.player_sprite = arcade.Sprite(self.pilota)
        self.player_sprite.scale = 0.5
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128

        self.velocita = 4

        self.setup()
    
    def setup(self):
        pass
    
    def on_draw(self):
        self.clear()
        #arcade.draw.draw_texture_rect(self.sfondo, arcade.types.Viewport(0,0,600,600))
        arcade.draw_sprite(self.player_sprite)

    def on_update(self, delta_time):
        # Calcola movimento in base ai tasti premuti
        change_x = 0
        change_y = 0
        
        if self.left_pressed:
            change_x -= self.velocita
        if self.right_pressed:
            change_x += self.velocita
        if self.jump_pressed:
            change_y += 10

    def on_key_press(self, tasto, modificatori):
        if tasto in (arcade.key.UP, arcade.key.SPACE):
            self.jump_pressed = True
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = True

    def on_key_release(self, tasto, modificatori):
        """Gestisce il rilascio dei tasti"""
        if tasto in (arcade.key.UP, arcade.key.W):
            self.up_pressed = False
        elif tasto in (arcade.key.DOWN, arcade.key.S):
            self.down_pressed = False
        elif tasto in (arcade.key.LEFT, arcade.key.A):
            self.left_pressed = False
        elif tasto in (arcade.key.RIGHT, arcade.key.D):
            self.right_pressed = False

def main():
    window = mywindow()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()