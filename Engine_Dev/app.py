import pygame 

from camera import Camera
from assets import Assets
from scene import menu, game

WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), 8)

pygame.display.set_caption("Pixel Strike")

if __name__ == "__main__":   
    Assets.init()                                        #   init Assets
    Camera.initialize(SCREEN, False)                     #   init Camera

    menu_scene = menu(SCREEN)                         
    game_scene = game(SCREEN)      

    while menu_scene.run:                               #   run menu scene
        menu_scene.play()

    while game_scene.run:                               #   run game scene
        game_scene.play()

