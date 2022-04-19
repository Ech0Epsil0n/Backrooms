## INTO THE BACKROOMS: ITEM CLASSES FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##
## PATHFINDING HELP FOUND HERE https://www.raywenderlich.com/3016-introduction-to-a-pathfinding ##

# Temp init to draw base items instead of importing images.
import pygame
import map_reader

pygame.init()

class StaticEntity :
    """A non-moving entity (trap, item, or other static object.) It's type is dictated by map generator-defined index
    value."""
    
    def __init__ (self, pos, index, name) :
        self.class_type = int(index)
        self.name = name

        if self.class_type >= 10 and self.class_type < 20 :
            self.image = pygame.image.load("Assets//Video//trap.png")

        elif self.class_type >= 20 :
            self.image = pygame.image.load("Assets//Video//BigKey.png")

        else :
            self.image = pygame.image.load("Assets//Video//SmallKey.png")

        self.mas_x, self.mas_y = pos[0], pos[1]

        # SETS ENTITY COLOR #
        if self.class_type < 10 :
            self.color = (0, 255, 0)

        elif self.class_type > 10 and self.class_type < 20 :
            self.color = (255, 0, 0)

        else :
            self.color = (102, 51, 153)

        self.entity_surf = None
        self.entity_x = None
        self.entity_y = None

    def use (self) :
        if self.class_type == 0 :
            print("Badoonga")

        if self.class_type == 1 :
            print("TZZZZZ")


    def update (self, player_x, player_y) :
        """Updates positional values, creates work surface, returns to caller. Ideally, should only be ran when
        StaticEntity would technically be in view."""

        # FINDS POSITIONAL VALUE #
        pos_x = self.mas_x - player_x
        pos_y = self.mas_y - player_y

        # CREATES WORK_SURF TO RETURN TO CALLER #
        work_surface = pygame.Surface((24, 24))
        work_surface.blit(self.image, (-20, -20))

        # UPDATES COLLISION HITBOX #
        self.collide_rect = pygame.Rect(pos_x, pos_y, 24, 24)

        return work_surface, pos_x, pos_y

class pathfinder :
    """A pathfinder class (more accurate to a list of functions) that deals exclusively with pathfinding."""

    # CALCULATES THE DISTANCE BETWEEN TWO TILES IN UNITS OF TILES #
    def calc_dest (self, tile_1, tile_2) :
        dist_x = tile_2.grid_x - tile_1.grid_x
        dist_y = tile_2.grid_y - tile_1.grid_y

        if dist_x < 0 :
            dist_x *= -1

        if dist_y < 0 :
            dist_y *= -1

        return (dist_x + dist_y) / 2

    def pather (self, start_tile, target_tile, tiles) :
        """Pathfinds from one start location to one end location using the A* method."""

        # INITIALIZES EMPTY LISTS #
        open_list = []
        closed_list = []
        path_list = []
        adj_list = []

        while True :
            # RESETS PATH #
            current_tile = start_tile
            path = []
            score = 0

            while True :
                # RESETS NECESSARY VARIABLES #
                add_x = -1
                add_int = 0
                adj_list = []

                while add_int < 8 :
                    # FINDS ALL ADJACENT VALID TILES #
                    new_tile = None

                    try :
                        if add_int < 3 :
                            new_tile = tiles[current_tile.grid_y - 1][current_tile.grid_x + add_x]

                        elif add_int < 6 :
                            new_tile = tiles[current_tile.grid_y][current_tile.grid_x + add_x]

                        else :
                            new_tile = tiles[current_tile.grid_y + 1][current_tile.grid_x + add_x]

                    except IndexError :
                        pass

                    if new_tile is not None :
                        if new_tile == target_tile :
                            path_list.append(new_tile)
                            return path_list

                        elif new_tile.valid == True :
                            adj_list.append(new_tile)
                            add_bool = True

                            # REMOVES DUPLICATES #
                            for tile in closed_list :
                                if tile == new_tile :
                                    add_bool = False

                            for tile in open_list :
                                if tile == new_tile :
                                    add_bool = False

                            if add_bool == True :
                                open_list.append(new_tile)

                    add_x += 1
                    add_int += 1

                    if add_x == 2 :
                        add_x = -1

                # RESETS FAVORITE TILE #
                favorite = None

                # TILE SCORING #
                lowest_score = 10000

                for tile in open_list :
                    if tile not in closed_list :
                        tile.score = (score + 1) + (self.calc_dest(target_tile, tile))

                        if tile.score < lowest_score :
                            lowest_score = tile.score
                            favorite = tile

                # ADDS FAVORITE TO CLOSED_LIST #
                closed_list.append(favorite)
                path_list.append(favorite)
                current_tile = favorite

                # UPDATES SCORE #
                score += 1
