import arcade
import menu

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "Platformer"


class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        
        mioMenu = menu.MenuView()
        self.show_view(mioMenu)

def main():
    window = MyGame()
    arcade.run()

if __name__ == "__main__":
    main()
