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
    
    def __init__ (self, pos, index, name, image, tiles) :
        self.class_type = int(index)
        self.name = name
        self.image = image

        # CREATES ENTITY RECT #
        self.collide_rect = pygame.Rect(pos[0], pos[1], self.image.get_width(), self.image.get_height())

        # FINDS ENTITY TILE #
        for row in tiles:
            for tile in row:
                tile_rect = pygame.Rect(tile.x, tile.y, 64, 64)

                if tile_rect.colliderect(self.collide_rect):
                    self.tile = tile

    def use (self, player_facing, player_rect) :
        # LAUNCHES STUN BALL IN DIRECTION PLAYER IS FACING #
        if self.class_type == 4 :
            veloc_speed = 300

            # DICTATES VELOCITY BY PLAYER FACING #
            if player_facing == 0 :
                veloc_x, veloc_y = 0, -veloc_speed

            elif player_facing == 1 :
                veloc_x, veloc_y = 0, veloc_speed

            elif player_facing == 2 :
                veloc_x, veloc_y = veloc_speed, 0

            elif player_facing == 3 :
                veloc_x, veloc_y = -veloc_speed, 0

            # CREATES BULLET #
            return stun_ball((player_rect[0] + (player_rect[2] / 2), player_rect[1] + (player_rect[3] / 2)),
                             (veloc_x, veloc_y))

class stun_ball :
    """A basic ball that advances quickly in a given direction and will stun the monster if it collides with it.
    Degrades over time."""

    def __init__ (self, pos, velocity) :
        # ESTABLISHES CLASS VARIABLES #
        self.pos_x, self.pos_y = pos[0], pos[1]
        self.veloc_x, self.veloc_y = velocity[0], velocity[1]
        self.radius = 5

    def update (self, delta_time) :
        # MOVES BALL #
        self.pos_x += self.veloc_x * delta_time
        self.pos_y += self.veloc_y * delta_time

        # DEGRADES BALL OVER TIME #
        self.radius += 40 * delta_time

        # IF BALL IS DEGRADED ENOUGH, DESTROYS BALL #
        if self.radius > 30 :
            destroy_bool = True

        else :
            destroy_bool = False

        return destroy_bool

class sound_generation :
    """A sound radius that extends from its epicenter. If it collides with a monster it will call it to the
    epicenter of the sound radius."""

    def __init__ (self, epicenter, size, tile) :
        self.epicenter = epicenter
        self.cur_size = 0
        self.size = size
        self.tile = tile

    def update (self, delta_time) :
        # INCREASES SIZE OF RADIUS. IF RADIUS IS OF SUFFICIENT SIZE, REMOVES RADIUS #
        self.cur_size += (self.size * 3) * delta_time
        remove_bool = False

        if self.cur_size >= self.size :
            remove_bool = True

        # CREATES COLLIDE_RECT #
        collide_rect = pygame.Rect(self.epicenter[0] - self.cur_size, self.epicenter[1] - self.cur_size,
                                   self.cur_size * 2, self.cur_size * 2)

        return remove_bool, collide_rect


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
                # SKIPS DIAGONALS #
                if add_y == -1 or add_y == 1 :
                    if add_x == -1 or add_x == 1 :
                        add_x += 1

                        if add_x > 1 :
                            add_x = -1
                            add_y += 1

                        continue

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

            closed_list[cur_tile] = [total_cost, cost_so_far, heuristic, cur_tile]

        # MODIFIES HISTORY TO REAL PATH #
        walked_list = []
        current_tile = target_tile

        while current_tile is not None :
            walked_list.insert(0, current_tile)
            current_tile = history[current_tile]

        return walked_list
