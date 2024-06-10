
from scene_object import object_2d
from animation import animation
from assets import Assets

class tower(object_2d):
    def __init__(self, x, y, width, height, sprite_name, animation_delay = 3):
        super().__init__(x, y, width, height)
        self.animation = animation("idle", Assets.unit[sprite_name], animation_delay)

    def draw(self, screen):
        screen.blit(self.animation.play(), (self.x, self.y))
