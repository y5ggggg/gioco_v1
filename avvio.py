import arcade
import menu

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_TITLE = "Aiuta il pilota"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, fullscreen=True)
        
        mioMenu = menu.MenuView()
        self.show_view(mioMenu)

def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
