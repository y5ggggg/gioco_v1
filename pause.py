import arcade
import arcade.gui
import gioco
import gameview

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class PauseView(arcade.View):
    def __init__ (self, gioco_view):
        super().__init__ ()
        self.gioco_view = gioco_view
        self.set=gioco.mywindow
        self.gameview= gameview.GameView()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        resume_button = arcade.gui.UIFlatButton(text="RIPRENDI", width=200)
        menu_button   = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button   = arcade.gui.UIFlatButton(text="ESCI", width=200)

        resume_button.on_click = self.on_resume
        menu_button.on_click   = self.on_menu
        quit_button.on_click   = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(resume_button)
        layout.add(menu_button)
        layout.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorLayout(  
                children=[layout]
            )
        )
        
        
    def on_resume(self, event):
        self.window.show_view(self.gioco_view)

    def on_menu(self, event):
        import menu
        menu_view = menu.MenuView()
        menu_view.window = self.window
        self.set.setup(self)
        self.window.show_view(menu_view)

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.gioco_view.on_draw()
        arcade.draw_rect_filled(
            arcade.XYWH(self.position, WINDOW_HEIGHT / 2, WINDOW_WIDTH, WINDOW_HEIGHT),
            (0, 0, 0, 150)
        )
        self.pause_text.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.gioco_view.on_update(delta_time)
        self.pause_text=arcade.Text("PAUSA", x=self.gioco_view.player_sprite.center_x, y = WINDOW_HEIGHT/2 + 150, color = arcade.color.WHITE, font_size = 48, anchor_x="center", anchor_y="center")
        self.position = self.gioco_view.player_sprite.center_x
    def on_hide_view(self):
        self.manager.disable()
