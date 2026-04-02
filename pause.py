import arcade
import arcade.gui

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 23

class PauseView(arcade.View):
    def __init__ (self, gioco_view):
        super().__init__ ()
        self.gioco_view = gioco_view
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        
        self.font = arcade.load_font("8094231822.ttf")
        resume_button = arcade.gui.UIFlatButton(text="RIPRENDI", width=200)
        reset_button = arcade.gui.UIFlatButton(text="RIAVVIA", width=200)
        menu_button = arcade.gui.UIFlatButton(text="MENU PRINCIPALE", width=200)
        quit_button = arcade.gui.UIFlatButton(text="ESCI", width=200)

        resume_button.on_click = self.on_resume
        reset_button.on_click = self.on_reset
        menu_button.on_click = self.on_menu
        quit_button.on_click = self.on_quit

        layout = arcade.gui.UIBoxLayout(spacing=20)
        layout.add(resume_button)
        layout.add(reset_button)
        layout.add(menu_button)
        layout.add(quit_button)

        self.manager.add(
            arcade.gui.UIAnchorLayout(  
                children=[layout]
            )
        )
        
        
    def on_resume(self, event):
        self.window.show_view(self.gioco_view)

    def on_reset(self, event):
        import gioco
        self.gioc = gioco.mywindow()
        self.gioc.window = self.window
        self.window.show_view(self.gioc)
        self.gioc.elapsed_time = 0.0
        self.gioc.jump = PLAYER_JUMP_SPEED
        self.gioc.movement_left = PLAYER_MOVEMENT_SPEED
        self.gioc.movement_right = PLAYER_MOVEMENT_SPEED

    def on_menu(self, event):
        import menu
        self.manager.disable()
        self.gioco_view.gameview.camera.position=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
        menu_view = menu.MenuView()
        self.window.show_view(menu_view)

    def on_quit(self, event):
        arcade.exit()

    def on_draw(self):
        self.gioco_view.on_draw()
        arcade.draw_rect_filled(
            arcade.XYWH(self.position, WINDOW_HEIGHT / 2, 3000, WINDOW_HEIGHT),
            (0, 0, 0, 150)
        )
        self.pause_text.draw()
        self.manager.draw()

    def on_update(self, delta_time):
        self.pause_text=arcade.Text("PAUSA", x=self.gioco_view.player_sprite.center_x, y = WINDOW_HEIGHT/2 + 200, color = arcade.color.WHITE, font_name = "Broadway BT", font_size = 48, anchor_x="center", anchor_y="center")
        self.position = self.gioco_view.player_sprite.center_x

    def on_hide_view(self):
        self.manager.disable()
