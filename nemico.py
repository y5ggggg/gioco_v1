import arcade
from animazione import Enemy

PATROL_RANGE = 150

class Nemico(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_list = arcade.SpriteList()

    def _crea_nemico(self, x: float, y: float, velocity: float = 3 ) -> Enemy:
        enemy = Enemy(scala=0.35)
        enemy.center_x = x
        enemy.center_y = y
        enemy.change_x = velocity
        enemy.patrol_origin = x
        enemy.velocità = velocity
        self.stop_ = 0.0
        enemy.imposta_animazione("run")
        return enemy
    
    def on_update(self, delta_time: float):
    
        for enemy in self.enemy_list:
            if self.stop_ >= 0:
                self.stop_ -= delta_time
                enemy.imposta_animazione("idle")
                enemy.update_animation(delta_time)
                continue
            else:
                enemy.imposta_animazione("run")
            enemy.center_x += enemy.change_x
            distanza = enemy.center_x - enemy.patrol_origin
            if distanza <= -PATROL_RANGE:
                enemy.center_x = enemy.patrol_origin - PATROL_RANGE
                self.stop_=1.0
                enemy.change_x = enemy.velocità
            elif distanza >= PATROL_RANGE:
                enemy.center_x = enemy.patrol_origin + PATROL_RANGE
                self.stop_=1.0  
                enemy.change_x = -enemy.velocità

            if enemy.change_x < 0: 
                enemy.scale = (-0.35, 0.35)
            else:
                enemy.scale = (0.35, 0.35)

            enemy.update_animation(delta_time)
    