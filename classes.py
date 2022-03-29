## INTO THE BACKROOMS: ITEM CLASSES FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

# Temp init to draw base items instead of importing images.
import pygame

pygame.init()

class StaticEntity :
    """A non-moving entity (trap, item, or other static object.) It's type is dictated by map generator-defined index
    value."""
    
    def __init__ (self, pos, index, name) :
        # Sets index to class type.
        self.class_type = int(index)
        self.name = name

        # Loads entity image.
        if self.class_type >= 10 and self.class_type < 20 :
            self.image = pygame.image.load("Assets/trap.png")

        elif self.class_type >= 20 :
            self.image = pygame.image.load("Assets/BigKey.png")

        else :
            self.image = pygame.image.load("Assets/SmallKey.png")

        # Loads positional data.
        self.mas_x, self.mas_y = pos[0], pos[1]

        # Sets color based on type.
        if self.class_type < 10 :
            self.color = (0, 255, 0)

        elif self.class_type > 10 and self.class_type < 20 :
            self.color = (255, 0, 0)

        else :
            self.color = (102, 51, 153)

        # Creates draw values. Manipulated by main script.
        self.entity_surf = None
        self.entity_x = None
        self.entity_y = None

    def update (self, player_x, player_y, player_rect) :
        """Updates positional values, creates work surface, returns to caller. Ideally, should only be ran when
        StaticEntity would technically be in view."""

        # Updates positional value.
        pos_x = self.mas_x - player_x
        pos_y = self.mas_y - player_y

        # Creates work surface and returns to caller.
        work_surface = pygame.Surface((24, 24))
        work_surface.blit(self.image, (-20, -20))

        # Collision detection.
        self.collide_rect = pygame.Rect(pos_x, pos_y, 64, 64)

        return work_surface, pos_x, pos_y
