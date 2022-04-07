## INTO THE BACKROOMS: MAIN FILE ##
## CREATED ON MARCH 26TH, 2022 ##
## ETGG 1802 ##

## IMPORTS AND INITIALIZATIONS ##
import json
import pygame

def load_map(index) :
    """Returns a rendered map surface to caller. Which map is rendered is dictated by user-input index value."""

    # Would put all available map json files into a list, and then choose which one to load through index.
    maps = []
    maps.append(open("Maps//test_map_one.json"))
    maps.append(open("Maps//test_map_two.json"))

    map_data = json.load(maps[index])

    # Loads tileset basic data.
    class Tileset :
        """Contains tileset gid and image data so that reader can parse information accurately."""

        def __init__(self, gid, image_path) :
            img_str = "Maps\\" + image_path

            self.gid = gid
            self.image = pygame.image.load(img_str)

    class Tile :
        """A simple tile class that contains collision instructions for walls. The type of wall is dictated by
        user-input index value."""

        def __init__ (self, index, pos) :
            self.type = index
            self.pos = pos
            self.col_pos = (pos[0] + 32, pos[1] + 32)

            self.side_list = [[False, False, False, False], [True, False, False, False], [False, False, True, False],
                              [False, False, False, True], [False, True, False, False], [True, False, True, False],
                              [False, True, True, False], [False, True, False, True], [True, False, False, True]]

        def check (self, player_pos) :
            # Collision check startup.
            side_list = self.side_list[self.type - 1]

            up = side_list[0]
            down = side_list[1]
            right = side_list[2]
            left = side_list[3]

            return_x, return_y = player_pos[0] - 32, player_pos[1] - 32
            collision_bool = False

            if up == True :
                if player_pos[1] + 10 < self.col_pos[1] :
                    collision_bool = True
                    return_y += 1

            if down == True :
                if player_pos[1] > self.col_pos[1] :
                    collision_bool = True
                    return_y -= 1

            if right == True :
                if player_pos[0] - 16 > self.col_pos[0] :
                    collision_bool = True
                    return_x -= 1

            if left == True :
                if player_pos[0] + 18 < self.col_pos[0] :
                    collision_bool = True
                    return_x += 1

            return collision_bool, (return_x, return_y)

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
    for layer in data_list :
        # Establishes baseline variables.
        x = 0
        y = 0

        # Blits a select row from entry in data_list.
        for row in layer :
            x = 0

            for value in row :
                if value != 0 :
                    map_surf.blit(tilesets[0].image, (x, y), (0, (value * 64) - 64, 64, 64))
                    tile_list.append(Tile(value, (x, y)))

                x += 64

            y += 64

    return map_surf, object_list, tile_list
