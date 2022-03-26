## INTO THE BACKROOMS: ITEM CLASSES FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

# Temp init to draw base items instead of importing images.
import pygame

pygame.init()

class StaticEntity :
    """A non-moving entity (trap, item, or other static object.) It's type is dictated by map generator-defined index
    value."""
    
    def __init__ (self, index, pos, name, color) :
        # Sets index to class type.
        self.class_type = index
        self.name = name

        # Places position values.
        self.mas_x, self.mas_y = pos[0], pos[1]
        self.color = color

        # Creates draw values. Manipulated by main script.
        self.entity_surf = None
        self.entity_x = None
        self.entity_y = None

    def __str__(self):
        return self.name

    def update (self, player_x, player_y, player_rect) :
        """Updates positional values, creates work surface, returns to caller. Ideally, should only be ran when
        StaticEntity would technically be in view."""

        # Updates positional value.
        pos_x = self.mas_x - player_x
        pos_y = self.mas_y - player_y

        # Creates work surface and returns to caller.
        work_surface = pygame.Surface((30, 30))
        pygame.draw.rect(work_surface, self.color, (0, 0, 30, 30))

        # Collision detection.
        self.collide_rect = pygame.Rect(pos_x, pos_y, 30, 30)

        return work_surface, pos_x, pos_y
