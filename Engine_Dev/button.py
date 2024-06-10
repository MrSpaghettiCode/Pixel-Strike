from scene_object import object_2d

import pygame

pygame.font.init()

class btn(object_2d):
    _font = pygame.font.SysFont('Comic Sans MS', 30)

    def __init__(self, x, y, width, height, text = ""):
        super().__init__(x, y, width, height, layer=0)
        self.text = text

    def draw(self, screen):
        super().draw(screen)
        rendered_text = btn._font.render(self.text, False, (0, 0, 0))
        screen.blit(rendered_text, (self.x + self.width*0.3, self.y + self.height*0.5))
            