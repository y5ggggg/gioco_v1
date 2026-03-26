import arcade
import arcade.gui


class MenuView(arcade.View):
    '''
    def __init__(self):
        self.gameview = GameView()

    def on_draw(self):
        self.clear()
        arcade.draw_text("Noi siamo F1", 480, 350,
                         arcade.color.WHITE, font_size=48, anchor_x="center")
        arcade.draw_text("Premi INVIO per iniziare", 480, 250,
                         arcade.color.LIGHT_GRAY, font_size=20, anchor_x="center")

    def on_key_press(self, tasto, modifiers):
        if tasto == arcade.key.RETURN:
            self.gameview.setup()
            self.window.show_view(self.gameview)
            '''
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

    def on_play(self, event):
        import gioco
        game_view = gioco.mywindow()
        game_view.window = self.window  # Assicurati che la vista del gioco abbia accesso alla finestra
        self.window.show_view(game_view)

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY) 
        self.manager.draw()

    def on_hide_view(self):
        self.manager.disable()

