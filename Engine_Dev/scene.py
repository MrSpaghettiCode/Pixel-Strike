import pygame
import random

from spatial_hashing import Collision_map
from scene_object import object_2d
from button import btn
from assets import Assets
from camera import Camera
from unit import unit
from grid import grid

FPS = 60

pygame.display.init()

class scene:
    def __init__(self, screen, fps = FPS, col_cell_cize = 100, col_layers = [1]):
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.screen = screen
        self.run = True
        
        #this list contains all layer-id's that have collision enabled
        self._col_layers = []
        self.objects = {}
        '''
            This dictionary holds all object_2d's in this scene within layers
            Each layer is a list of object_2d's
            
                Layer 0 -> UI       # default
                Layer 1 -> Units
            
        '''
        self.add_col_to_layers(col_layers)
        Collision_map.initialize(col_cell_cize)

    def add_col_to_layers(self, layers):
        for layer in layers:
            if self.objects.get(layer) is None:
                self.objects.update({layer:[]})

            self._col_layers.append(layer)

    def add(self, objects=[]):
        #without copy, this can crash some enumeration somewere...
        object_2d_copy = self.objects.copy()
        for object in objects:
            object:object_2d

            #this checks if the layer was already added to object_2d's
            #   if not -> add layer and object
            if object_2d_copy.get(object.layer) is None:
                object_2d_copy.update({object.layer:[object]})
                continue
            
            #   else -> add object to list in layer
            object_2d_copy[object.layer].append(object)

        #copy back. just to be safe
        self.objects = object_2d_copy.copy()

    def end(self):
        self.run = False
    
    def handle_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    
                case pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    #implement spacial hashing here, this sucks (would also be important for selecting units)
                    for object in self.objects[0]: #weil ui layer
                        if object.clicked(mouse_pos):
                            object.click()
                            break

    def draw(self):
        for layer in self.objects.keys():
            for object in self.objects[layer]:
                object.draw(self.screen)
        
        if Camera.selection_rect:
            pygame.draw.rect(self.screen, (255, 0, 0), Camera.selection_rect, 2)

        pygame.display.flip()

    #when overridden, this method contains everything that should happen within this scene
    def behaviour(self):
        pass
    
    #same, but only called once at the start of the scene
    def on_start(self):
        pass

    def play(self):
        self.on_start()
        while self.run:
            self.handle_events()
            self.Handle_collision()

            self.behaviour()

            self.draw()
            self.clock.tick(self.fps)

    def Handle_collision(self):
        Collision_map.reset()
        object: unit

        #build collision map
        for layer in self._col_layers:
            for object in self.objects[layer]:
                Collision_map.add_rect(object.get_rect(), object)
                #maybe add layers to coll_map
                #or just exclude layers from collision map?
        
        #check collision
        for layer in self._col_layers:
            for object in self.objects[layer]:
                 for pc in Collision_map.potential_collisions(object.get_rect(), object):
                        if pc.collides_with(object.get_rect()):
                            pass

                            #do collision shit
        

class game(scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen:pygame.surface.Surface
        self.dims = self.screen.get_size()

        Camera.allow_unit_selection()

    
    def on_start(self):
        x = self.dims[0]-400
        y = self.dims[1]*0.96
        
        slime_spawner = btn(x, y, 50, 50,"Slime")
        slime_spawner.on_click(self.spawn_slime)

        crab_spawner = btn(x + 100, y, 50, 50,"Crab")
        crab_spawner.on_click(self.spawn_crab)
        
        tower_spawner = btn(x + 200, y, 50, 50,"Tower")
        tower_spawner.on_click(self.spawn_tower)

        self.btn_holder = grid(self.dims[0]-400, self.dims[1]*0.96, 800, 180, 100, 50)
        self.btn_holder.add([slime_spawner, crab_spawner, tower_spawner])

        self.add(self.btn_holder.cells)
    
    def spawn_tower(self):
        for i in range(100):
            self._spawn_unit("tower")

    def spawn_slime(self):
        for i in range(100):
            self._spawn_unit("slime")

    def spawn_crab(self):
        for i in range(100):
            self._spawn_unit("crab")

    def _spawn_unit(self, type):
        x, y = random.randint(0, self.dims[0]-100), random.randint(0, self.dims[1] - 250)
        size = (50, 50)

        u = unit(x, y, size[0], size[1], type)

        u.on_click(u.bounce_on_click)

        self.add([u])
    
    def draw(self):
        self.screen.fill((150, 150, 150))
        #self.grid.draw(self.screen)

        super().draw()

    def behaviour(self):
        Camera.handle_movement()

        #move all units in layer 1
        if not self.objects.get(1):
            return
        
        for unit in self.objects[1]:
            unit.move()

class menu(scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen:pygame.surface.Surface
        dims = self.screen.get_size()
        
        quit_btn = btn(100, 400, 200, 200, "quit")
        play_btn = btn(350, 400, 200, 200, "play")

        quit_btn.on_click(self.on_quitbtn_click)
        play_btn.on_click(self.on_playbtn_click)

        self.add([quit_btn, play_btn])

    def on_quitbtn_click(self):
        print("bye")
        pygame.quit()
    
    def on_playbtn_click(self):
        print("starting game")
        self.end()
    
    def draw(self):
        self.screen.fill((150, 150, 150))

        super().draw()