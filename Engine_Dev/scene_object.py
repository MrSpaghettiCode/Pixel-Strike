import pygame

class box:
    #we need this class, because pygame.Rect is not hashable :C
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.x + self.width, self.y + self.height)
    
    def collides_with(self, hitbox):
        self_x2 = self.x + self.width
        self_y2 = self.y + self.height

        other_x2 = hitbox.x + hitbox.width
        other_y2 = hitbox.y + hitbox.height

        return self.x < other_x2 and self_x2 > hitbox.x and self.y < other_y2 and self_y2 > hitbox.y

class drawable(box):
    def __init__(self, x, y, width, height, layer):
        super().__init__(x, y, width, height)
        self.layer = layer
     
    def draw_rect(self, screen:pygame.surface.Surface, color):
         pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
    
    #this method exists for polymorphism reasons
    #should be overridden in classes that require any form of sprite drawing
    def draw(self):
        pass

class object_2d(drawable):
    def __init__(self, x, y, width, height, layer = 0, container = None):
        super().__init__(x, y, width, height, layer)    #add logic for container later
        self._click_methods = []

    def clicked(self, mouse_pos) -> bool:
        click_pos = pygame.Rect(mouse_pos[0], mouse_pos[1] , 3, 3)
        return self.collides_with(click_pos)
    
    #this invokes every method in the _click_methods list
    def click(self):
        [m() for m in self._click_methods] 
    
    def on_click(self, metod_to_run):
        self._click_methods.append(metod_to_run)
    
    def draw(self, screen):
        super().draw_rect(screen, (100, 150, 200))

    #not sure if this works. we will see
    def kill(self, container):
        container.pop(self)

    #this should be overridden in classes that require any form of moving
    def move(self):
        pass 
