import random

from animation import animation
from scene_object import object_2d
from assets import Assets
from camera import Camera

class unit(object_2d):
    def __init__(self, x, y, width, height, sprite_name, animation_delay = 3):
        super().__init__(x, y, width, height, layer=1)
        self.animation = animation("idle", Assets.unit[sprite_name], animation_delay)
        self.mass = 50

        self.max_vel = random.randint(10, 30)
        self.x_vel, self.y_vel = 0, 0
        self.vel_dec = 1-(0.9 * self.mass)

    def draw(self, screen):
        screen.blit(self.animation.play(), (self.x, self.y))

    def bounce_on_click(self):
        print("bounce_on_click")
        self.apply_colision_force(random.randint(0, 10), random.randint(0, 10))

    def apply_force(self, force_x, force_y):
        if self.x_vel < self.max_vel and self.x_vel > -self.max_vel:
            self.x_vel += force_x
        if self.y_vel < self.max_vel and self.y_vel > -self.max_vel:
            self.y_vel += force_y

    def apply_colision_force(self, x_vel, y_vel, mass):
         coll_force = (((x_vel*0.2)*(mass))*(0.1*random.randint(1, 10)), ((y_vel*0.2)*(mass))*(0.1*random.randint(1, 10)))

         self.apply_force(coll_force[0], coll_force[1])
  
    def move(self):
        self.x += self.x_vel + Camera.rel[0]
        self.y += self.y_vel + Camera.rel[1]
   
        #make velocity go down over time
        self.x_vel *= self.vel_dec
        self.y_vel *= self.vel_dec

