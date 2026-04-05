import arcade

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Cronometro")
        self.elapsed_time = 0.0 # secondi trascorsi

    def on_update(self, delta_time):
        self.elapsed_time += delta_time # delta_time = secondi dall'ultimo frame

    def on_draw(self):
        self.clear()

        # Formatta come MM:SS
        minutes = int(self.elapsed_time) // 60
        seconds = int(self.elapsed_time) % 60
        millesimi = int((self.elapsed_time % 1) * 1000)
        timer_text = f"{minutes:02d}:{seconds:02d}.{millesimi:03d}"
        arcade.draw_text(timer_text, 400, 550, arcade.color.WHITE, 36, anchor_x="center")

game = MyGame()
arcade.run()
