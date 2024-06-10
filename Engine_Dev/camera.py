import pygame

pygame.init()

class Camera:
    x, y = 0, 0
    rel = 0, 0
    selection_rect = None

    _screen = None
    _dims = None

    _selection_rect_ini_x, _selection_rect_ini_y = 0, 0
    _selection_rect_end_x, _selection_rect_end_y = 0, 0
    _selection_start = False

    _moving = False
    _allow_unit_selection = False

    @staticmethod
    def allow_unit_selection():
        Camera._allow_unit_selection = True

    @staticmethod
    def initialize(screen, allow_unit_selection):
        Camera._screen = screen
        Camera._dims = screen.get_size()
        Camera._allow_unit_selection = allow_unit_selection

    @staticmethod
    def handle_movement():
        _, m_wheel_down, _ = pygame.mouse.get_pressed()

        #get the movement of the mouse 
        #relative to the last frame this method was called in
        rel_x, rel_y = pygame.mouse.get_rel()

        Camera._handle_selection()

        if not m_wheel_down:
            Camera._moving = False
            Camera.rel = 0, 0
            return

        Camera._moving = True
        Camera.x, Camera.y = pygame.mouse.get_pos()

        Camera.rel = (rel_x, rel_y)
    
    @staticmethod
    def _handle_selection():
        if not Camera._allow_unit_selection:
            return
        
        #this has to be called here, before get_pressed(), because the Doc's say so...
        pygame.event.get()
        if pygame.mouse.get_pressed()[0]:
            if Camera._selection_start:
                return
            
            Camera._selection_start = True
            Camera._selection_rect_ini_x, Camera._selection_rect_ini_y = pygame.mouse.get_pos()
            return
        
        if not Camera._selection_start:
            return
        
        Camera._selection_start = False
        Camera._selection_rect_end_x, Camera._selection_rect_end_y = pygame.mouse.get_pos()
        Camera._calc_selection_rect()
       

    @staticmethod
    def _calc_selection_rect():
        selection_rect_width = Camera._selection_rect_ini_x - Camera._selection_rect_end_x
        selection_rect_height = Camera._selection_rect_ini_y - Camera._selection_rect_end_y

        #pygame does not display rects with negative width or height, so we switch things up
        if selection_rect_width > 0:
            Camera.create_rect(
                Camera._selection_rect_end_x,
                Camera._selection_rect_end_y,
                selection_rect_width,
                selection_rect_height
            )
            return

        Camera.create_rect(
            Camera._selection_rect_ini_x,
            Camera._selection_rect_ini_y,
            -selection_rect_width,
            -selection_rect_height
        )

    @staticmethod
    def create_rect(x, y, width, height):
        #like mentioned above, we need to account for negative numbers...
        if width < 0:
            x -= width
            width *= -1

        if height < 0:
            y += height
            height *= -1

        Camera.selection_rect = (
            x,
            y,
            width,
            height
        )