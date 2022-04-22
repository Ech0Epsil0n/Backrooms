## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 26TH, 2022 ##
## ETGG 1802 ##

## IMPORTS AND INITIALIZATIONS ##
import json
import pygame

## DEFINES CLASSES ##
class Tile:
    """Basic tile unit used for pathfinding."""

    def __init__(self, x, y, grid_x, grid_y, valid=True) :
        self.x = x
        self.y = y
        self.grid_x = grid_x
        self.grid_y = grid_y

        self.score = 0
        self.adj_list = []
        self.valid = valid

    def __str__(self):
        return f"TILE AT ({self.grid_x}, {self.grid_y})"

    def __lt__(self, other) :
        return self.x > other.x

def load_map(index) :
    """Returns a rendered map surface to caller. Which map is rendered is dictated by user-input index value."""

    # LOADS MAPS INTO LIST #
    maps = []
    maps.append(open("Maps//test_map_one.json"))
    maps.append(open("Maps//test_map_two.json"))
    maps.append(open("Maps//test_map_three.json"))

    map_data = json.load(maps[index])

    class Tileset :
        """Contains tileset gid and image data so that reader can parse information accurately."""

        def __init__(self, gid, image_path, columns) :
            img_str = "Maps\\" + image_path

            self.gid = gid
            self.image = pygame.image.load(img_str)
            self.columns = columns

    # LOADS TILESETS #
    tilesets = []
    for tileset in map_data["tilesets"] :
        tilesets.append(Tileset(tileset["firstgid"], tileset["image"], tileset["columns"]))

    # CREATES MAP_SURF #
    map_width, map_height = map_data["width"], map_data["height"]
    map_width_pixels, map_height_pixels = map_width * 64, map_height * 64

    map_area = map_width_pixels * map_height_pixels
    map_surf = pygame.Surface((map_width_pixels, map_height_pixels))

    # INITIALIZES EMPTY LISTS #
    data_list = []
    object_list = []
    tile_list = []
    wall_list = []

    # CREATES LIST OF LAYER DATA #
    layers = map_data["layers"]

    for layer in layers :
        # IF EXCEPTION, OBJECT LAYER #
        try :
            layer["data"]

        # OBJECT LAYER DATA #
        except :
            objects = layer["objects"]

            for object in objects :
                object_list.append((object["x"], object["y"], object["type"], object["name"]))

            continue

        # IF NO-EXCEPTION, DATA LAYER #
        temp_list = []
        x = 0

        # CREATES DATA MATRIX FROM ALL DATA LAYERS #
        while x < map_area:
            temp_list.append(layer["data"][x:x + map_width])
            x += map_width

        if len(temp_list) != 0 :
            data_list.append(temp_list)

    # BLITS INFORMATION FROM DATA MATRIX #
    for dat_row in data_list :
        # BASELINE VARIABLES #
        y = 0
        grid_y = 0

        # TAKES A ROW OF DATA #
        for row in dat_row :
            x = 0
            grid_x = 0

            tile_temp = []

            # BLITS EACH INDIVIDUAL DATA VALUE TO MAP_SURF #
            for value in row :
                new_tile = Tile(x, y, grid_x, grid_y)
                wall = False

                if value != 0 :
                    tileset_int = 0

                    # FINDS PROPER TILESET #
                    if len(tilesets) > 1 :
                        calculating = True

                        while calculating :
                            try :
                                if value >= tilesets[tileset_int + 1].gid :
                                    tileset_int += 1

                                else :
                                    calculating = False

                            except IndexError :
                                calculating = False
                                pass

                    if tileset_int == 0 :
                        wall = True

                    # RESETS NECESSARY VARIABLES #
                    fav_tileset = tilesets[tileset_int]
                    column_count = fav_tileset.columns
                    value_x = value - fav_tileset.gid
                    value_y = 0

                    # FINDS PROPER ROW OF TILESET TO BLIT FROM #
                    if column_count != 1 :
                        while value_x >= column_count :
                            value_x -= column_count
                            value_y += 1

                    map_surf.blit(fav_tileset.image, (x, y), (value_x * 64, value_y * 64, 64, 64))

                    if wall == True :
                        new_tile.valid = False

                x += 64
                grid_x += 1
                tile_temp.append(new_tile)

            y += 64
            grid_y += 1
            tile_list.append(tile_temp)

    # CREATES WALL LIST #
    for row in tile_list :
        for tile in row :
            if tile.valid == False :
                wall_list.append(tile)

    return map_surf, object_list, tile_list, wall_list
