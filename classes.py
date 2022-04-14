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
        # Sets index to class type.
        self.class_type = int(index)
        self.name = name

        # Loads entity image.
        if self.class_type >= 10 and self.class_type < 20 :
            self.image = pygame.image.load("Assets//Video//trap.png")

        elif self.class_type >= 20 :
            self.image = pygame.image.load("Assets//Video//BigKey.png")

        else :
            self.image = pygame.image.load("Assets//Video//SmallKey.png")

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

    def use (self) :
        if self.class_type == 0 :
            print("Badoonga")

        if self.class_type == 1 :
            print("TZZZZZ")


    def update (self, player_x, player_y) :
        """Updates positional values, creates work surface, returns to caller. Ideally, should only be ran when
        StaticEntity would technically be in view."""

        # Updates positional value.
        pos_x = self.mas_x - player_x
        pos_y = self.mas_y - player_y

        # Creates work surface and returns to caller.
        work_surface = pygame.Surface((24, 24))
        work_surface.blit(self.image, (-20, -20))

        # Collision detection.
        self.collide_rect = pygame.Rect(pos_x, pos_y, 24, 24)

        return work_surface, pos_x, pos_y

class pathfinder :
    """A pathfinder class (more accurate to a list of functions) that deals exclusively with pathfinding."""

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

        # Creates list for data management.
        open_list = []
        closed_list = []
        path_list = []
        adj_list = []

        while True :
            # Establishes base tile and resets path list..
            current_tile = start_tile
            score = 0

            while True :
                # Adds all nearby tile into open_list.
                add_x = -1
                add_int = 0
                adj_list = []

                while add_int < 8 :
                    # Finds all adjacent valid tiles. (Non-walls and non-used.)
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

                            # Ensures the pather does not add duplicates to closed or open.
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

                # Resetting favorite.
                favorite = None

                # Finds the shortest path to the target.
                lowest_score = 10000

                # Tile scoring.
                for tile in open_list :
                    if tile not in closed_list :
                        tile.score = (score + 1) + (self.calc_dest(target_tile, tile))

                        if tile.score < lowest_score :
                            lowest_score = tile.score
                            favorite = tile

                # Adds favorite to closed_list.
                closed_list.append(favorite)
                path_list.append(favorite)
                current_tile = favorite

                # Changes score to reflect new value.
                score += 1
