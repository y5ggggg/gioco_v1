import arcade
from gameview import GameView


class MenuView(arcade.View):
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