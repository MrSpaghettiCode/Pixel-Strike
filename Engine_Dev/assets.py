import pygame
import os

ASSETS_PATH = os.path.realpath(os.path.dirname(__file__)) + "\\assets"

class Assets:
    ui = {}
    unit = {}

    @staticmethod
    def init():
        Assets._load_ui_assets()
        Assets._load_unit_assets()

    @staticmethod
    def _load_ui_assets():
        ui_path = ASSETS_PATH + "\\ui"
        for _, _, file_names in os.walk(ui_path):
            for file_name in file_names:
                file_path = f"{ui_path}\\{file_name}"
                sprite = Assets.get_and_scale_Image(file_path)
                Assets.ui.update({file_name.split('.')[0]:sprite})

    @staticmethod
    def _load_unit_assets():
        #   this converts the 'units' folder into a dictionary
        #   every KeyValuePair looks like this -> 
        #   {"unit_name":{"frame_set_name":[frame1, frame2, ...]}}
        units_path = ASSETS_PATH + "\\units"
        for unit_dir in os.listdir(units_path):
            unit_name = unit_dir
            Assets.unit.update({unit_name:{}})

            for sprite_dir in os.listdir(units_path + f"\\{unit_dir}"):
                sprites = units_path + f"\\{unit_dir}\\{sprite_dir}"
                Assets.unit[unit_name].update({sprite_dir:[]})

                for _, _, file_names in os.walk(sprites):
                    for file_name in file_names:
                        sprite_path = f"{sprites}\\{file_name}"
                        sprite = Assets.get_and_scale_Image(sprite_path, 0)   
                        Assets.unit[unit_name][sprite_dir].append(sprite)
            
    @staticmethod
    def scale_image(image:pygame.surface, scale_ammount):
        size = image.get_size()
        return pygame.transform.scale(image, (size[0] * scale_ammount, size[1]* scale_ammount)).convert_alpha()

    @staticmethod
    def get_and_scale_Image(path, rotate = 90, scale = (100, 100)):
        return pygame.transform.scale(pygame.transform.rotate(pygame.image.load(path), rotate), scale).convert_alpha()