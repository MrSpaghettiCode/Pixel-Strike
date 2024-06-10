import pygame

from scene_object import drawable
from assets import Assets

class grid(drawable):
    def __init__(self, x, y, width, height, cell_size, color = (100, 100, 100), cell_padding = 10):
        super().__init__(x-width*0.5, y, width, height, layer=0)
        self.cell_size = cell_size
        self.color = color
        self.cells = []
        self.cell_padding = cell_padding

        self._place_cells()

    def add(self, cells):
        for cell in cells:
            self.cells.append(cell)

    def _place_cells(self):
        padding = self.cell_padding
        for cell in self.cells:
            cell.set_pos(self.x + cell.width,self.y-self.height)
            padding *= 2

    def draw(self, screen):
        for x in range(1, self.width):
            if not x % self.cell_size == 0:
                continue
            
            for y in range(1, self.height):
                if not x % self.cell_size == 0:
                    continue
                
                pygame.draw.line(screen, self.color, (x + self.x, self.y), (self.x + x,self.y -  self.height))
                if not y % self.cell_size == 0:
                    continue

                #print((x, y + self.y), (self.width, self.y + y))
                pygame.draw.line(screen, self.color, (self.x, self.y - y), (self.width + self.x, self.y - y))
