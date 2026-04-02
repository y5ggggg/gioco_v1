import arcade
import arcade.gui

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        play_button = arcade.gui.UIFlatButton(text="PLAY", width=200)
        quit_button = arcade.gui.UIFlatButton(text="ESCI", width=200)

        play_button.on_click = self.on_play
        quit_button.on_click = self.on_quit
        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(play_button)
        layout.add(quit_button)
        self.manager.add(arcade.gui.UIAnchorLayout(children=[layout]))
        self.sfondo = arcade.load_texture("./immagini/sfondo_menu.png")
    
    def on_play(self, event):
        import gioco
        game_view = gioco.mywindow()
        game_view.window = self.window  # Assicurati che la vista del gioco abbia accesso alla finestra
        self.window.show_view(game_view)

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.window.default_camera.use()
        arcade.set_background_color(arcade.color.YELLOW)
        arcade.draw.draw_texture_rect(self.sfondo, arcade.LBWH(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

