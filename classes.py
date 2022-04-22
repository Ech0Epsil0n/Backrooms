## INTO THE BACKROOMS: ITEM CLASSES FILE ##
## CREATED ON MARCH 17TH, 2022 ##
## ETGG 1802 ##
## PATHFINDING HELP FOUND HERE https://www.raywenderlich.com/3016-introduction-to-a-pathfinding ##

# Temp init to draw base items instead of importing images.
import pygame
import map_reader
import heapq

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

    def pather (self, start_tile, target_tile, tiles, monster=None) :
        # DEFINES NECESSARY VARIABLES #

        # GENERATES HEURISTIC FOR START TILE #
        open_list = []
        heuristic = self.calc_dest(start_tile, target_tile)
        heapq.heappush(open_list, [heuristic, 0, heuristic, start_tile])

        # GENERATES NECESSARY DICTIONARIES #
        closed_list = {}
        history = {start_tile: None}

        # FORMS OPEN LIST #
        while len(open_list) > 0 :
            # TAKES MOST PROMISING TILE IN OPEN_LIST #
            total_cost, cost_so_far, heuristic, cur_tile = heapq.heappop(open_list)

            # IF CURRENT TILE IS TARGET, RETURNS HISTORY #
            if cur_tile == target_tile :
                break

            # FINDS ADJACENT TILES #
            add_x = -1
            add_y = -1
            cur_tile.adj_list = []

            while add_y != 2 :
                # ATTEMPTS TO FIND ADJACENT TILE OF A SPECIFIC LOCATION #
                new_tile = None

                try :
                    new_tile = tiles[cur_tile.grid_y + add_y][cur_tile.grid_x + add_x]

                except IndexError :
                    pass

                # ITERATES THROUGH X/Y FINDERS #
                add_x += 1

                if add_x == 2 :
                    add_x = -1
                    add_y += 1

                # ADDS NEW TILE TO ADJACENT LIST IF POSSIBLE #
                if new_tile is not None and new_tile.valid == True :
                    cur_tile.adj_list.append(new_tile)

            # ITERATES THROUGH ALL ADJACENT TILES AND MODIFIES DATA APPROPRIATELY #
            for neighbor in cur_tile.adj_list :
                # FINDS TENTATIVE NEIGHBOR COST #
                tile_dist = self.calc_dest(neighbor, target_tile)
                tentative_neighbor_cost = cost_so_far + tile_dist

                # MAKES NEW ENTRY IN OPEN_LIST IF NECESSARY #
                if neighbor not in history :
                    heapq.heappush(open_list, [tentative_neighbor_cost + tile_dist, tentative_neighbor_cost,
                                               tile_dist, neighbor])
                    history[neighbor] = cur_tile

                # REPLACES CURRENT NEIGHBOR DATA WITH MORE EFFICIENT NEIGHBOR DATA #
                # elif neighbor in closed_list and tentative_neighbor_cost < closed_list[neighbor][1] :
                #     neighbor_info = closed[neighbor]
                #     neighbor_info[1] = tentative_neighbor_cost
                #     neighbor_info[0] = tentative_neighbor_cost + neighbor_info[2]
                #     history[neighbor] = cur_tile
                #     del closed[neighbor]
                #     heapq.heappush(open_list, neighbor_info)

            closed_list[cur_tile] = [total_cost, cost_so_far, heuristic, cur_tile]

        # MODIFIES HISTORY TO REAL PATH #
        walked_list = []
        current_tile = target_tile

        while current_tile is not None :
            walked_list.insert(0, current_tile)
            print(current_tile)
            current_tile = history[current_tile]

        return walked_list
