## INTO THE BACKROOMS: ITEM CLASSES FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##

# Temp init to draw base items instead of importing images.
import pygame

pygame.init()

class Item :
    """A basic item that can be picked up, equipped, and used by the player. The index (later, class_type) value is
    used by the map generator script to tell which type of item this instance of the class is."""
    
    def __init__ (self, index, pos, name, color) :
        # Sets index to class type.
        self.class_type = index
        self.name = name
        # Places position values.
        self.mas_x, self.mas_y = pos[0], pos[1]
        self.color = color
    def __str__(self):
        return self.name

    def update (self, player_x, player_y, player_rect) :
        """Updates positional values, creates work surface, returns to caller. Ideally, should only be ran when
        Item would technically be in view."""

        # Updates positional value.
        pos_x = self.mas_x - player_x
        pos_y = self.mas_y - player_y

        # Creates work surface and returns to caller.
        if self.class_type == 0 :
            work_surface = pygame.Surface((30, 30))
##            pygame.draw.rect(work_surface, (255, 255, 0), (0, 0, 30, 30))

        # Collision detection.
        collide_rect = pygame.Rect(pos_x, pos_y, 30, 30)

        return work_surface, pos_x, pos_y

    def render(self,surface):
        pygame.draw.circle(surface,self.color,(self.mas_x,self.mas_y),15)

    
    def item_pickup(self, pos_x, pos_y, player_x, player_y):
        player_pos = player_x, player_y
        item_pos = pos_x, pos_y
        
