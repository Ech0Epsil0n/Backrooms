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

        self.valid = valid

    def __str__(self):
        return f"TILE AT ({self.grid_x}, {self.grid_y})"

def load_map(index) :
    """Returns a rendered map surface to caller. Which map is rendered is dictated by user-input index value."""

    # Would put all available map json files into a list, and then choose which one to load through index.
    maps = []
    maps.append(open("Maps//test_map_three.json"))

    map_data = json.load(maps[index])

    # Loads tileset basic data.
    class Tileset :
        """Contains tileset gid and image data so that reader can parse information accurately."""

        def __init__(self, gid, image_path) :
            img_str = "Maps\\" + image_path

            self.gid = gid
            self.image = pygame.image.load(img_str)

    # Loads a list of tilesets from map_data.
    tilesets = []
    for tileset in map_data["tilesets"] :
        tilesets.append(Tileset(tileset["firstgid"], tileset["image"]))

    # Creates surface.
    map_width, map_height = map_data["width"], map_data["height"]
    map_width_pixels, map_height_pixels = map_width * 64, map_height * 64
    map_area = map_width_pixels * map_height_pixels
    map_surf = pygame.Surface((map_width_pixels, map_height_pixels))

    # Creates data and object lists, and loads layers into their appropriate list.
    data_list = []
    object_list = []
    tile_list = []
    wall_list = []
    layers = map_data["layers"]

    for layer in layers :
        # Attempts to access data from layer. If unsuccessful, layer must be object-laden.
        try :
            layer["data"]

        # Takes an object-laden layer and appends a tuple to object list from data.
        except :
            objects = layer["objects"]

            for object in objects :
                object_list.append((object["x"], object["y"], object["type"], object["name"]))

            continue

        # If successful, layer must be data-laden. Loads data onto list.
        temp_list = []
        x = 0

        while x < map_area:
            temp_list.append(layer["data"][x:x + map_width])
            x += map_width

        if len(temp_list) != 0 :
            data_list.append(temp_list)

    # Blits all information from data matrix.
    for dat_row in data_list :
        # Establishes baseline variables.
        x = 0
        y = 0
        grid_y = 0

        # Blits a select row from entry in data_list.
        for row in dat_row :
            x = 0
            grid_x = 0
            tile_temp = []

            for value in row :
                new_tile = Tile(x, y, grid_x, grid_y)

                if value != 0 :
                    map_surf.blit(tilesets[0].image, (x, y), (0, (value * 64) - 64, 64, 64))

                    if layer["name"] == "walls" :
                        new_tile.valid = False

                x += 64
                grid_x += 1
                tile_temp.append(new_tile)

            y += 64
            grid_y += 1
            tile_list.append(tile_temp)

    # Takes all walls and adds them to a list for easier player collision.
    for row in tile_list :
        for tile in row :
            if tile.valid == False :
                wall_list.append(tile)

    return map_surf, object_list, tile_list, wall_list
